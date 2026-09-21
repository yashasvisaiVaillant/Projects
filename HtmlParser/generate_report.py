import argparse
import sys
from failure_report_generator import FailureReportGenerator


def main():
    parser = argparse.ArgumentParser(description='Generate failure report from HTML report file.')
    parser.add_argument('--html_file', type=str, required=True, help='Path to the input HTML report file.')
    parser.add_argument('--output_file', type=str, default='failure_report.xlsx', help='Path for the output Excel file.')
    parser.add_argument(
        '--report_root',
        help='Canonical shared folder containing the test report folders.'
    )
    args = parser.parse_args()

    generator = FailureReportGenerator(
        args.html_file,
        args.output_file,
        args.report_root
    )
    try:
        created = generator.run()
        if created:
            print("Report created.")
        else:
            print("No failures; report not created.")
        return 0
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

if __name__ == '__main__':
    sys.exit(main())
