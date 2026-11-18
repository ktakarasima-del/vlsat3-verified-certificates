#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Takarashima, Kenshirou
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
# of the Software, and to permit persons to whom the Software is furnished to
# do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
"""Verify public certificates using standard-library Python and official tools only.

No network requests are made. Supply official inputs separately. Proof checks
establish UNSAT of the included CNF; translation receipts are reported measurements,
not a separately replayable formal proof of the SMT-to-CNF correspondence.
"""
import argparse
import bz2
import gzip
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import tarfile
import tempfile

ARCHIVES = {'unsat_cakepb_proofs_bundle.tar.gz': '80acae8f51de807dbdab6a8fd2a8d5f407894e5344141ff82ebe6bc034b5f26c', 'sat_ground_models_bundle.tar.gz': '5fde2cf538fe0f14bbfcfd0e317bfaf9de7e5bb10a76c4f508ed3b3e1757aa06'}

def digest(path):
    h=hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda:f.read(1024*1024), b''): h.update(block)
    return h.hexdigest()

def require(condition,message):
    if not condition: raise ValueError(message)

def run(argv, expected, timeout, env=None):
    p=subprocess.run(argv,stdin=subprocess.DEVNULL,capture_output=True,text=True,
                     encoding='utf-8',errors='replace',timeout=timeout,env=env)
    lines={line.strip() for line in p.stdout.splitlines()}
    require(p.returncode==0 and expected in lines and 'unknown' not in lines
            and (expected not in ('sat','unsat') or lines.intersection({'sat','unsat'})=={expected}),
            'External check failed: '+Path(argv[0]).name+' '+p.stdout[-500:]+' '+p.stderr[-500:])
    return {'exit_code':p.returncode,'stdout':p.stdout,'stderr':p.stderr}

def checksums(root):
    entries=(root/'SHA256SUMS.txt').read_text(encoding='ascii').splitlines()
    require(len(entries)==9,'Expected nine checksums')
    seen=set()
    for line in entries:
        match=re.fullmatch(r'([0-9a-f]{64})  ([A-Za-z0-9_.-]+)',line)
        require(match is not None,'Invalid checksum line')
        sha,name=match.groups()
        require(name not in seen and digest(root/name)==sha,'Checksum mismatch or duplicate: '+name)
        seen.add(name)
    return len(seen)

def extract(root,out):
    members=[]
    for name,sha in ARCHIVES.items():
        archive=root/name
        require(digest(archive)==sha,'Archive digest mismatch: '+name)
        with tarfile.open(archive,'r:gz') as tf:
            for member in tf:
                require(member.isfile() and re.fullmatch(r'vlsat3_[a-l][0-9]{2}\.(?:cnf\.gz|pbp|kernel\.pbp|verification\.json|ground_asserts\.smt2|sat_verify\.json)',member.name) is not None,'Unsafe archive member')
                require(member.name not in members,'Duplicate archive member')
                require(member.size<50*10**9,'Excessive member size')
                members.append(member.name)
                with tf.extractfile(member) as src,(out/member.name).open('xb') as dst:
                    shutil.copyfileobj(src,dst,1024*1024)
    return members

def original(inputs,name,expected):
    plain=inputs/(name+'.smt2')
    compressed=inputs/(name+'.smt2.bz2')
    require(plain.is_file() or compressed.is_file(),'Missing official input: '+name)
    raw=plain.read_bytes() if plain.is_file() else bz2.decompress(compressed.read_bytes())
    require(hashlib.sha256(raw).hexdigest()==expected,'Official input hash mismatch: '+name)
    return raw

