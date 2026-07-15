# Generate a combined failure report from an HTML report file.

import argparse
from failure_report_generator import FailureReportGenerator

def main():
    parser = argparse.ArgumentParser(description='Generate failure report from HTML report file.')
    parser.add_argument('--html_file', type=str, required=True, help='Path to the input HTML report file.')
    parser.add_argument('--output_file', type=str, default='failure_report.xlsx', help='Path for the output Excel file.')
    args = parser.parse_args()

    generator = FailureReportGenerator(args.html_file, args.output_file)
    generator.run()

if __name__ == '__main__':
    main()