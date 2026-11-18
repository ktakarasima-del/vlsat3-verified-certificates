# Third-party notices

No third-party tool source or binary is distributed. These hashes identify the exact binaries used for local measurements; other platform builds can have different hashes.

| Tool | Official source | Binary SHA-256 | License |
|---|---|---|---|
| VeriPB 3.0.2 | https://gitlab.com/MIAOresearch/software/VeriPB/-/tree/3.0.2 | d634fddf0a207435c8805c982d289e9a4b1bae43a15ddea932e7d41b30319806 | MIT OR Apache-2.0 |
| CakePB CP2026 | https://gitlab.com/MIAOresearch/software/cakepb/-/tree/CP2026 | f053e94e6d884ccf01e89ec11db934657f45d7d0b0682ea84393bcfb6c9e4792 | BSD-3-Clause (CakeML binary distribution) |
| Z3 5.4.0 | https://github.com/Z3Prover/z3/releases/tag/z3-5.4.0 | 51ea6db335860c584f059fec618ce4de8208776b12103043e6bcfb4003f67479 | MIT |
| cvc5 1.4.2 | https://github.com/cvc5/cvc5/releases/tag/cvc5-1.4.2 | 6aecddf466552b83bb5883756c7955e0c9d5ddcc6d7f45b48c2f6e06a741b102 | BSD-3-Clause; bundled dependencies retain their own licenses |
| Bitwuzla 0.10.0 | https://github.com/bitwuzla/bitwuzla/releases/tag/0.10.0 | 66db2cfb0ba87caaab31448a5e39e4988da4e2f71733d694d6852745342c8ce9 | MIT; bundled dependencies retain their own licenses |
| Z3 5.4.0 (additional verification component: libz3.dll) | https://github.com/Z3Prover/z3/releases/tag/z3-5.4.0 | d59390c48442c5ca040cf1545cf85f84f24354edf9c768dfd16438e2aee654ae | MIT |

Official license references:

- https://gitlab.com/MIAOresearch/software/VeriPB/-/blob/3.0.2/LICENSE-MIT
- https://gitlab.com/MIAOresearch/software/cakepb/-/tree/CP2026
- https://github.com/Z3Prover/z3/blob/master/LICENSE.txt
- https://github.com/cvc5/cvc5/blob/cvc5-1.4.2/COPYING
- https://github.com/bitwuzla/bitwuzla/blob/0.10.0/COPYING

VLSAT-3 / 20210312-Bouvier benchmark source: https://cadp.inria.fr/resources/vlsat/3.html . Attribution: Pierre Bouvier, The VLSAT-3 Benchmark Suite, INRIA Technical Report 516 (2021). Original SMT inputs are not redistributed. CNF files are mathematical translations of the official benchmarks. The data license applies to newly generated contributions only and does not relicense any third-party rights. Each selected official input declares CC-BY-4.0 in its SMT metadata. The original author is credited above. Changes: numeric CNF translation and independently generated certificates and assignments; original SMT files are not included.

Competition data: https://github.com/SMT-COMP/smt-comp.github.io/tree/master/data . Per-year source URLs and per-case counts are in MANIFEST.json. Historical classification is restricted to the recorded evaluated years and SingleQuery track.
