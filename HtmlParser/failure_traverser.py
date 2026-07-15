# Traverses the HTML report to find all failures and their hierarchy for reporting purposes
from bs4 import BeautifulSoup

class FailureTraverser:
    def __init__(self):
        self.failure_set = set() # To remove any duplicate entries

    # Get the hierarchy of each failure to add to the report
    def get_full_hierarchy(self, failed_div):
        hierarchy = []

        current = failed_div
        while current:
            header = current.find('div', class_='header_Failed')
            if header:
                #hier_number = header.find('span', class_='tb_hierarchynumber')
                name = header.find('span', class_='tb_name') # test-step name
                library = header.find('span', class_='tb_library') # library used

                # Create a String with the affected test-step and library
                parts = []
                #if hier_number:
                #    parts.append(hier_number.get_text(strip=True))
                if name:
                    parts.append(name.get_text(strip=True))
                if library:
                    parts.append(library.get_text(strip=True))
                hierarchy.insert(0, ' '.join(parts)) # builds from bottom to top
            parent_failed = current.find_parent('div', class_='Failed') # returns None if no parent exists with div class Failed
            current = parent_failed

        # Exclude the first 3 entries since they are common to all failures and not relevant to the report
        return hierarchy[3:]

    def process_failed_div(self, failed_div):
        hierarchy = self.get_full_hierarchy(failed_div)
        reason = ' :: '.join(hierarchy)
        self.failure_set.add(reason)

    def traverse_failed_div(self, div):
        # Check for nested 'body-expanded', this indicates that there are more failures nested within this div
        nested_bodies = div.find_all('div', class_='body-expanded', recursive=False)
        if nested_bodies:
            for body in nested_bodies:
                nested_failed_divs = body.find_all('div', class_='Failed', recursive=False)
                for nf in nested_failed_divs:
                    self.traverse_failed_div(nf)
        else:
            self.process_failed_div(div)