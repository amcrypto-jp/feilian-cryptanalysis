"""Exact component and constant checks; SageMath, no submission files needed."""
import json
import os
from pathlib import Path

output = Path(os.environ.get('FEILIAN_REVIEW_OUTPUT', 'verification-sage/arithmetic.json'))
R = PolynomialRing(GF(2), 'x')
x = R.gen()
modulus = x**64 + 1
checks = {}
for name, exponents in [('sigma0', (0, 5, 48)), ('sigma1', (0, 11, 40))]:
    polynomial = sum(x**i for i in exponents)
    gcd = polynomial.gcd(modulus)
    fixed_gcd = (polynomial + 1).gcd(modulus)
    if gcd != 1 or fixed_gcd.degree() != 1:
        raise RuntimeError('Unexpected Sigma arithmetic result')
    checks[name] = {'polynomial': str(polynomial), 'gcd_with_word_modulus': str(gcd),
                    'linear_rank': int(64 - gcd.degree()),
                    'fixed_space_dimension': int(fixed_gcd.degree())}
scaled = (RealIntervalField(1400)(pi) - 3) * Integer(16)**256
lo, hi = scaled.lower().floor(), scaled.upper().floor()
if lo != hi:
    raise RuntimeError('Precision insufficient to certify pi digits')
digits = format(int(lo), '0256x')
words = [digits[i:i+16] for i in range(0, 256, 16)]
expected = ('243f6a8885a308d3 13198a2e03707344 a4093822299f31d0 082efa98ec4e6c89 '
            '452821e638d01377 be5466cf34e90c6c c0ac29b7c97c50dd 3f84d5b5b5470917 '
            '9216d5d98979fb1b d1310ba698dfb5ac 2ffd72dbd01adfb7 b8e1afed6a267e96 '
            'ba7c9045f12c7f99 24a19947b3916cf7 0801f2e2858efc16 636920d871574e69').split()
roots = [format(int((Integer(p) << 128).isqrt() % (Integer(1) << 64)), '016x') for p in [2, 3, 5, 7]]
if words != expected or roots != ['6a09e667f3bcc908', 'bb67ae8584caa73b', '3c6ef372fe94f82b', 'a54ff53a5f1d36f1']:
    raise RuntimeError('Unexpected constant derivation')
checks['pi_fraction_first_16_words'] = words
checks['sqrt_fraction_first_64_bits'] = roots
checks['modulus_factorization'] = str(modulus.factor())
output.parent.mkdir(parents=True, exist_ok=True)
output.write_text(json.dumps(checks, indent=2) + '\n')
print(json.dumps(checks, indent=2))
