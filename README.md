# FEILIAN technical review — version 1.0.0

Mounir IDRASSI · [mounir@amcrypto.jp](mailto:mounir@amcrypto.jp) · 24 September 2026

This package assesses the FEILIAN submission dated 30 June 2026. It contains
a report, source references, ordinary conformance and arithmetic checks, and
publication drafts. The recommendation is to request a corrected submission
before adoption. The strongest implementation finding is a message-length
binding defect in the 1SC, 4SC and 8SC RTL wrappers, established by static
analysis. The 2SC counter path is an explicit exception. This review does not
establish a full-round cryptanalytic break of the correctly encoded software hash.

The materials are prepared locally for the named author's review and possible
release. No publication, submission, author contact or external issue creation
was performed in preparing this package.

## Start here

| Material | Purpose |
|---|---|
| [REPORT.pdf](REPORT.pdf) | Typeset assessment for circulation |
| [REPORT.html](REPORT.html) | Offline browser version with native MathML |
| [REPORT.md](REPORT.md), [REPORT.tex](REPORT.tex) | Editable report sources |
| [FINDINGS.md](FINDINGS.md) | Findings, evidence levels and requested corrections |
| [REPRODUCING.md](REPRODUCING.md) | Commands and exact test coverage |
| [PROVENANCE.md](PROVENANCE.md) | Reviewed inputs, chronology, attribution and limitations |
| [data/SOURCES.md](data/SOURCES.md) | Portable file and line locators for the original submission |
| [evidence/](evidence/) | Recorded executions of the included verification code |
| [ANNOUNCEMENT.md](ANNOUNCEMENT.md), [AUTHOR_LETTER.txt](AUTHOR_LETTER.txt) | Unsent publication and correspondence drafts |
| [CITATION.cff](CITATION.cff), [references.bib](references.bib) | Citation metadata and bibliography |
| [AI_DISCLOSURE.md](AI_DISCLOSURE.md), [LICENSING.md](LICENSING.md) | Preparation and reuse terms |
| [GITHUB.md](GITHUB.md), [CHANGES.md](CHANGES.md) | Release instructions and version history |

## Verified coverage

All 4,097 short-message KATs passed for each of six C implementations: 24,582
C-to-KAT comparisons. The independent Python model matched 20 selected lengths
per output size and nine ordinary examples. Appendix B is now explained exactly:
512/768 examples use padded-block counts, while 1,024-bit examples use true
message lengths. All six digests, 45 printed round states, nine initial states
and nine recovered domains agree under those assignments.
Both Sigma maps have rank 64; 10,000 deterministic SubColumn inverse checks
passed, and Sage confirmed the constants and polynomial calculations.

RTL findings, noncanonical-bit handling, size-conversion issues and allocation
failure paths were assessed statically. No RTL simulation, fault injection,
extreme-length execution or full-round cryptanalytic search was performed.
The shared DRNG/KAT-driver finding R8 is also static and concerns vector
generation, not the FEILIAN primitive. Passing conformance checks is not a
proof of security.

## Quick verification

From the extracted package directory, with Python 3.11 or later:

```sh
python3 verify_package.py
python3 run.py --mode quick --output-dir verification-quick
```

The first command checks the file hashes, not author identity. The second uses
only packaged ordinary examples and does not need the original submission.
For the full C/KAT comparison and exact Sage checks, follow
[REPRODUCING.md](REPRODUCING.md). Original submission files, compiled libraries
and local build dependencies are not redistributed.

## Attribution and release boundary

[Saarinen's report](https://ngcc.dev/reports/hash-10.html) was consulted before
this review. Its reference-C allocation-failure finding is credited as prior
work; R5 extends the static observation to optimized C. This package makes
no claim of independent discovery of that finding or exhaustive novelty.
A privately supplied second review is credited for the appendix explanation
and additional hardware/DRNG observations accepted after critical checking.
Its unsupported or incorrect claims are not incorporated. See
[data/second_review.json](data/second_review.json) for input fingerprints.
OpenAI Codex assisted with the review and preparation; see the disclosure.

The versioned package directory is the intended repository root. The parent
submission workspace and private working notes are outside the release.
MIT applies to the original review software and build assets; CC BY 4.0 applies
to the original report, documentation and result records, subject to the
third-party exceptions in [LICENSING.md](LICENSING.md).
