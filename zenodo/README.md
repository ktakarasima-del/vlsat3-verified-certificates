# Independently checked VLSAT-3 certificates and ground models

Author: Takarashima, Kenshirou

This bundle contains 34 UNSAT cases accepted by VeriPB 3.0.2 and CakePB CP2026, and 15 SAT cases checked by Z3 5.4.0 and cvc5 1.4.2 on original official SMT inputs with ground assertions inserted. Bitwuzla 0.10.0 is used only for supported bit-vector logics; SKIP_LOGIC means it was inapplicable, not that it returned SAT. See the CSV and manifest for exact case membership and hashes.

The generating solver is treated as a black box. Its source code, implementation, algorithms and executable binaries are not distributed. Only mathematical certificates, numeric CNF inputs, ground assignments and measured verification receipts are included. This is evidence of correctness for the included cases, with no speed comparison, operating-system support claim or performance ranking.

## Independent verification in three steps

1. Check all nine deliverables: `python verify_zenodo_bundle.py --bundle . --checksums-only`.
2. Obtain the original official input files separately from the per-case URLs in MANIFEST.json. Keep their original bytes as `<benchmark>.smt2` or `<benchmark>.smt2.bz2` in an input directory. Install the exact official tool versions listed in THIRD_PARTY_NOTICES.md; no tool executables are bundled.
3. Run `python verify_zenodo_bundle.py --bundle . --official-inputs INPUT_DIRECTORY --report ../verification_report.json`. Use `--veripb`, `--cakepb`, `--z3`, `--cvc5`, `--bitwuzla` to select executable paths. The script checks archive and member hashes, streams CNF decompression, checks every UNSAT proof using both checkers, checks optional kernel proofs, and checks every SAT assignment against the hash-pinned original with official solver CLIs. Large proofs run one at a time with the specified CakePB memory settings; available memory must accommodate them. The report must be stored outside the ten upload files.

The two archives and verification script can also be copied alone into an isolated directory: the script embeds both archive digests. Checking SHA256SUMS.txt for all nine files requires the complete ten-file directory and is a separate first step.

## Scope of assurance

Proof replay establishes UNSAT of the distributed DIMACS CNF. The translation receipt records measured local entailment checks using Z3 and cvc5, and Bitwuzla for supported logics. The field named translation_equivalence records this one-way original-formula-to-CNF entailment check; it is not a machine-checked bidirectional equivalence theorem. The public script does not regenerate the private translation or replay these local obligations. For SAT, the original bytes are unchanged except for adding ground assertions immediately before the single check-sat command.

Historical labels refer only to the published SMT-COMP SingleQuery results linked in the manifest: zero recorded successful runs across evaluated years 2021–2026, or zero in 2026. They do not mean the benchmarks had no previously known answer. Representative cases are explicitly marked. Missing years are not silently counted as evaluations. No claim is made about the private solver's general behavior or unlisted instances.

Generated data and documents: CC-BY-4.0. Public verifier: MIT. Third-party rights are retained; original official SMT files and external binaries are not redistributed. See LICENSE and THIRD_PARTY_NOTICES.md.
