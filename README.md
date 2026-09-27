# FEILIAN technical review — version 1.0.2

Mounir IDRASSI · [mounir@amcrypto.jp](mailto:mounir@amcrypto.jp) · 27 September 2026

This review assesses the FEILIAN submission dated 30 June 2026. The package
contains the report, a mathematical appendix, source identifiers, reproduction
code and recorded results. It recommends a corrected submission before
adoption. The principal implementation finding concerns message-length binding
in the 1SC, 4SC and 8SC RTL wrappers, established by static analysis; the 2SC
counter path is an explicit exception. No full-round cryptanalytic break of
the correctly encoded software hash is established.

Version 1.0.2 adds the complete SubColumn whole-output derivative classification,
its scoped composition limit, and clarifications of R6/R7. It also provides a
verified original-archive locator and cross-references to Saarinen's
subsequent publication of my findings. R1–R8 retain their evidence classifications
and the earlier conformance and arithmetic results. This version is prepared
locally for release. Earlier published versions remain historical snapshots.

## Start here

| Material | Purpose |
|---|---|
| [REPORT.pdf](REPORT.pdf), [REPORT.html](REPORT.html) | Typeset and offline browser versions |
| [REPORT.md](REPORT.md), [REPORT.tex](REPORT.tex) | Editable report sources |
| [FINDINGS.md](FINDINGS.md) | Findings, evidence levels and requested corrections |
| [SUBCOLUMN_STRUCTURES.md](SUBCOLUMN_STRUCTURES.md) | Mathematical appendix: complete component classification and composition limit |
| [REPRODUCING.md](REPRODUCING.md) | Commands, dependencies and exact coverage |
| [PROVENANCE.md](PROVENANCE.md), [data/SOURCES.md](data/SOURCES.md) | Source identity, retrieval and attribution |
| [evidence/](evidence/) | Recorded executions of the included checkers |
| [CITATION.cff](CITATION.cff), [references.bib](references.bib) | Citation metadata and bibliography |
| [AI_DISCLOSURE.md](AI_DISCLOSURE.md), [LICENSING.md](LICENSING.md) | Assistance disclosure and reuse terms |
| [GITHUB.md](GITHUB.md), [CHANGES.md](CHANGES.md) | Release guide and version history |

## Recorded verification

All 4,097 short-message KATs passed for each of six C implementations: 24,582
C-to-KAT comparisons. A separately written Python model matched 20 selected
lengths per output size and nine ordinary examples. All six Appendix B digests,
45 round states, nine initial states and nine recovered domains agree under
the identified counter conventions: padded-block counts for 512/768 and true
message lengths for 1024. Both Sigma maps have rank 64; 10,000 deterministic
SubColumn inverse checks passed, and Sage confirmed the arithmetic results.
The mathematical appendix has additional component checks documented in
[evidence/README.md](evidence/README.md).

My recorded evidence for RTL, noncanonical-input and failure-path findings
remains static. No RTL simulation, fault injection, extreme-length execution
or full-round attack search is included. These successful computations do not prove hash security.

## Reproduction

From the extracted package, with Python 3.11 or later:

```sh
python3 verify_package.py
python3 run.py --mode quick --output-dir verification-quick
```

The quick command needs no original submission. For C/KAT comparisons and
optional Sage checks, follow [REPRODUCING.md](REPRODUCING.md). The official
archive locator and checksum are in [data/SOURCES.md](data/SOURCES.md); all
74 original files matched the review's existing manifest.

## Attribution and package scope

I consulted [Saarinen's report](https://ngcc.dev/reports/hash-10.html) before
this review. Its reference-C allocation-failure finding is credited as prior
work; R5 extends its static coverage to optimized C. No exhaustive priority
claim is made. [AI_DISCLOSURE.md](AI_DISCLOSURE.md) describes the assistance
used alongside my own research and my responsibility for the conclusions.

Saarinen's ngcc.dev is an independent personal initiative, unaffiliated with
NICCS. It is a secondary reference for prior work and another publication venue
for my findings. The [publication mapping](FINDINGS.md#secondary-publication-record)
and [source record](data/saarinen_followup.json) identify the later entries and
his reported follow-up checks. The site's labels are its own editorial assessments.

Use this versioned directory as the repository root. Original submission files,
private drafting records and unsent correspondence are kept separately. MIT
applies to the original review software and build assets; CC BY 4.0 applies to
the original report, documentation and result records, with the exceptions in
[LICENSING.md](LICENSING.md).
