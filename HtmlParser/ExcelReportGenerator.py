from openpyxl import Workbook, load_workbook
from openpyxl.styles import Alignment, Font
from openpyxl.utils import get_column_letter


class ExcelReportGenerator:
    def __init__(self, output_file):
        self.output_file = output_file

    def generate(self, test_name, failure_steps):
        rows = [[test_name, failure_steps[0]]]
        rows.extend(['', step] for step in failure_steps[1:])

        workbook = Workbook()
        worksheet = workbook.active
        worksheet.title = "Failures"

        worksheet.append(["Test Name", "Failure Step"])
        for cell in worksheet[1]:
            cell.font = Font(bold=True)

        for row in rows:
            worksheet.append(row)

        column_widths = {}
        for row in worksheet.iter_rows(values_only=True):
            for column_index, value in enumerate(row, start=1):
                length = len(str(value)) if value is not None else 0
                column_widths[column_index] = max(
                    length, column_widths.get(column_index, 0)
                )

        for column_index, width in column_widths.items():
            column_letter = get_column_letter(column_index)
            worksheet.column_dimensions[column_letter].width = min(width + 2, 80)

        workbook.save(self.output_file)


class ExcelFormatter:
    def __init__(self, filename):
        self.filename = filename

    def merge_test_name_rows(self):
        workbook = load_workbook(self.filename)
        worksheet = workbook.active
        group_start = None

        for row_index in range(2, worksheet.max_row + 1):
            test_name = worksheet.cell(row=row_index, column=1).value
            if test_name not in (None, ''):
                if group_start is not None:
                    self._merge_test_name_group(
                        worksheet, group_start, row_index - 1
                    )
                group_start = row_index

        if group_start is not None:
            self._merge_test_name_group(
                worksheet, group_start, worksheet.max_row
            )

        workbook.save(self.filename)

    @staticmethod
    def _merge_test_name_group(worksheet, start_row, end_row):
        if end_row > start_row:
            worksheet.merge_cells(
                start_row=start_row,
                start_column=1,
                end_row=end_row,
                end_column=1
            )

        worksheet.cell(row=start_row, column=1).alignment = Alignment(
            vertical='center',
            wrap_text=True
        )

    def adjust_columns(self):
        workbook = load_workbook(self.filename)
        worksheet = workbook.active

        for column_index, column_cells in enumerate(
            worksheet.columns, start=1
        ):
            max_length = 0
            column_letter = get_column_letter(column_index)
            for cell in column_cells:
                cell.alignment = Alignment(wrap_text=True)
                if cell.value:
                    max_length = max(max_length, len(str(cell.value)))

            worksheet.column_dimensions[column_letter].width = max_length + 2

        workbook.save(self.filename)
