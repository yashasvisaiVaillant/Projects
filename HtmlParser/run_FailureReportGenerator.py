import subprocess
import sys
import os

def main():
    # Get current working directory
    current_dir = os.getcwd()

    # Paths to your scripts (adjust as needed)
    copy_script = r"copy_reports.py"
    report_script = r"generate_failure_report.py"

    # Define source and target directories
    reports_dir = current_dir  # current directory as source
    target_dir = os.path.join(current_dir, "data_for_failure_report")  # subfolder inside current directory

    # Ensure target directory exists
    os.makedirs(target_dir, exist_ok=True)

    # Arguments for copy_reports.py
    copy_args = [
        sys.executable, copy_script,
        '--reports_dir', reports_dir,
        '--target_dir', target_dir
    ]

    # Arguments for generate_failure_report.py
    html_file = os.path.join(current_dir, "data.html") 
    output_file = os.path.join(current_dir, "failure_report.xlsx")

    report_args = [
        sys.executable, report_script,
        '--html_file', html_file,
        '--output_file', output_file
    ]

    # Run copy_reports.py
    print("Running copy_reports.py...")
    subprocess.run(copy_args, check=True)

    # Run generate_failure_report.py
    print("Running generate_failure_report.py...")
    subprocess.run(report_args, check=True)

    print("All tasks completed.")

if __name__ == "__main__":
    main()