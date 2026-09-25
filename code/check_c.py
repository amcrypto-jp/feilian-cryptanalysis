"""Ordinary short-message KAT comparison with the hash-verified C submission."""
from pathlib import Path
import ctypes
import json
import platform
import re
import shutil
import subprocess
import tempfile
from inputs import verify_submission
from model import hash_model

LENGTHS = (0, 1, 7, 8, 9, 63, 64, 65, 511, 512, 513,
           1016, 1023, 1024, 1025, 1031, 1032, 2047, 2048, 4096)


def load_kats(root, bits):
    text = (root / 'Test_Vectors' / f'KAT_2_12_FEILIAN{bits}.txt').read_text()
    matches = re.findall(r'Msg_Len = (\d+)\s*\nMsg = ([0-9A-F]*)\s*\n'
                         r'Dst_Len = (\d+)\s*\nDst = ([0-9A-F]+)', text)
    if len(matches) != 4097:
        raise ValueError('Expected 4097 short KATs')
    records = []
    for index, (length, message, output_bits, digest) in enumerate(matches):
        if int(length) != index or int(output_bits) != bits:
            raise ValueError('Unexpected KAT ordering or output size')
        msg, expected = bytes.fromhex(message), bytes.fromhex(digest)
        if len(msg) < (index + 7) // 8 or len(expected) != bits // 8:
            raise ValueError('Unexpected KAT encoding length')
        if index % 8 and msg[index // 8] & ((1 << (8 - index % 8)) - 1):
            raise ValueError('Noncanonical KAT final byte')
        records.append((index, msg, expected))
    return records


def build(root, temp, bits, simd, compiler, output):
    kind = 'Optimized_Implementation' if simd else 'Reference_Implementation'
    name = ('FEILIAN_SIMD' if simd else 'FEILIAN') + str(bits)
    source_dir = root / 'Implementations' / kind / name
    target = temp / (name + '.so')
    command = [compiler, '-std=c99', '-O2', '-shared', '-fPIC', '-Wall', '-Wextra',
               '-Wconversion', '-Wshadow']
    if simd:
        command.append('-mavx2')
    command += ['CryptHash_AlgorithmInstance.c', '-o', str(target)]
    result = subprocess.run(command, cwd=source_dir, capture_output=True, text=True)
    log = (result.stdout + result.stderr).replace(str(root), '<submission>').replace(str(temp), '<build>')
    (output / (name + '_build.log')).write_text(log)
    result.check_returncode()
    library = ctypes.CDLL(str(target))
    library.CryptHash.argtypes = (ctypes.c_int, ctypes.c_void_p, ctypes.c_ulonglong,
                                 ctypes.c_void_p)
    library.CryptHash.restype = ctypes.c_int
    return library


def hash_c(library, message, bits, digest_bits):
    if not 0 <= bits <= 4096 or bits > 8 * len(message):
        raise ValueError('The review driver accepts short, well-formed inputs only')
    if bits % 8 and message[bits // 8] & ((1 << (8 - bits % 8)) - 1):
        raise ValueError('Expected canonical final byte')
    buffer = ctypes.create_string_buffer(message or b'\0')
    digest = (ctypes.c_ubyte * (digest_bits // 8))()
    status = library.CryptHash(digest_bits, buffer, bits, digest)
    if status != 0:
        raise RuntimeError(f'Canonical hash request returned {status}')
    return bytes(digest)


def run(submission_root, output, cc='gcc', simd='auto'):
    root, count = verify_submission(submission_root)
    compiler = shutil.which(cc)
    if compiler is None:
        raise RuntimeError(f'Compiler not found: {cc}')
    if platform.system() != 'Linux':
        raise RuntimeError('This shared-library driver currently targets Linux')
    cpu_file = Path('/proc/cpuinfo')
    avx2 = (platform.machine() in ('x86_64', 'AMD64') and cpu_file.is_file()
            and re.search(r'\bavx2\b', cpu_file.read_text()) is not None)
    use_simd = avx2 and simd == 'auto'
    result = {'environment': {'python': platform.python_version(), 'system': platform.system(),
                              'machine': platform.machine(),
                              'compiler': subprocess.check_output([compiler, '--version'], text=True).splitlines()[0]},
              'original_files_verified': count, 'simd_executed': use_simd,
              'scope': 'Canonical short-message KATs and ordinary examples only', 'variants': {}}
    print(f'Original file hashes verified: {count}. SIMD enabled: {use_simd}.')
    with tempfile.TemporaryDirectory(prefix='feilian-conformance-') as build_dir:
        temp = Path(build_dir)
        for bits in (512, 768, 1024):
            scalar = build(root, temp, bits, False, compiler, output)
            vector = build(root, temp, bits, True, compiler, output) if use_simd else None
            kat = load_kats(root, bits)
            for length, message, expected in kat:
                if hash_c(scalar, message, length, bits) != expected:
                    raise RuntimeError(f'Scalar KAT mismatch: {bits}, {length}')
                if vector and hash_c(vector, message, length, bits) != expected:
                    raise RuntimeError(f'SIMD KAT mismatch: {bits}, {length}')
            for length in LENGTHS:
                if hash_model(kat[length][1], length, bits) != kat[length][2]:
                    raise RuntimeError(f'Independent model KAT mismatch: {bits}, {length}')
            examples = {}
            for name, message in [('empty', b''), ('abc', b'abc'), ('a_times_129', b'a' * 129)]:
                digest = hash_c(scalar, message, 8 * len(message), bits)
                if digest != hash_model(message, 8 * len(message), bits):
                    raise RuntimeError('Ordinary example model mismatch')
                examples[name] = digest.hex()
            result['variants'][str(bits)] = {
                'scalar_kats_passed': len(kat), 'simd_kats_passed': len(kat) if vector else None,
                'independent_model_lengths': list(LENGTHS), 'independent_model_passed': len(LENGTHS),
                'ordinary_examples': examples}
            print(f'{bits}: scalar 4097/4097; SIMD ' + ('4097/4097' if vector else 'skipped') + '; model 20/20.', flush=True)
    (output / 'c_conformance.json').write_text(json.dumps(result, indent=2) + '\n')
    return result
