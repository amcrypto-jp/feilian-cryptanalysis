"""Check only the six ordinary Appendix B examples and their printed states.

The two counter conventions are compared on these fixed published examples.
This is a document-conformance check, not a general alternate hash interface.
"""
import json
import re
import subprocess
from inputs import PACKAGE, verify_submission
import model

EXAMPLES = (('abc', b'abc'), ('a_times_129', b'a' * 129))
CHECKPOINTS = (1, 2, 5, 10, 20)


def matrix_after(marker, text, transpose=False):
    values = re.findall(r'\b[0-9a-f]{16}\b', text.split(marker, 1)[1])[:16]
    if len(values) != 16:
        raise ValueError('Incomplete Appendix B matrix')
    # Only the initial IV display is transposed; computed states are row-major.
    return [values[(i % 4) * 4 + i // 4] for i in range(16)] if transpose else values


def extract(text):
    """Transcribe the fixed Appendix B examples into normalized numeric records."""
    result = {}
    for bits, number in ((1024, 1), (768, 2), (512, 3)):
        match = re.search(r'B\.' + str(number) + r'\s+FEILIAN-' + str(bits)
                          + r'([\s\S]*?)(?=B\.\d\s+FEILIAN|\Z)', text)
        if match is None:
            raise ValueError('Appendix section not found')
        parts = match.group(1).split('Two-block message:')
        if len(parts) != 2:
            raise ValueError('Expected two Appendix B examples')
        examples = []
        for index, ((name, _), part) in enumerate(zip(EXAMPLES, parts)):
            records = part.split('Initial state of v:')[1:]
            if len(records) != index + 1:
                raise ValueError('Unexpected Appendix B block count')
            values = re.findall(r'\b[0-9a-f]{16}\b', part.split('Hash digest output:', 1)[1])[:bits // 64]
            if len(values) != bits // 64:
                raise ValueError('Incomplete Appendix B digest')
            blocks = []
            for block_index, record in enumerate(records):
                blocks.append({
                    'initial': matrix_after('Initial state of v:', 'Initial state of v:' + record,
                                            transpose=block_index == 0),
                    'rounds': {str(n): matrix_after(
                        f'State v after {n} ' + ('round:' if n == 1 else 'rounds:'), record)
                        for n in CHECKPOINTS}})
            examples.append({'message': name, 'printed_digest': ''.join(values), 'blocks': blocks})
        result[str(bits)] = examples
    return result


def words(values):
    return tuple(int(value, 16) for value in values)


def run(output, submission_root=None):
    stored = json.loads((PACKAGE / 'data/appendix_states.json').read_text())
    prior = json.loads((PACKAGE / 'data/appendix_examples.json').read_text())
    if submission_root is not None:
        root, _ = verify_submission(submission_root)
        extracted = subprocess.check_output(
            ['pdftotext', '-layout', str(root / 'Algorithm specifications/Specification.pdf'), '-'],
            text=True)
        if extract(extracted) != stored:
            raise RuntimeError('Stored Appendix B data differs from the pinned PDF')
    result = {'printed_values_checked_against_pdf': submission_root is not None,
              'variants': {}, 'recovered_domains': [],
              'verified_totals': {'digests': 0, 'initial_states': 0, 'round_snapshots': 0, 'domains': 0}}
    for bits in (1024, 768, 512):
        rows = []
        for index, (name, message) in enumerate(EXAMPLES):
            example = stored[str(bits)][index]
            old = prior[str(bits)][index]
            if example['message'] != name or example['printed_digest'] != old['printed_digest']:
                raise RuntimeError('Inconsistent stored example identity')
            data = message + bytes((-len(message)) % 128)
            block_count = len(data) // 128
            if len(example['blocks']) != block_count:
                raise RuntimeError('Incorrect stored block count')
            expected_profile = 'true' if bits == 1024 else 'padded'
            profiles = {}
            for profile in ('true', 'padded'):
                h = model.IV_C
                matched_initial = matched_rounds = 0
                counts = []
                for block_index, record in enumerate(example['blocks']):
                    initial = words(record['initial'])
                    matched_initial += h == initial
                    block = data[128 * block_index:128 * (block_index + 1)]
                    message_words = tuple(int.from_bytes(block[i:i+8], 'little') for i in range(0, 128, 8))
                    final = block_index == block_count - 1
                    count = (min(1024 * (block_index + 1), len(message) * 8)
                             if profile == 'true' else 1024 * (block_index + 1))
                    counts.append(count)
                    tweak = (bits, model.MASK if final else 0, 0, count)
                    v = list(h)
                    for rnd in range(20):
                        for half in range(2):
                            if rnd % 4 == 0:
                                for col in range(4):
                                    v[col] ^= message_words[8 * half + col]
                                    v[8 + col] ^= message_words[8 * half + 4 + col]
                            v = model.half_round(v)
                        for col in range(4):
                            v[4 + col] ^= model.CONSTANTS[(rnd // 4 + col) % 4]
                        if rnd == 0 and profile == expected_profile:
                            residual = tuple(a ^ b for a, b in zip(v, words(record['rounds']['1'])))
                            if any(residual[:12]) or residual[12:] != tweak:
                                raise RuntimeError('Recovered domain differs from the expected assignment')
                            result['recovered_domains'].append({
                                'variant': bits, 'example': name, 'block': block_index + 1,
                                'domain': [f'{x:016x}' for x in residual[12:]],
                                'counter_bits': (residual[14] << 64) + residual[15]})
                        for col in range(4):
                            v[12 + col] ^= tweak[col]
                        if rnd + 1 in CHECKPOINTS:
                            matched_rounds += tuple(v) == words(record['rounds'][str(rnd + 1)])
                    calculated = tuple(a ^ b for a, b in zip(h, v))
                    if calculated != model.compress(h, message_words, bits, final, count, 'c'):
                        raise RuntimeError('Tracing and validated compression disagree')
                    h = calculated
                digest = b''.join(x.to_bytes(8, 'little') for x in h)[:bits // 8].hex()
                matches = digest == example['printed_digest']
                if matches != (profile == expected_profile):
                    raise RuntimeError('Unexpected variant-to-counter-profile assignment')
                if profile == 'true' and digest != model.hash_model(message, len(message) * 8, bits).hex():
                    raise RuntimeError('Ordinary C-profile model mismatch')
                if matches:
                    if matched_initial != block_count or matched_rounds != 5 * block_count:
                        raise RuntimeError('An Appendix B state disagrees')
                    result['verified_totals']['digests'] += 1
                    result['verified_totals']['initial_states'] += matched_initial
                    result['verified_totals']['round_snapshots'] += matched_rounds
                profiles[profile] = {'counter_bits': counts, 'digest': digest, 'digest_matches': matches,
                                     'initial_states_matched': matched_initial,
                                     'round_snapshots_matched': matched_rounds}
            c_digest = profiles['true']['digest']
            if c_digest != old['c_digest'] or (c_digest == example['printed_digest']) != old['matches']:
                raise RuntimeError('Original ordinary digest comparison changed')
            rows.append({'message': name, 'printed_digest': example['printed_digest'], 'c_digest': c_digest,
                         'matches': profiles['true']['digest_matches'],
                         'matched_counter_profile': expected_profile, 'profiles': profiles})
            print(f'Appendix B: {bits}, {name}: {expected_profile} count; all printed states agree.')
        result['variants'][str(bits)] = rows
    result['verified_totals']['domains'] = len(result['recovered_domains'])
    if result['verified_totals'] != {'digests': 6, 'initial_states': 9, 'round_snapshots': 45, 'domains': 9}:
        raise RuntimeError('Incomplete Appendix B coverage')
    (output / 'appendix_comparison.json').write_text(json.dumps(result, indent=2) + '\n')
    print('Appendix B: 6 digests, 9 initial states, 45 round snapshots and 9 domains verified.')
    return result
