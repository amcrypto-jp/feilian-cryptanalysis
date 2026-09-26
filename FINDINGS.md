# Findings and evidence levels

These identifiers belong to this review. They are not assigned competition
issue numbers, CVEs or acknowledgments by the submitters. The detailed
reasoning and qualifications are in [REPORT.md](REPORT.md).

| ID | Affected material | Finding and impact | Evidence | Requested correction |
|---|---|---|---|---|
| R1 | 1SC, 4SC and 8SC hardware wrappers | Compression receives the prior block count. Zero padding and the final flag therefore do not bind the final logical length. High severity for variable-length hashing in these wrappers. | Static dataflow and state-machine review; no HDL execution. The 2SC counter path includes the current block and is an exception. | Capture the accepted block, flag and inclusive cumulative count together; validate bounds and overflow. |
| R2 | Chapter 2, Appendix A, C, RTL and hardware README | IV, AddConstant rows, counter word order and variant labels disagree. Hardware width parameters are not forwarded; its byte-only input domain and final-byte range need explicit contracts. | PDF rendering, source comparison, ordinary independent-model results, exact constant derivation. | Designate an authoritative bit-level definition and align every implementation and test. |
| R3 | Appendix B | The 512/768 examples use cumulative padded-block lengths; the 1024 examples and C use true message lengths. Padded counts omit final logical-length binding. | All six digests, 45 round snapshots, nine initial states and nine recovered domains verified against the pinned PDF. Historical generator provenance remains unconfirmed. | Preserve true-length binding and regenerate the appendix with a reproducible provenance record. |
| R4 | All six C implementations | Partial-byte canonicalization is undocumented and unenforced; length conversion and arithmetic need checks; truncation and family selection are distinct. | Static source analysis. Supplied partial-bit KATs use canonical final bytes. No noncanonical or extreme-length witness run. | Specify the bitstring contract, mask or reject unused bits, validate lengths and expose clear variant/truncation semantics. |
| R5 | Three optimized C implementations, in addition to prior reference-C report | Allocation failure is converted to an all-zero successful result through the same unchecked return path. | Static extension of Saarinen's prior finding; failure not induced. | Propagate errors through the public status and prevent failed output from being accepted. |
| R6 | §§4.2–4.6 | The proof models a different interface; idealizations are not composed; statistical results and asserted phase counts do not establish security margins. | Mathematical and proof-scope analysis. Sigma invertibility and constants positively checked. | Supply a theorem for the actual mode and quantitative analysis of message/tweak/state interactions. |
| R7 | Chapter 6 and interfaces used for keyed applications | General MAC, KDF, XOF and random-oracle replacement claims exceed the established assumptions and specifications. | Entropy, domain, composition and interface analysis; no keyed-mode implementation tested. | Specify each mode, its limits, assumptions, security notion and state-isolation contract separately. |
| R8 | Shared ICCS-attributed DRNG and KAT driver | Undefined zero-count rotation on 32-bit unsigned int; unchecked derivation and initialization failures. The six supplied FEILIAN DRNG copies are byte-identical. | Static analysis and source hashes; no sanitizer or failure-path reproduction claimed. Fixed KAT comparisons bypass the DRNG. | Coordinate an upstream correction, define rotations and propagate errors before recording vectors. |

## Scope of the strongest conclusion

R1 concerns the message encoding performed by specific hardware wrappers,
independently of the compression function's cryptanalytic strength. It should
not be reported as a demonstrated break of the correctly encoded software hash.
The source conclusion is strong, but no RTL execution or hardware measurement
has been performed. The 2SC exception does not certify that implementation as
fully conformant or secure; R2 still applies to the submission.

R6 and R7 identify missing assurance and overbroad claims. A proof gap is not an
attack. The report records what checks succeeded as well as what remains open.

## Prior work

Markku-Juhani O. Saarinen's [23 September 2026 report](https://ngcc.dev/reports/hash-10.html)
was consulted before this work. Its finding `hash-10-1` concerns silent
allocation failure in the three reference implementations. R5 extends its
implementation coverage by static inspection. The other findings are additional
relative to that report as consulted on 24 September; exhaustive priority or
novelty is not claimed. The R3 explanation and additional hardware and shared-DRNG observations were accepted from supplementary AI-generated analysis after critical checking. Acceptance of those observations does not endorse every claim in that material. [AI_DISCLOSURE.md](AI_DISCLOSURE.md) identifies GPT-6 Astra and deepseek-v4.1-flash and describes their respective roles.
