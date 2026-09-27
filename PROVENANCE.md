# Provenance and scope

Mounir IDRASSI · Version 1.0.2 · 27 September 2026

## Reviewed target and retrieval

The review initially used a local FEILIAN submission containing 74 files:
specification and basic-information PDFs, six C instances, four RTL
architectures, test vectors and supporting material. The exact file inventory
is [data/input_manifest.json](data/input_manifest.json).

On 26 September 2026, the [official Round 1 archive](https://www.niccs.org.cn/niccs/Proposal/Cryptographic%20Hash%20Algorithms/Round%201%20candidates/FEILIAN.zip) was retrieved.
All 74 original file hashes matched the existing review manifest. That
comparison was reconfirmed against the stored archive on 27 September 2026.
This subsequent check establishes the identity of the reviewed files; it does
not represent a new execution of the conformance or security experiments.

- Archive size: 46,405,040 bytes.
- Archive SHA-256: `876082a40ecf3b25d8b19478cbfeab4bd5f96ff7a293aacc5b57a9f73c2ff26c`.
- Retrieval and comparison record: [data/source_archive.json](data/source_archive.json).
- File/line locators: [data/SOURCES.md](data/SOURCES.md).

The principal specification is dated 30 June 2026, has 68 PDF pages and
642,596 bytes, and is located at `Algorithm specifications/Specification.pdf`.
Its SHA-256 is
`8e3a9a109f3188ab57cbd0156c243f80a6453051cf98006dfef11d66bdeb5fa8`.
Printed page numbers are one less than the PDF viewer page numbers.
The AddConstant diagram and boomerang inequality were also visually inspected.
All source references concern these identified bytes. The original submission
and downloaded literature are obtained separately and are not redistributed.

## Prior work and attribution

I consulted Markku-Juhani O. Saarinen's
[FEILIAN report](https://ngcc.dev/reports/hash-10.html), dated 23 September 2026,
before this review. Its reference-C allocation-failure finding is prior work;
R5 extends the static observation to optimized C. The original consultation
record is [data/prior_report.json](data/prior_report.json). R1–R4 and R6–R8
are additional observations relative to that report as consulted, without
an exhaustive novelty claim.

The [mathematical appendix](SUBCOLUMN_STRUCTURES.md) is part of this review.
It contains the concrete SubColumn classification and its composition limit.
Its full classification is a proof claim, distinct from the finite component
checks. [AI_DISCLOSURE.md](AI_DISCLOSURE.md) describes assistance used alongside
my own research, including the checked DeepSeek contributions to the appendix
counter explanation and hardware/test-generator observations.

## Secondary publication on Saarinen's site

[ngcc.dev](https://ngcc.dev/) is Markku-Juhani O. Saarinen's independent personal
initiative and states that it is unaffiliated with NICCS. It is cited here for
prior work and as an additional publication venue, without implying an official
competition decision or endorsement.

On 26 September 2026, he published my R1, R2–R3 and two R4 observations as
`hash-10-2` through `hash-10-5`, and credited my R5 extension in `hash-10-1`.
His original allocation-failure credit remains intact. The compact
[source record](data/saarinen_followup.json) gives the entries, issue
acknowledgments, consulted dates and cited harness revision. It labels the
severity and status values explicitly as metadata from his site. The original
consultation record above is preserved.

His page reports subsequent RTL simulations and reference-C partial-byte
checks; optimized-C partial-bit coverage and the length-arithmetic finding
remain based on source inspection. Those follow-up reports were not independently
reproduced here. The cited harness revision is a source locator, not a claim
that its code was audited or executed in this review.

## Code and recorded evidence

The Python model implements the stated operations separately from the original
C. Its `c` profile was checked against all three scalar variants and selected
KATs. The packaged conformance run built six unchanged C sources and compared
all short-message KATs. [evidence/README.md](evidence/README.md) identifies
the completed runs and [REPRODUCING.md](REPRODUCING.md) gives their commands.

Appendix B values are transcriptions of the identified specification, checked
against its printed digests and intermediate states. Binary ranks and Sage
polynomial/constant calculations are exact; the inverse checks use seed
20260924. Component certificates and 1,029 column / 261 half-round reference-C
comparisons have their own record. These totals retain their original execution
identities; the 27 September editorial revision does not add new algorithm runs.

The six submitted DRNG files are byte-identical, as recorded in
[data/shared_drng.json](data/shared_drng.json). Their portability and
error-propagation findings are static; the conformance driver hashes fixed
KAT messages without invoking that generator.

## Scope and release status

In my included review executions, no RTL simulation, fault injection,
extreme-length execution, noncanonical bit-input demonstration, keyed-mode
experiment or full-round attack search was performed. Larger KAT sets and the million-iteration loop were not run.
The scientific findings retain the limitations stated in the report.

Version 1.0.2 is prepared locally for release. Earlier published versions
remain unchanged. Historical drafting material and unsent correspondence are
preserved locally outside this package. No publication, upload, push,
submission or external contact was performed during this preparation.
