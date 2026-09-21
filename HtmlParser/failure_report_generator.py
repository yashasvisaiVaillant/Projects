from pathlib import Path

from bs4 import BeautifulSoup
from ExcelReportGenerator import ExcelReportGenerator
from failure_traverser import FailureTraverser


class FailureReportGenerator:
    def __init__(self, html_file, output_file):
        self.html_file = html_file
        self.output_file = output_file

    def run(self):
        html_path = Path(self.html_file).resolve()
        test_name = html_path.parent.name
        main_report = html_path.parent / f'{test_name}.html'
        if not main_report.exists():
            raise FileNotFoundError(f'Main report not found: {main_report}')

        # BeautifulSoup detects the BOM or declared encoding when given raw bytes.
        soup = BeautifulSoup(html_path.read_bytes(), 'html.parser')
        # Start only at roots; the traverser recursively visits failed/error nodes.
        result_divs = [
            div for div in soup.find_all(
                'div', class_=FailureTraverser.RESULT_STATES
            )
            if div.find_parent(
                'div', class_=FailureTraverser.RESULT_STATES
            ) is None
        ]

        traverser = FailureTraverser()
        for div in result_divs:
            traverser.traverse_failed_div(div)

        result_type, failures = traverser.get_failure_records(soup)
        failure_count = len(failures)
        print(f"Total unique failures recorded: {failure_count}")

        if failure_count == 0:
            print(f"No failures found in {self.html_file}. Skipping report generation.")
            return False

        excel_report = ExcelReportGenerator(self.output_file)
        excel_report.generate(test_name, result_type, failures, main_report)
        print(f"Excel report written to: {self.output_file}")
        return True