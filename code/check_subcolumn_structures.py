#!/usr/bin/env python3
"""Check component identities and nonconstancy certificates, not hash attacks.

Universal 64-bit claims are proved in SUBCOLUMN_STRUCTURES.md. These finite
checks do not constitute a machine-checked proof of that document.
"""
import argparse
import ctypes
import itertools
import json
from pathlib import Path
import random
import shutil
import subprocess
import sys
import tempfile

sys.dont_write_bytecode = True
from model import MASK, half_round, inverse_subcolumn, linear_rank, ror
from model import sigma0, sigma1, subcolumn
from inputs import verify_submission

M = 1 << 63
PACKAGE = Path(__file__).resolve().parents[1]


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def xor(a, b):
    return tuple(x ^ y for x, y in zip(a, b))


def column(base):
    return subcolumn(*base)


def matrix(base):
    out = list(base)
    for c in range(4):
        values = subcolumn(*(base[4*r+c] for r in range(4)))
        for r in range(4):
            out[4*r+c] = values[r]
    return tuple(out)


def second_layer(base):
    return matrix(half_round(base))


def derivative(function, base, delta):
    return xor(function(base), function(xor(base, delta)))


def nonconstant_certificate(function, delta, rng):
    first_base = tuple(0 for _ in delta)
    first_output = derivative(function, first_base, delta)
    for attempt in range(1, 129):
        second_base = tuple(rng.getrandbits(64) for _ in delta)
        second_output = derivative(function, second_base, delta)
        if first_output != second_output:
            return {
                'delta': delta,
                'base1': first_base, 'derivative1': first_output,
                'base2': second_base, 'derivative2': second_output,
                'bases_evaluated': attempt + 1,
            }
    raise RuntimeError('No nonconstancy certificate found within the budget; inconclusive')


def check_addition_lemma():
    records = []
    for width in (2, 3, 4):
        modulus = 1 << width
        top = modulus >> 1
        for terms in (2, 3):
            tuples = list(itertools.product(range(modulus), repeat=terms))
            found = set()
            evaluations = 0
            for delta in tuples:
                beta = sum(delta) % modulus
                for base in tuples:
                    evaluations += 1
                    value = (sum(a ^ b for a, b in zip(base, delta)) % modulus) ^ (sum(base) % modulus)
                    if value != beta:
                        break
                else:
                    found.add(delta)
            expected = set(itertools.product((0, top), repeat=terms))
            minus_case = (terms - 1) % top == 0
            if minus_case:
                expected.update(itertools.product((top - 1, modulus - 1), repeat=terms))
            require(found == expected, 'Addition-lemma check failed')
            records.append({
                'width': width, 'summands': terms, 'candidate_mask_tuples': len(tuples),
                'constant_derivatives': len(found), 'evaluations': evaluations,
                'minus_case_present': minus_case,
                'scope': 'Every mask classified by exhaustive base evaluation or an exact counterexample',
            })
    return records


def check_reference_c(submission, output, rng):
    root, count = verify_submission(submission)
    compiler = shutil.which('gcc')
    if compiler is None:
        raise RuntimeError('gcc is required for the optional reference-C comparison')
    source = root / 'Implementations/Reference_Implementation/FEILIAN1024'
    wrapper = """
#include "CryptHash_AlgorithmInstance.c"
void review_column(const uint64_t *in, uint64_t *out) {
    for (int i=0; i<4; i++) out[i]=in[i];
    sbox_column(&out[0], &out[1], &out[2], &out[3]);
}
void review_half(const uint64_t *in, uint64_t *out) {
    uint64_t s[4][4];
    for (int r=0; r<4; r++) for (int c=0; c<4; c++) s[r][c]=in[4*r+c];
    sbox_matrix(s);
    shift_rows(s);
    for (int r=0; r<4; r++) for (int c=0; c<4; c++) out[4*r+c]=s[r][c];
}
"""
    with tempfile.TemporaryDirectory(prefix='feilian-components-') as temporary:
        target = Path(temporary) / 'components.so'
        result = subprocess.run(
            [compiler, '-std=c99', '-O2', '-Wall', '-Wextra', '-shared', '-fPIC',
             '-I', str(source), '-x', 'c', '-', '-o', str(target)],
            input=wrapper, text=True, capture_output=True,
        )
        log = (result.stdout + result.stderr).replace(str(root), '<submission>').replace(temporary, '<build>')
        (output / 'subcolumn_c_build.log').write_text(log)
        result.check_returncode()
        library = ctypes.CDLL(str(target))
        counts = {}
        for name, size, function, random_cases in (
                ('review_column', 4, column, 1024),
                ('review_half', 16, half_round, 256)):
            native = getattr(library, name)
            native.argtypes = (ctypes.POINTER(ctypes.c_uint64), ctypes.POINTER(ctypes.c_uint64))
            native.restype = None
            cases = [tuple([x] * size) for x in (0, 1, M - 1, M, MASK)]
            cases += [tuple(rng.getrandbits(64) for _ in range(size)) for _ in range(random_cases)]
            for base in cases:
                inp = (ctypes.c_uint64 * size)(*base)
                out = (ctypes.c_uint64 * size)()
                native(inp, out)
                require(tuple(out) == tuple(function(base)), 'Reference C differs from the review model')
            counts[name] = len(cases)
    return {
        'original_files_verified': count,
        'source': 'Implementations/Reference_Implementation/FEILIAN1024/CryptHash_AlgorithmInstance.c',
        'scope': 'Ordinary component evaluations; no hash collision or attack experiment',
        'column_comparisons': counts['review_column'],
        'half_round_comparisons': counts['review_half'],
        'compiler': subprocess.check_output([compiler, '--version'], text=True).splitlines()[0],
    }


