from bs4 import BeautifulSoup
import chardet

# Load your HTML content from a file
html_file = r"reports\HPAD-12832_E4_GSHP_HMI_BasicCommissioning\HPAD-12832_E4_GSHP_HMI_BasicCommissioning_data.html"

# detect file encoding
with open(html_file, 'rb') as file:
    rawdata = file.read()

result = chardet.detect(rawdata)
encoding = result['encoding']


with open(html_file, encoding=encoding) as file:
    html_content = file.read()

# Parse the HTML content
soup = BeautifulSoup(html_content, 'html.parser')

# Find all divs with class 'FailedDecision'
failed_decisions = soup.find_all('div', class_='FailedDecision')

# Save each extracted section to a separate file or print them
for i, div in enumerate(failed_decisions, start=1):
    # Pretty print the extracted div
    print(f"FailedDecision #{i}:\n{div.prettify()}\n")
    # Optionally, save to individual files
    # with open(f'failed_decision_{i}.html', 'w', encoding='utf-8') as f:
    #     f.write(str(div))