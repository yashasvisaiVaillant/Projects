import argparse
import csv
import sys


REPORTABLE_VERDICTS = {'TestVerdict.Failed', 'TestVerdict.Error'}
PASSED_VERDICT = 'TestVerdict.Passed'


def load_test_verdicts(csv_file):
    with open(csv_file, newline='', encoding='utf-8-sig') as file:
        reader = csv.DictReader(file)
        required_columns = {'title', 'verdict'}
        if not reader.fieldnames or not required_columns.issubset(
            reader.fieldnames
        ):
            raise ValueError(
                f'CSV must contain these columns: {sorted(required_columns)}'
            )

        return {
            row['title'].strip(): row['verdict'].strip()
            for row in reader
            if row['title'].strip()
        }


def main():
    parser = argparse.ArgumentParser(
        description='Check whether a test result should be parsed.'
    )
    parser.add_argument('--csv_file', required=True)
    parser.add_argument('--test_name', required=True)
    args = parser.parse_args()

    try:
        verdict = load_test_verdicts(args.csv_file).get(args.test_name)
        if verdict == PASSED_VERDICT:
            print(f'{args.test_name}: Passed')
            return 1
        if verdict in REPORTABLE_VERDICTS:
            print(f'{args.test_name}: {verdict.removeprefix("TestVerdict.")}')
            return 0

        print(
            f'No supported verdict found for test: {args.test_name}',
            file=sys.stderr
        )
        return 2
    except (OSError, ValueError) as error:
        print(f'Unable to read test results: {error}', file=sys.stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
