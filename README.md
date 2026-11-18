# Independently checked VLSAT-3 evidence

This repository is a lightweight verification companion to the published dataset **Independently checked VLSAT-3 certificates and ground models**.

**Dataset and proof archives:** [Zenodo record](https://zenodo.org/records/24299444) · [DOI: 10.5281/zenodo.24299444](https://doi.org/10.5281/zenodo.24299444)

## Results and scope

- **34 UNSAT certificates:** the associated DIMACS CNFs were accepted by VeriPB 3.0.2 and CakePB CP2026. Three cases also include elaborated kernel proofs.
- **15 SAT ground-assignment checks:** Z3 5.4.0 and cvc5 1.4.2 accepted the hash-pinned original SMT inputs with the supplied assignments inserted before check-sat. All 15 use datatype logics; Bitwuzla is inapplicable to these SAT cases and is recorded as SKIP_LOGIC.
- The included UNSAT cases span six SMT logics. Historical labels describe published SMT-COMP SingleQuery result records in 2021-2026, not globally unknown satisfiability answers.
- **Reported machine:** Intel Core i7 processor, **64GB RAM**. The exact CPU model is unspecified. This hardware description is not a controlled speed comparison, minimum-memory claim or performance ranking.

The generating solver is a black box. Its source, implementation details and executable binaries are not distributed here. The public verifier uses Python's standard library and official external tool CLIs only.

## Verify the published dataset

1. Download **all ten files** from the Zenodo record into a separate directory. The two large evidence archives are hosted on Zenodo, not stored in Git history.
2. In that directory run:

```sh
python verify_zenodo_bundle.py --bundle . --checksums-only
```

3. Obtain the original official SMT inputs from the URLs in MANIFEST.json, install the pinned official tool versions in THIRD_PARTY_NOTICES.md, and run:

```sh
python verify_zenodo_bundle.py --bundle . --official-inputs INPUT_DIRECTORY --report ../verification_report.json
```

The exact small published files are mirrored under [zenodo/](zenodo/). Its SHA256SUMS.txt belongs to the **complete original ten-file Zenodo release**, including both archives. It is not a checksum list for this repository's root README. Keep reports outside the dataset directory.

## What is independently checked?

UNSAT proof replay establishes that the distributed CNF is unsatisfiable. Translation receipts record measured local, one-way original-formula-to-CNF entailment checks using Z3 and cvc5, and Bitwuzla where applicable. The public script does not regenerate the private translation or replay those local obligations. The receipt field translation_equivalence is not a publicly machine-checked bidirectional equivalence theorem.

For SAT, the public script checks the supplied assignments on the official original input bytes, with only assignment assertions inserted before the original check-sat command. It does not replace the input by a private normalization.

## Attribution and licenses

Dataset author: **Takarashima, Kenshirou**, as credited in the published Zenodo record. VLSAT-3 benchmark attribution and tool source URLs/licenses are retained in [THIRD_PARTY_NOTICES.md](zenodo/THIRD_PARTY_NOTICES.md).

Generated data and documentation are CC-BY-4.0; the public verifier is MIT. Third-party rights are retained. See [LICENSE](zenodo/LICENSE). This repository does not grant rights to the private generating solver. This root README adds the repository layout and author-reported hardware to the preserved release documentation.

Use the Zenodo DOI to cite the fixed evidence release; CITATION.cff points to that dataset. Repository publication does not constitute peer review or independent endorsement.