def run(output, submission=None):
    rng = random.Random(20260926)
    require(ror(M, 63) == 1, 'Incorrect ROR63 convention')
    require(sigma0(1 << 55) == (1 << 55) ^ (1 << 50) ^ (1 << 7), 'Sigma0 bit identity')
    require(sigma1(1) == 1 ^ (1 << 53) ^ (1 << 24), 'Sigma1 bit identity')
    ranks = [linear_rank(sigma0), linear_rank(sigma1)]
    require(ranks == [64, 64], 'Sigma map not bijective')
    addition = check_addition_lemma()

    family = {
        (x, y, x, x ^ y): (x ^ y, 0, y, 0)
        for x in (0, M) for y in (0, M)
    }
    bases = [tuple([x] * 4) for x in (0, 1, M - 1, M, MASK)]
    bases += [tuple(rng.getrandbits(64) for _ in range(4)) for _ in range(256)]
    for delta, expected in family.items():
        for base in bases:
            require(derivative(column, base, delta) == expected, 'T1 identity failed')
    for base in bases:
        require(inverse_subcolumn(*column(base)) == base, 'Component inverse failed')

    exclusions = []
    for delta in itertools.product((0, M), repeat=4):
        if delta not in family:
            exclusions.append(nonconstant_certificate(column, delta, rng))
    require(len(exclusions) == 12, 'Incomplete MSB exclusions')

    non_msb = [(MASK, 0, 0, 0), (0, MASK, 0, 0), (0, 0, MASK, 0),
               (0, 0, 0, MASK), (MASK,) * 4, (1,) * 4, (0x5555555555555555,) * 4]
    other_certificates = [nonconstant_certificate(column, delta, rng) for delta in non_msb]

    composition = []
    matrix_cases = 0
    parameters = list(itertools.product((0, M), repeat=2))
    for choices in itertools.product(parameters, repeat=4):
        delta = [0] * 16
        expected_matrix = [0] * 16
        expected_half = [0] * 16
        for c, (x, y) in enumerate(choices):
            delta[c], delta[4+c], delta[8+c], delta[12+c] = x, y, x, x ^ y
            expected_matrix[c], expected_matrix[8+c] = x ^ y, y
            expected_half[c] = x ^ y
            expected_half[8 + (c - 2) % 4] = y
        for _ in range(4):
            base = tuple(rng.getrandbits(64) for _ in range(16))
            require(derivative(matrix, base, delta) == tuple(expected_matrix), 'T3 full difference map failed')
            require(derivative(half_round, base, delta) == tuple(expected_half), 'T4 full difference map failed')
            matrix_cases += 1
        if any(delta):
            composition.append(nonconstant_certificate(second_layer, delta, rng))
    require(len(composition) == 255, 'Incomplete composition exclusions')

    native = check_reference_c(submission, output, rng) if submission else {'executed': False}
    result = {
        'scope': 'Component arithmetic and finite certificates only',
        'universal_64_bit_classification_basis': 'Analytical proof in SUBCOLUMN_STRUCTURES.md; not a machine-checked proof',
        'sigma_binary_ranks': ranks,
        'addition_lemma_small_width_checks': addition,
        'T1_positive_comparisons': len(family) * len(bases),
        'inverse_comparisons': len(bases),
        'T2_msb_nonmember_certificates': exclusions,
        'C1_named_non_msb_certificates': other_certificates,
        'T3_T4_matrix_difference_comparisons_each': matrix_cases,
        'T5_nonmember_certificates': composition,
        'reference_c': native,
        'full_round_security_or_attack_claim': False,
    }
    (output / 'subcolumn_structures.json').write_text(json.dumps(result, indent=2) + '\n')
    print('Exact Sigma ranks: 64, 64; rotation and bit identities agree.')
    print('Two-/three-input addition: all masks classified at widths 2, 3, 4, including the width-2 exception.')
    print(f'T1: {len(family)*len(bases)} comparisons; inverse: {len(bases)} comparisons.')
    print('T2/C1: 12 MSB and 7 specified non-MSB candidates excluded by stored counterexamples.')
    print(f'T3/T4: {matrix_cases} full difference-map comparisons each.')
    print('T5: all 255 nonzero family members excluded at the second-layer boundary by stored counterexamples.')
    if submission:
        print(f"Reference C: {native['column_comparisons']} column and {native['half_round_comparisons']} half-round agreements.")
    print('COMPONENT CHECKS PASSED. Universal claims rely on the accompanying proof.')
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output-dir', type=Path, required=True)
    parser.add_argument('--submission-root', type=Path)
    args = parser.parse_args()
    output = args.output_dir.resolve()
    if output == PACKAGE or any(output.is_relative_to(PACKAGE / name)
                               for name in ('code', 'data', 'evidence', 'assets', 'LICENSES')):
        parser.error('Choose an output directory outside packaged sources and evidence')
    output.mkdir(parents=True, exist_ok=True)
    run(output, args.submission_root)
