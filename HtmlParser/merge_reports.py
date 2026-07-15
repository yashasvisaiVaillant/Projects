# Merges individual failure reports into a single Excel file and formats it
import os
import pandas as pd
from ExcelFormatter import ExcelFormatter

def main():
    main_dir = os.getcwd()
    output_file = os.path.join(main_dir, 'combined_failure_report.xlsx')
    all_dfs = []

    for folder in os.listdir(main_dir):
        folder_path = os.path.join(main_dir, folder)
        if os.path.isdir(folder_path):
            report_path = os.path.join(folder_path, 'failure_report.xlsx')
            if os.path.exists(report_path):
                df = pd.read_excel(report_path)
                all_dfs.append(df)

    if all_dfs:
        combined_df = pd.concat(all_dfs, ignore_index=True)
        combined_df.to_excel(output_file, index=False)
        print(f"Combined report saved to {output_file}")
    else:
        print("No individual reports found to merge.")

    # format the Excel file
    formatter = ExcelFormatter('combined_failure_report.xlsx')
    formatter.adjust_columns()

if __name__ == "__main__":
    main()