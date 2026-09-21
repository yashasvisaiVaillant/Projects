# Traverses the HTML report to find all failures and their hierarchy for reporting purposes in failure_report_generator.py

class FailureTraverser:
    def __init__(self):
        self.failure_set = set()
        self.failure_steps = []

    # Get the hierarchy of each failure to add to the report
    def get_full_hierarchy(self, failed_div):
        hierarchy = []
        current = failed_div
        
        while current:
            header = current.find('div', class_='header_Failed')
            if header:
                name = header.find('span', class_='tb_name') # gives the test-step name
                #library = header.find('span', class_='tb_library') # gives the library used

                # Create a String with the affected test-step and library
                parts = []
                if name:
                    parts.append(name.get_text(strip=True))
                #if library: # Can be included if required
                    #parts.append(library.get_text(strip=True))
                hierarchy.insert(0, ' '.join(parts)) # builds the location of Failure (from bottom to top)
            parent_failed = current.find_parent('div', class_='Failed') # returns None if no parent exists with div class Failed
            current = parent_failed

        # Exclude the first 3 entries since they are common to all failures and not relevant to the report
        return hierarchy[3:]

    def traverse_failed_div(self, div):
        # Check for the attribute nested 'body-expanded'-> this indicates that there are more failures nested within
        nested_bodies = div.find_all('div', class_='body-expanded', recursive=False)
        if nested_bodies:
            for body in nested_bodies:
                nested_failed_divs = body.find_all('div', class_='Failed', recursive=False)
                for nf in nested_failed_divs:
                    self.traverse_failed_div(nf)
        else:
            # Process failure and get hierarchy
            hierarchy = self.get_full_hierarchy(div)
            # Store hierarchy for later use
            if not hasattr(self, 'hierarchies'):
                self.hierarchies = []
            self.hierarchies.append(hierarchy)
            reason = ' --> '.join(hierarchy)
            if reason not in self.failure_set:
                self.failure_set.add(reason)
                self.failure_steps.append(reason)