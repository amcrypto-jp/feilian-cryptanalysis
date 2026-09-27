# Recorded validation

The conformance and arithmetic files record executions on 24 September 2026.
The document and component checks below were added on 26 September 2026. The
original submission was hash-verified before C compilation. The 27 September
editorial update preserves these results and does not add algorithm executions.

| Record | Contents |
|---|---|
| [reproduce-full.log](reproduce-full.log) | Standard output from `run.py --mode all` |
| [c_conformance.json](c_conformance.json) | Platform/compiler details, 24,582 passing C-to-KAT checks, 60 selected independent-model KAT checks and nine ordinary C/model examples |
| [quick.json](quick.json) | Ordinary examples in both stated profiles, 10,000 inverse checks and both binary ranks |
| [appendix_comparison.json](appendix_comparison.json) | Six digests, 45 round snapshots, nine initial states and nine recovered domains; fixed variant/count assignments verified against a fresh PDF extraction |
| [arithmetic.json](arithmetic.json), [sage.log](sage.log) | SageMath 10.9 exact polynomial, interval and integer checks |
| `FEILIAN*_build.log` | Actual GCC diagnostics from the six C builds |

The recorded Python version is 3.14.4 and GCC is 15.2.0 on Linux x86-64 with
AVX2. Compilation used C99, optimization level 2, shared/PIC output and the
warning flags documented in the driver; SIMD builds additionally used AVX2.
No original C source was patched. Compiler diagnostics concern a validated
positive output-length conversion and unused SIMD masks. They are retained
for transparency, not characterized as new security findings.

Sage confirms rank 64 and one-dimensional fixed spaces for both Sigma maps,
the repeated factorization of the word modulus, all sixteen pi-derived IV
words and the four square-root constants. The ordinary comparisons reproduce
the disagreements described in the report; the Appendix B mismatch rows are
expected findings, not failures of the verification runner. The exact counter
convention explaining each example is now checked, including intermediate
states. The unchanged Sage record remains from the initial run; its code and
mathematical claims were not altered by this revision.

The DRNG findings are static observations with source-identity records under
`data/`; no sanitizer or allocation-failure results are claimed here. The full
C driver does not run the DRNG.

No RTL execution is recorded here. The RTL observations are in the static
source index under `data/`. Allocation failures, noncanonical inputs, extreme
lengths, long KAT collections, keyed modes and full-round attack searches were
not executed. See [REPRODUCING.md](../REPRODUCING.md).

Saarinen's personal site separately reports follow-up checks; see the
[secondary-source record](../data/saarinen_followup.json). Those reports were
not independently reproduced here and do not change the execution records above.

Document rebuilding is separate from the scientific runs recorded here.
It does not change their coverage or execution dates.

## Specification example check

[specification_examples.json](specification_examples.json) and
[its log](specification_examples.log) record extraction of both identical
§4.5.2 examples from the pinned PDF. The command and original-source requirement
are in [REPRODUCING.md](../REPRODUCING.md).

## Component classification checks

[subcolumn_structures.json](subcolumn_structures.json), [its log](subcolumn_structures.log) and [C build log](subcolumn_c_build.log) record the checks accompanying [SUBCOLUMN_STRUCTURES.md](../SUBCOLUMN_STRUCTURES.md). These include exact ranks, small addition-mask classifications, finite component nonconstancy certificates and 1,029 column / 261 half-round agreements with the original scalar C. The complete 64-bit LD classification is an analytical theorem, not a sampling inference or a machine-checked proof.
