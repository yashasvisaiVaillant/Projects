import os
import argparse
import pandas as pd
from bs4 import BeautifulSoup
import chardet
from ExcelFormatter import ExcelFormatter

def get_full_hierarchy(failed_div):
    hierarchy = []

    current = failed_div
    while current:
        header = current.find('div', class_='header_Failed')
        if header:
            # Find parts, excluding hierarchy number and test name
            name = header.find('span', class_='tb_name')
            library = header.find('span', class_='tb_library')

            parts = []
            if name:
                parts.append(name.get_text(strip=True))
            if library:
                parts.append(library.get_text(strip=True))
            # Insert at start to maintain root-to-leaf order
            hierarchy.insert(0, ' '.join(parts))
        parent_failed = current.find_parent('div', class_='Failed')
        current = parent_failed
    return hierarchy

def process_failed_div(failed_div, failure_set):
    hierarchy = get_full_hierarchy(failed_div)
    # Find index of 'Modbus Monitor' and slice
    try:
        index = hierarchy.index('Modbus Monitor')
        # Slice from after 'Modbus Monitor'
        sliced_hierarchy = hierarchy[index + 1:]
    except ValueError:
        # 'Modbus Monitor' not found, use full hierarchy
        sliced_hierarchy = hierarchy

    reason = ' :: '.join(sliced_hierarchy)
    failure_set.add(reason)

def traverse_failed_div(div, failure_set):
    """
    Process a 'Failed' div:
    - If it has nested 'body-expanded', recurse into it.
    - Else, process it directly.
    """
    # Check for nested 'body-expanded'
    nested_bodies = div.find_all('div', class_='body-expanded', recursive=False)
    if nested_bodies:
        # Recurse into each nested body
        for body in nested_bodies:
            # Find all 'Failed' divs directly under this body
            nested_failed_divs = body.find_all('div', class_='Failed', recursive=False)
            for nf in nested_failed_divs:
                traverse_failed_div(nf, failure_set)
    else:
        # No nested body, process this failed div
        process_failed_div(div, failure_set)

def main():
    parser = argparse.ArgumentParser(description='Generate failure report from HTML report file.')
    parser.add_argument('--html_file', type=str, required=True, help='Path to the input HTML report file.')
    parser.add_argument('--output_file', type=str, default='failure_report.xlsx', help='Path for the output Excel file.')
    args = parser.parse_args()

    html_file = args.html_file
    output_file = args.output_file

    # Extract test name
    test_name = os.path.basename(os.path.dirname(html_file))

    # Detect encoding
    with open(html_file, 'rb') as f:
        rawdata = f.read()
    result = chardet.detect(rawdata)
    encoding = result['encoding']

    # Read HTML
    with open(html_file, encoding=encoding) as f:
        html_content = f.read()

    soup = BeautifulSoup(html_content, 'html.parser')

    # Find top-level 'Failed' divs
    failed_divs = soup.find_all('div', class_='Failed')
    print(f"Found {len(failed_divs)} top-level 'Failed' divs.")  # Debug

    failure_set = set()

    # Process each top-level 'Failed' div
    for div in failed_divs:
        traverse_failed_div(div, failure_set)

    print(f"Total failures recorded: {len(failure_set)}")  # Debug

    # Save all failures
    df = pd.DataFrame({'Failure Reason': list(failure_set)})
    df['Test Name'] = test_name
    df = df[['Test Name', 'Failure Reason']]

    df.to_excel(output_file, index=False)

    # Format the Excel file
    formatter = ExcelFormatter(output_file)
    formatter.adjust_columns()

if __name__ == '__main__':
    main()