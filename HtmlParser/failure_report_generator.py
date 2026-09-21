# This script generates a failure report from an HTML file containing test results.

import os
from bs4 import BeautifulSoup
from ExcelReportGenerator import ExcelReportGenerator
from failure_traverser import FailureTraverser


def read_html_with_detected_encoding(path): 
    # Encoding robustness: Why it’s needed:
    # It was observed that some of the Test data HTML files came in different encodings (UTF‑8, UTF‑16)
    # This can raise UnicodeDecodeError or silently corrupt characters.
    # A robust approach tries detection first, then falls back safely.
    
    # Read raw bytes 
    with open(path, 'rb') as f: 
        raw = f.read()
    # Try chardet if available
    enc = None
    try:
        import chardet
        info = chardet.detect(raw) or {}
        enc = info.get('encoding')
    except Exception:
        enc = None

    # Try detected encoding strictly; on error, fall back
    if enc:
        try:
            return raw.decode(enc, errors='strict')
        except Exception:
            pass

    # Try BOM-aware UTF-8 first
    try:
        return raw.decode('utf-8-sig', errors='strict')
    except Exception:
        # Final fallback that never fails (may replace undecodable bytes)
        return raw.decode('utf-8', errors='replace')

    
class FailureReportGenerator:
    def __init__(self, html_file, output_file):
        self.html_file = html_file
        self.output_file = output_file

    def run(self):
        # Extract test name from parent folder of the HTML file
        test_name = os.path.basename(os.path.dirname(os.path.abspath(self.html_file)))

        # Read HTML content (robust decoding)
        html_content = read_html_with_detected_encoding(self.html_file)

        # Parse HTML
        soup = BeautifulSoup(html_content, 'html.parser')

        # Find all 'div' elements with class 'Failed' anywhere in the document
        failed_divs = soup.find_all('div', class_='Failed')

        traverser = FailureTraverser()
        for div in failed_divs:
            traverser.traverse_failed_div(div)

        print(f"Total unique failures recorded: {len(traverser.failure_set)}")

        # Do not generate a report if there are no failures
        if not traverser.failure_set:
            print(f"No failures found in {self.html_file}. Skipping report generation.")
            return False
            
        # Build sorted list of failure steps
        steps = sorted(
            traverser.failure_set,
            key=lambda s: s.casefold() if isinstance(s, str) else str(s).casefold()
        )

        excel_report = ExcelReportGenerator(self.output_file)
        excel_report.generate(test_name, steps)
        print(f"Excel report written to: {self.output_file}")
        return True