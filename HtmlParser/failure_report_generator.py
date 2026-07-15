# This script generates a failure report from an HTML file containing test results.

import os
import pandas as pd
from bs4 import BeautifulSoup
from failure_traverser import FailureTraverser
from ExcelFormatter import ExcelFormatter

class FailureReportGenerator:
    def __init__(self, html_file, output_file):
        self.html_file = html_file
        self.output_file = output_file

    def run(self):
        # Extract test name
        test_name = os.path.basename(os.path.dirname(self.html_file))
        # Detect encoding
        import chardet
        with open(self.html_file, 'rb') as f:
            rawdata = f.read()
        result = chardet.detect(rawdata)
        encoding = result['encoding']
        # Read HTML content
        with open(self.html_file, encoding=encoding) as f:
            html_content = f.read()

        # Parse HTML
        soup = BeautifulSoup(html_content, 'html.parser')

        # Find top-level 'Failed' divs
        failed_divs = soup.find_all('div', class_='Failed')

        traverser = FailureTraverser()

        for div in failed_divs:
            traverser.traverse_failed_div(div)

        print(f"Total unique failures recorded: {len(traverser.failure_set)}")  # Debug

        # Do not generate a report if there are no failures
        if not traverser.failure_set:
            print(f"No failures found in {self.html_file}. Skipping report generation.")
            return

        # Save failures to DataFrame
        df = pd.DataFrame({'Failure Step': list(traverser.failure_set)})
        df['Test Name'] = test_name
        df = df[['Test Name', 'Failure Step']]

        # Save to Excel
        df.to_excel(self.output_file, index=False)

        # Format the Excel file
        formatter = ExcelFormatter(self.output_file)
        formatter.adjust_columns()