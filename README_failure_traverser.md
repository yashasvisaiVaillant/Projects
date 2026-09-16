**1. __init__ :**
Initializes self.failure_set as a set to store unique failure reasons.

**2. get_full_hierarchy(failed_div) :**
Builds a list (hierarchy) representing the hierarchy of a failure by traversing parent div elements with class 'Failed'.
For each failed_div, it:
Finds a child div with class 'header_Failed'.
Extracts test-step name (span.tb_name) and library (span.tb_library).
Combines these parts into a string and inserts at the beginning of hierarchy (bottom-up building).
After traversal, it discards the first 3 entries (return hierarchy[3:]), assuming these are common or irrelevant.

**3. process_failed_div(failed_div) :**
Calls get_full_hierarchy to get the hierarchy list.
Joins the hierarchy with ' :: ' to form a reason string.
Adds this reason to self.failure_set.

**4. traverse_failed_div(div) :**
Checks for nested failures within the current div.
If nested 'div.body-expanded' exists:
Recursively traverses each nested 'div.Failed'.
Else:
Calls process_failed_div(div) to process the current failure.


**Summary :**
The class walks through the HTML structure, capturing failure reasons with their context.
Handles nested failures via recursion.
Stores unique failure reasons, avoiding duplicates.
