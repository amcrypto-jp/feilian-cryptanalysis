# Version history

## 1.0.0 — 24 September 2026 — unpublished preparation

The initial local package contained the R1–R7 assessment, ordinary conformance
and Sage checks, pinned source inventory, execution evidence, attribution and
AI disclosures, and unsent publication drafts.

Before publication, the author authorized incorporation of the critically
assessed second review. The same version was revised in place:

- R3 now explains the appendix counts exactly: padded-block lengths for
  512/768, true message lengths for 1024. The portable checker verifies all six
  digests, 45 round states, nine initial states and nine recovered domains.
- R2 specifies the unforwarded width parameter, byte-only hardware domain,
  legal final-byte range and matrix-display distinction. R1 remains a static
  finding, with 2SC explicitly excepted from the counter-timing defect.
- New R8 concerns shared DRNG/test-driver portability and failure propagation.
  Its scope is vector generation; it does not invalidate fixed-vector hashing.
- R4/R6/R7 clarify partial-byte digest storage, Davies–Meyer fixed-point scope,
  MAC forgery versus tag collisions, and unambiguous fixed-width KDF counters.
- Provenance credits the second review's accepted contributions. Unsupported
  larger testing claims and incorrect conclusions were excluded. Documents,
  drafts, website files, evidence records, archives and manifests were rebuilt.

The original submission and supplied second-review files were not modified.
No publication, submission, author contact or deployment occurred. This is a
preparation history, not an erratum to an already published release.

### Editorial update — 25 September 2026

Made the disclosure, provenance, licensing notes and supporting drafts specific
to the FEILIAN review. R8's source-identity record covers the six DRNG copies
supplied with FEILIAN. The findings and recorded algorithm checks are unchanged.
Document formats, archives and integrity manifests were regenerated.
