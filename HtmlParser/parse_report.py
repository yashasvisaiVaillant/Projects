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

# Find all divs with class 'Failed'
failed_decisions = soup.find_all('div', class_='Failed')

# Loop through each 'Failed' div and extract relevant info
# Skip the first 5 since they are common to all results and process the rest
for i, div in enumerate(failed_decisions[5:], start=6):  # start=6 to reflect actual position
    # Find the 'header_Failed' div inside the current div
    header_div = div.find('div', class_='header_Failed')
    if header_div:
        # Extract tb_name
        tb_name_span = header_div.find('span', class_='tb_name')
        tb_name = tb_name_span.get_text(strip=True) if tb_name_span else None

        # Extract tb_library
        tb_library_span = header_div.find('span', class_='tb_library')
        tb_library = tb_library_span.get_text(strip=True) if tb_library_span else None

        print(f"FailedDecision #{i}:")
        print(f"  tb_name: {tb_name}")
        print(f"  tb_library: {tb_library}\n")
    else:
        print(f"FailedDecision #{i}: header_Failed div not found.\n")