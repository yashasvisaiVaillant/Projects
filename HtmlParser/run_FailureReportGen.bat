@echo off
setlocal

REM Get current directory
set "CURRENT_DIR=%cd%"

REM Paths to your scripts (adjust as needed)
set "SCRIPTS_DIR=C:\Yashasvi\Projects\HtmlParser"

REM Path to your report HTML file (assumed to be in current directory)
set "HTML_FILE=%CURRENT_DIR%\data.html"

REM Output report path
set "OUTPUT_FILE=%CURRENT_DIR%\failure_report.xlsx"

REM Target folder for copying files
set "TARGET_DIR=%CURRENT_DIR%\data_for_failure_report"

REM Ensure target directory exists
if not exist "%TARGET_DIR%" (
    mkdir "%TARGET_DIR%"
)

echo Running copy_reports.py...
python "%SCRIPTS_DIR%\copy_reports.py" --reports_dir "%CURRENT_DIR%" --target_dir "%TARGET_DIR%"

echo Running generate_failure_report.py...
python "%SCRIPTS_DIR%\generate_failure_report.py" --html_file "%HTML_FILE%" --output_file "%OUTPUT_FILE%"

echo All tasks completed.
pause
endlocal