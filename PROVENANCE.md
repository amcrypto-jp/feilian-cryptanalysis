# Provenance and scope

Version 1.0.0 · prepared 24 September 2026 · intended byline: Mounir IDRASSI.

## Reviewed target

The review used a locally supplied FEILIAN directory containing 74 original
files: specification and basic information PDFs, six C instances, four RTL
architectures, test vectors and supporting material. The complete file inventory
is [data/input_manifest.json](data/input_manifest.json). An inventory is not a
claim that every file received equally deep analysis or that every test was run.

The principal PDF is `Algorithm specifications/Specification.pdf`, dated
30 June 2026, 642,596 bytes, 68 PDF pages. Its SHA-256 is:

`8e3a9a109f3188ab57cbd0156c243f80a6453051cf98006dfef11d66bdeb5fa8`

Printed page numbers are one less than the PDF viewer page numbers. The
AddConstant diagram and boomerang inequality were visually inspected in
rendered pages. The source locators refer to exact hashed files, not to an
unidentified later version. All original file hashes remained unchanged after
the review and package preparation.

The public Saarinen report links to a competition archive. That archive was
not the input used here, and its ZIP digest has not been independently verified.
The per-file manifest identifies this review target; it does not assert archive
identity. Third-party PDFs, complete sources and KAT files are not redistributed.

## Prior work and chronology

The user supplied the reference to Markku-Juhani O. Saarinen's
[FEILIAN report](https://ngcc.dev/reports/hash-10.html) at the start of the review.
The report, dated 23 September 2026 and credited there with AI assistance, was
consulted before this analysis. It identifies silent allocation failure in
the three reference C implementations as `hash-10-1`.

The present review was prepared on 24 September 2026. Static inspection extends
that finding to optimized C as R5. The page was checked again during publication
preparation; its retrieval metadata and digest are in
[data/prior_report.json](data/prior_report.json). This package does not claim
independent discovery of the known allocator defect. R1–R4 and R6–R8 are
additional observations relative to that page as consulted, without an
exhaustive prior-art or novelty claim.

Before any publication, a second researcher supplied a private report and
verification files. Their fingerprints and the accepted contributions are in
[data/second_review.json](data/second_review.json). No name or public URL was
supplied for that researcher's attribution. The researcher is credited for
the appendix counter explanation and for raising the additional hardware and
shared-DRNG issues, which were critically checked before incorporation. The
initial mismatch-only analysis is superseded by R3's exact numerical explanation.
Historical generator provenance remains a question for the submitters.

The second review was not accepted wholesale. Its general verifier was not
executed, its claimed large testing campaigns were not imported, and its
unsupported attack and generic-security claims are not part of this package's
evidence. The earlier independent model reproduced all printed intermediate
states under the accepted counter assignments. A comparison with the second
model also agreed on 60 selected canonical KATs and nine ordinary examples;
that private cross-check is supplementary, not an added 24,582-test campaign.
The packaged checker depends only on this package and the optional original
submission, not on the second researcher's files.

The six `drng.c` files supplied with FEILIAN were verified byte-identical.
The file identities are recorded in [data/shared_drng.json](data/shared_drng.json). The generator's
ICCS attribution and the README support coordination with the infrastructure
provider. No organizer was contacted as part of this preparation.

No public FEILIAN repository, DOI, report number or disclosure acknowledgment
is claimed to exist merely because a draft mentions a planned release.

## Code and execution evidence

The Python model was written separately from the supplied C implementation,
using the stated operations and parameter conventions. Its `c` profile was
checked against all three scalar variants and selected published KATs.
Independent implementation in this sentence describes separate code, not
independence from all prior literature or a second human review.

The packaged driver was rerun against hash-verified, unchanged originals. It
compiled all six C hash sources with GCC on Linux x86-64 and AVX2 and compared
all short KATs. The Python model uses a selected 20 lengths per variant.
The original run and the packaged rerun agreed. Machine-readable environment
details are in [evidence/c_conformance.json](evidence/c_conformance.json).

The quick runner's C-profile digests originated in ordinary C executions.
Alternate Chapter 2 digests are model results under explicit interpretation
choices. Appendix digest and state values are factual transcriptions, rechecked against
a fresh extraction of the pinned PDF on the packaged full run. The checker
verifies both counter conventions on only the six ordinary printed examples
and requires the expected assignment, all 45 round states and nine initial
states. Nine recovered domain values provide an additional consistency check. Sage's interval and integer checks
derive constants independently of those digest comparisons.

The 10,000 inverse samples use deterministic seed 20260924. Sampling supports
implementation validation; the algebraic inverse provides the mathematical
bijection argument. Binary rank and polynomial gcd checks establish linear
properties only, not a full-compression security bound.

## Limits and preparation status

RTL and error-path conclusions are static. No HDL simulator or physical device
was used. No fault injection, extreme-length execution, noncanonical bit-input
demonstration, full-round attack construction, exhaustive differential search
or keyed-mode execution was performed. Larger KAT sets and the million-iteration
loop were not rerun. See [REPRODUCING.md](REPRODUCING.md) for exact coverage.

OpenAI Codex assisted with analysis, code, documentation and validation. The
materials are prepared for the intended author's review; the tools cannot
attest to a separate human verification that has not taken place in this
session. No author, mailing list, repository or website was contacted with the
findings. Public pages and build dependencies were retrieved read-only.

Version 1.0.0 was revised in place after the second review because the author
confirmed that no release had occurred. [CHANGES.md](CHANGES.md) records this
prerelease revision; it is not an erratum to a published version.

Publication drafts are local files. The version/date identify this preparation,
not a claim that public distribution or peer review has already occurred.
