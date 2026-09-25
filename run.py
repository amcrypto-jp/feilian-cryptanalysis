#!/usr/bin/env python3
"""Run the FEILIAN review's ordinary conformance and component checks."""
import argparse
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / 'code'))
from check_quick import run as quick
from check_c import run as c_checks
from check_appendix import run as appendix


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--mode', choices=('quick', 'c', 'all'), default='quick')
    parser.add_argument('--submission-root', type=Path)
    parser.add_argument('--output-dir', type=Path, default=Path('verification-results'))
    parser.add_argument('--cc', default='gcc')
    parser.add_argument('--simd', choices=('auto', 'off'), default='auto')
    args = parser.parse_args()
    if args.mode in ('c', 'all') and args.submission_root is None:
        parser.error('--submission-root is required for mode c or all')
    output = args.output_dir.expanduser().resolve()
    for protected in (ROOT / 'data', ROOT / 'code', ROOT / 'assets', ROOT / 'evidence', ROOT / 'LICENSES'):
        if output == ROOT or output.is_relative_to(protected):
            parser.error('Choose an output directory outside the packaged evidence and source directories')
    output.mkdir(parents=True, exist_ok=True)
    if args.mode in ('quick', 'all'):
        quick(output)
        appendix(output, args.submission_root if args.mode == 'all' else None)
    if args.mode in ('c', 'all'):
        c_checks(args.submission_root, output, args.cc, args.simd)
    print('Requested checks completed successfully. Results are in the chosen output directory.')


if __name__ == '__main__':
    main()
