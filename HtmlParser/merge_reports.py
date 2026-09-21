import argparse
import os
from openpyxl import Workbook, load_workbook
from openpyxl.styles import Font
from ExcelReportGenerator import ExcelFormatter
from test_result_filter import REPORTABLE_VERDICTS, load_test_verdicts

def main():
    parser = argparse.ArgumentParser(
        description='Combine failure and error reports.'
    )
    parser.add_argument('--results_csv')
    args = parser.parse_args()

    main_dir = os.getcwd()
    folder_name = os.path.basename(os.path.normpath(main_dir))
    output_file = os.path.join(main_dir, f'Failure_Report_{folder_name}.xlsx')
    report_paths = []
    verdicts = (
        load_test_verdicts(args.results_csv) if args.results_csv else None
    )

    for folder in sorted(os.listdir(main_dir), key=str.casefold):
        folder_path = os.path.join(main_dir, folder)
        if os.path.isdir(folder_path):
            if verdicts is not None and verdicts.get(folder) not in REPORTABLE_VERDICTS:
                continue
            report_path = os.path.join(folder_path, 'failure_report.xlsx')
            if os.path.exists(report_path):
                report_paths.append(report_path)

    if report_paths:
        combined_workbook = Workbook()
        combined_worksheet = combined_workbook.active
        combined_worksheet.title = "Failures"
        combined_worksheet.append(
            ["Test Name", "Result Type", "Failure Step", "Failure Reason"]
        )
        for cell in combined_worksheet[1]:
            cell.font = Font(bold=True)

        for report_path in report_paths:
            report_workbook = load_workbook(report_path, rich_text=True)
            report_worksheet = report_workbook.active
            for source_row in report_worksheet.iter_rows(
                min_row=2, max_col=4
            ):
                combined_worksheet.append(
                    [cell.value for cell in source_row]
                )
                if source_row[3].hyperlink:
                    target_cell = combined_worksheet.cell(
                        row=combined_worksheet.max_row, column=4
                    )
                    target_cell.hyperlink = source_row[3].hyperlink.target
                    target_cell.style = 'Hyperlink'
            report_workbook.close()

        ExcelFormatter.format_report_worksheet(combined_worksheet)
        combined_workbook.save(output_file)
        print(f"Combined report saved to {output_file}")
    else:
        print("No individual reports found to merge.")

if __name__ == "__main__":
    main()