def verify(args):
    root=args.bundle.resolve()
    if args.checksums_only:
        print(json.dumps({'checksums_passed':checksums(root)})); return
    require(len(ARCHIVES)==2,'Missing archive pin')
    tools={k:str(getattr(args,k)) for k in ['veripb','cakepb','z3','cvc5','bitwuzla']}
    logs=[]
    with tempfile.TemporaryDirectory(prefix='certificate-check-',dir=args.work_dir) as td:
        out=Path(td)
        members=extract(root,out)
        receipts=sorted(out.glob('*.verification.json'))
        sat_receipts=sorted(out.glob('*.sat_verify.json'))
        require(receipts and sat_receipts,'Empty certificate set')
        expected_members=set()
        for receipt in receipts:
            d=json.loads(receipt.read_text(encoding='utf-8')); n=d['benchmark']
            require(receipt.name==n+'.verification.json' and re.fullmatch(r'vlsat3_[a-f][0-9]{2}',n),'Invalid benchmark')
            require(d['cakepb']['status']=='VERIFIED_UNSAT' and d['veripb']['status']=='VERIFIED_UNSAT' and d['translation_equivalence']['verified'] is True,'Unverified receipt')
            expected_members.update([n+'.verification.json',n+'.cnf.gz',n+'.pbp'])
            cnf=out/(n+'.cnf'); proof=out/(n+'.pbp'); kernel=out/(n+'.kernel.pbp')
            with gzip.open(out/(n+'.cnf.gz'),'rb') as src,cnf.open('xb') as dst: shutil.copyfileobj(src,dst,1024*1024)
            require(digest(cnf)==d['cnf_sha256'] and digest(proof)==d['pbp_sha256'],'Certificate hash mismatch')
            with cnf.open('rb') as f:
                require(f.readline().strip()==f"p cnf {d['cnf_variables']} {d['cnf_clauses']}".encode(),'CNF header mismatch')
            vp=run([tools['veripb'],'--cnf',str(cnf),str(proof)],'s VERIFIED UNSATISFIABLE',args.timeout)
            if kernel.exists():
                expected_members.add(kernel.name)
                run([tools['veripb'],'--cnf',str(cnf),str(kernel)],'s VERIFIED UNSATISFIABLE',args.timeout)
            env=os.environ.copy()
            env.update({'CML_HEAP_SIZE':'20480','CML_STACK_SIZE':'4096'} if d['cnf_clauses']>=5000000 else {'CML_HEAP_SIZE':'7552','CML_STACK_SIZE':'256'})
            cp=run([tools['cakepb'],str(cnf),str(kernel if kernel.exists() else proof)],'s VERIFIED UNSAT',args.timeout,env)
            logs.append({'benchmark':n,'veripb':vp,'cakepb':cp})
            cnf.unlink()
            print(n+' UNSAT verified',flush=True)
        for receipt in sat_receipts:
            d=json.loads(receipt.read_text(encoding='utf-8')); n=d['benchmark']
            require(receipt.name==n+'.sat_verify.json' and re.fullmatch(r'vlsat3_[g-l][0-9]{2}',n),'Invalid benchmark')
            expected_members.update([n+'.sat_verify.json',n+'.ground_asserts.smt2'])
            ground_path=out/(n+'.ground_asserts.smt2')
            require(digest(ground_path)==d['ground_asserts_sha256'],'Ground assignment hash mismatch')
            ground=ground_path.read_bytes()
            require(ground and all(line.startswith(b'(assert (= ') and line.endswith(b'))') for line in ground.splitlines()),'Invalid assignment file')
            raw=original(args.official_inputs,n,d['smtlib_original_sha256'])
            positions=list(re.finditer(rb'\(\s*check-sat\s*\)',raw))
            require(len(positions)==1,'Expected exactly one check-sat')
            pos=positions[0].start()
            check=out/(n+'.check.smt2'); check.write_bytes(raw[:pos]+ground+raw[pos:])
            record={'benchmark':n}
            record['z3']=run([tools['z3'],'-smt2',str(check)],'sat',args.timeout)
            record['cvc5']=run([tools['cvc5'],str(check)],'sat',args.timeout)
            if d['logic'] in ('QF_BV','QF_UFBV'):
                record['bitwuzla']=run([tools['bitwuzla'],str(check)],'sat',args.timeout)
            logs.append(record); check.unlink()
            print(n+' SAT verified',flush=True)
        require(set(members)==expected_members,'Unexpected or missing archive files')
    report={'unsat_verified':len(receipts),'sat_verified':len(sat_receipts),'checks':logs}
    if args.report: args.report.write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'unsat_verified':len(receipts),'sat_verified':len(sat_receipts)}))

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--bundle',type=Path,default=Path('.'))
    p.add_argument('--checksums-only',action='store_true')
    p.add_argument('--official-inputs',type=Path)
    p.add_argument('--work-dir',type=Path)
    p.add_argument('--report',type=Path)
    p.add_argument('--timeout',type=int,default=3600)
    for k,default in [('veripb','veripb'),('cakepb','cake_pb_cnf'),('z3','z3'),('cvc5','cvc5'),('bitwuzla','bitwuzla')]: p.add_argument('--'+k,default=default)
    args=p.parse_args()
    if not args.checksums_only: p.error('--official-inputs is required') if args.official_inputs is None else None
    verify(args)

if __name__=='__main__': main()
