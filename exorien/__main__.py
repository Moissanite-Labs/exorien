"""Read one local encounter JSON document and print an auditable result."""
import argparse
import json
import sys
from pathlib import Path
from .grounding import InvalidEncounter, compare


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('encounter', type=Path)
    args = parser.parse_args()
    try:
        data = json.loads(args.encounter.read_text(encoding='utf-8'))
        result = compare(data)
    except (OSError, UnicodeError, ValueError) as exc:
        print(f'exorien: {exc}', file=sys.stderr)
        return 2
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if result['status'] == 'comparable' else 1


if __name__ == '__main__':
    sys.exit(main())
