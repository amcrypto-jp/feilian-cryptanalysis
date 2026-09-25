# Verification guide

Run these commands from the extracted versioned package. The Python tools need
Python 3.11 or later and use only its standard library. The C driver targets
Linux and uses GCC by default. SIMD checks run automatically only on an x86-64
host advertising AVX2; an omitted SIMD run is reported as skipped. SageMath is
optional for the exact polynomial and constant checks. `pdftotext` is required
by `--mode all` to re-extract Appendix B.

## Package integrity

```sh
python3 verify_package.py
```

Alternatively, `sha256sum -c SHA256SUMS` checks the same listed files.
The manifest detects changed bytes; it does not authenticate the author and
does not audit additional unlisted files. Outputs belong in a separate directory.

## Self-contained checks

```sh
python3 run.py --mode quick --output-dir verification-quick
```

This computes the empty message, `abc` and 129 repetitions of `a` for each
output size, under both documented interpretations. The `c` profile follows
the executed C convention. The `chapter2` profile uses the printed IV and
AddConstant rows, little-endian words from §3.2, and the high-word-first
counter convention used by C. It is an explicitly chosen interpretation of an
inconsistent specification, not a declaration of the canonical algorithm.

The stored C-profile values were obtained from the original C execution and
matched by the separately written model. The alternate-profile values are
regression records of that model. The six Appendix B digests and 54 displayed matrices are factual transcriptions
checked against the original PDF. Only the initial IV displays are transposed
when normalizing them. In quick mode the values are read from
[data/appendix_states.json](data/appendix_states.json); the original PDF is not
re-extracted. The checker is limited to the six fixed printed examples. It
enforces the 1024/true-count and 512/768/padded-count assignments and checks
all 45 round snapshots, nine initial states and nine recovered domain values.

This command also performs 10,000 deterministic forward/inverse SubColumn
checks and computes the two binary linear-map ranks. It does not search for
collisions or test failure conditions. A successful exit means the recorded
comparisons held, including the expected Appendix B counter assignments and
the four remaining disagreements with the C convention.

## Full C and short KAT comparison

Obtain the same FEILIAN submission separately and replace `/path/to/FEILIAN`
below with its extracted root, containing `Algorithm specifications`,
`Implementations` and `Test_Vectors`.

```sh
python3 run.py --mode all --submission-root /path/to/FEILIAN --output-dir verification-full
```

All 74 original files must match [data/input_manifest.json](data/input_manifest.json)
before the C sources are compiled. A modified or incomplete submission is
rejected. Extra files in the submission directory are ignored. The tool creates
temporary shared libraries, loads them through `ctypes`, and removes the build
directory when finished. It does not edit the originals. It builds only the
hash source for each instance, not an arbitrary supplied build script.

Expected results on an AVX2 Linux host are:

| Check | Expected result |
|---|---|
| Scalar C, 512/768/1024 | 4,097 short KATs passed each |
| SIMD C, 512/768/1024 | 4,097 short KATs passed each |
| Independent Python model | 20 selected KAT lengths passed per size |
| Ordinary examples | Nine C/model agreements |
| Appendix B | Six digests, 45 round snapshots, nine initial states and nine domains explained; true counts for 1024, padded counts for 512/768 |
| SubColumn samples | 10,000 forward/inverse agreements |
| Sigma maps | Binary rank 64 each |

The selected model lengths are 0, 1, 7, 8, 9, 63, 64, 65, 511, 512, 513,
1016, 1023, 1024, 1025, 1031, 1032, 2047, 2048 and 4096 bits.
The C path checks every length 0 through 4096 inclusive. Unused final-byte
bits in these KATs are canonical. For scalar-only execution add `--simd off`;
for the C comparisons alone, without Appendix B extraction, use `--mode c`.

The recorded run is [evidence/reproduce-full.log](evidence/reproduce-full.log),
with machine-readable results in that directory. Compiler warnings were
retained; they do not constitute additional findings.

## Exact Sage checks

```sh
sage code/arithmetic_checks.sage
```

The result is written to `verification-sage/arithmetic.json`; optionally set
the `FEILIAN_REVIEW_OUTPUT` environment variable to another output path.
Sage checks the two Sigma polynomials modulo `x^64 + 1`, their gcds and
fixed-space dimensions. Certified interval arithmetic derives the first 256
hexadecimal fractional digits of pi; exact integer arithmetic derives the four
square-root constants. The results should agree with
[evidence/arithmetic.json](evidence/arithmetic.json).

## Static findings and exclusions

[data/SOURCES.md](data/SOURCES.md) and [data/rtl_source_facts.json](data/rtl_source_facts.json)
identify the source evidence for manual inspection against the pinned files.
These are locators and observations, not an RTL execution transcript. Read the
enclosing state machines and interfaces, not just the quoted lines.
[data/shared_drng.json](data/shared_drng.json) records the six byte-identical
DRNG copies supplied with FEILIAN. The generator and its failure paths are
not executed by these checks; the C/KAT driver consumes fixed KAT message bytes
directly. Reading supplied vectors and regenerating them are distinct checks.

No hardware simulator, synthesis or device test was run. No allocation failure,
noncanonical final-byte request, oversized length or 32-bit truncation case
was executed. The long `2^23` and `2^33` KAT sets and million-iteration loop
were not rerun. No full-round differential search, collision construction,
side-channel measurement or MAC/KDF/XOF execution was performed. The package
therefore verifies the ordinary computations and arithmetic described above;
it does not turn all static findings into experimental demonstrations.

## Rebuilding the documents

The included documents were built with Pandoc 3.11 and Tectonic 0.17.0 using
DejaVu fonts. Install those tools and fonts, then run:

```sh
python3 build_documents.py
```

Use `--pandoc /path/to/pandoc --tectonic /path/to/tectonic` for tools outside
PATH. Tectonic may fetch its public TeX bundle on first use. The resulting
HTML embeds its stylesheet and uses native MathML; it needs no network access
to render. Rebuilds can change PDF metadata and hashes. Review the rebuilt
documents and regenerate release manifests only when intentionally issuing
a changed package; do not expect byte-identical PDF output across environments.
