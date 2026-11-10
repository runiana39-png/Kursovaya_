"""CLI for checking migration milestones from a JSON input."""
import argparse
import json
from pathlib import Path
from .core import Progress, export_json


def main() -> None:
    parser = argparse.ArgumentParser(description='IDE migration checklist')
    parser.add_argument('input', type=Path, help='JSON file with [{code, done}]')
    parser.add_argument('--output', type=Path, help='Optional report path')
    args = parser.parse_args()
    items = json.loads(args.input.read_text(encoding='utf-8'))
    if not isinstance(items, list):
        raise ValueError('Expected JSON array')
    report = export_json([Progress(**row) for row in items])
    if args.output:
        args.output.write_text(report, encoding='utf-8')
    print(report)

if __name__ == '__main__':
    main()
