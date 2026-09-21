import re


class FailureTraverser:
    def __init__(self):
        self._failure_steps = []

    def get_full_hierarchy(self, failed_div):
        hierarchy = []
        current = failed_div

        while current:
            header = current.find('div', class_='header_Failed')
            if header:
                name = header.find('span', class_='tb_name')
                if name:
                    hierarchy.insert(0, name.get_text(strip=True))
            current = current.find_parent('div', class_='Failed')

        # The outer sequence, test case, and phase are common report scaffolding.
        return hierarchy[3:]

    def traverse_failed_div(self, div):
        nested_bodies = div.find_all('div', class_='body-expanded', recursive=False)
        if nested_bodies:
            for body in nested_bodies:
                for nested_failure in body.find_all(
                    'div', class_='Failed', recursive=False
                ):
                    self.traverse_failed_div(nested_failure)
        else:
            hierarchy = self.get_full_hierarchy(div)
            self._failure_steps.append(' --> '.join(hierarchy))

    def get_failure_records(self, soup):
        # Detail blocks occur in the same document order as the overview leaves.
        decisions = soup.find_all('div', class_='FailedDecision')
        if len(decisions) != len(self._failure_steps):
            raise ValueError(
                'Failure steps and failure reasons could not be matched.'
            )

        records = []
        seen_steps = set()
        for step, decision in zip(self._failure_steps, decisions):
            if step in seen_steps:
                continue

            seen_steps.add(step)
            details = decision.find('div', recursive=False)
            # Remove invisible separators and volatile timestamps from diagnostics.
            detail_lines = [
                re.sub(r'^\([^)]*\)\s*', '', line.strip())
                for line in details.get_text('\n', strip=True)
                .replace('\u200b', '')
                .splitlines()
                if line.strip()
            ] if details else []
            if len(detail_lines) >= 2:
                reason = (
                    f'Expected: {detail_lines[0]}\n'
                    f'Actual: {" ".join(detail_lines[1:])}'
                )
            else:
                reason = f'Actual: {detail_lines[0]}' if detail_lines else ''

            records.append((step, reason))

        return records