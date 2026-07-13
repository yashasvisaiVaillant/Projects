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

# Initialize a list to hold concatenated strings
concatenated_list = []

# Skip the first 4 and process the rest
for i, div in enumerate(failed_decisions[4:], start=5):  # start=5 to reflect actual position
    header_div = div.find('div', class_='header_Failed')
    if header_div:
        # Extract tb_name
        tb_name_span = header_div.find('span', class_='tb_name')
        tb_name = tb_name_span.get_text(strip=True) if tb_name_span else None

        # Extract tb_library
        tb_library_span = header_div.find('span', class_='tb_library')
        tb_library = tb_library_span.get_text(strip=True) if tb_library_span else None

        # Append to list if available
        if tb_name and tb_library:
            concatenated_list.append(f"{tb_name}.{tb_library}")
        elif tb_name:
            concatenated_list.append(f"{tb_name}")
        elif tb_library:
            concatenated_list.append(f"{tb_library}")
        # If neither is available, skip
    else:
        continue

# Join all entries into a single string separated by commas (or any separator you prefer)
result_string = ' :: '.join(concatenated_list)

print("The failure occurs at:", result_string)