#!/usr/bin/env python3
"""Read the two printed SubColumn examples from the hash-identified PDF.

This is a document-conformance check, not a differential search. Requires
pdftotext and a separately obtained copy of the original submission.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess

PDF_SHA256 = '8e3a9a109f3188ab57cbd0156c243f80a6453051cf98006dfef11d66bdeb5fa8'


def run(submission_root, output):
    pdf = submission_root / 'Algorithm specifications' / 'Specification.pdf'
    if hashlib.sha256(pdf.read_bytes()).hexdigest() != PDF_SHA256:
        raise ValueError('Specification differs from the reviewed PDF')
    text = subprocess.check_output(
        ['pdftotext', '-layout', '-f', '23', '-l', '23', str(pdf), '-'],
        text=True,
    )
    section = text.split('There are differentials of probability of 1 for it.', 1)[1]
    section = section.split('In addition, no preservation', 1)[0]
    rows = [re.findall(r'\b[08]000000000000000\b', line)
            for line in section.splitlines()]
    rows = [row for row in rows if row]
    if len(rows) != 4 or any(len(row) != 4 for row in rows):
        raise ValueError('Unexpected PDF extraction layout; inspect the rendered page')
    vectors = [list(column) for column in zip(*rows)]
    expected_input = ['0000000000000000', '8000000000000000'] * 2
    expected_output = ['8000000000000000', '0000000000000000'] * 2
    if vectors != [expected_input, expected_output, expected_input, expected_output]:
        raise ValueError('Printed differential examples differ from the recorded reading')
    result = {
        'scope': 'Fresh extraction of the two displayed examples; no hash attack or differential search',
        'specification_sha256': PDF_SHA256,
        'printed_page': 22,
        'pdf_page': 23,
        'examples': [{'input': vectors[i], 'output': vectors[i + 1]} for i in (0, 2)],
        'both_examples_identical': True,
        'reversed_example_printed': False,
    }
    output.mkdir(parents=True, exist_ok=True)
    (output / 'specification_examples.json').write_text(json.dumps(result, indent=2) + '\n')
    print('Both printed examples are identical: (0,M,0,M) -> (M,0,M,0).')
    print('The alleged reversed example is absent. Document check passed.')
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--submission-root', type=Path, required=True)
    parser.add_argument('--output-dir', type=Path, required=True)
    args = parser.parse_args()
    package = Path(__file__).resolve().parents[1]
    output = args.output_dir.resolve()
    if output == package or any(output.is_relative_to(package / name)
                               for name in ('code', 'data', 'evidence', 'assets', 'LICENSES')):
        parser.error('Choose a separate output directory outside packaged sources and evidence')
    run(args.submission_root.resolve(), output)
