"""Canonical examples and component checks, requiring only Python 3.11+."""
import json
import platform
import random
from inputs import PACKAGE
from model import hash_model, inverse_subcolumn, linear_rank, subcolumn, sigma0, sigma1


def run(output):
    stored = json.loads((PACKAGE / 'data/ordinary_vectors.json').read_text())
    messages = {'empty': b'', 'abc': b'abc', 'a_times_129': b'a' * 129}
    results = {'python': platform.python_version(), 'ordinary_examples': [],
               'scope': 'Canonical examples and component checks; no security-complexity claim'}
    for bits, examples in stored['variants'].items():
        for name, expected in examples.items():
            message = messages[name]
            calculated = {profile: hash_model(message, 8 * len(message), int(bits), profile).hex()
                          for profile in ('c', 'chapter2')}
            for profile in calculated:
                if calculated[profile] != expected[profile]:
                    raise RuntimeError(f'Example mismatch: {bits}, {name}, {profile}')
            results['ordinary_examples'].append({'bits': int(bits), 'message': name,
                                                'digests': calculated})
    rng = random.Random(20260924)
    for _ in range(10000):
        words = tuple(rng.getrandbits(64) for _ in range(4))
        if inverse_subcolumn(*subcolumn(*words)) != words:
            raise RuntimeError('SubColumn inverse mismatch')
    ranks = [linear_rank(sigma0), linear_rank(sigma1)]
    if ranks != [64, 64]:
        raise RuntimeError('Sigma rank mismatch')
    results['components'] = {'subcolumn_inverse_pass': 10000,
                             'sigma0_rank': ranks[0], 'sigma1_rank': ranks[1]}
    (output / 'quick.json').write_text(json.dumps(results, indent=2) + '\n')
    print('Quick checks: 9 ordinary examples in each of 2 profiles; 10000 inverse checks; ranks 64, 64.')
    return results
