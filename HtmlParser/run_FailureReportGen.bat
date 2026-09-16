@echo off
setlocal enabledelayedexpansion

REM Path to your scripts directory
set "SCRIPTS_DIR=\\vaders26\Reports\PHP2025\Scripts\HtmlParser"

REM Loop through each subfolder
for /d %%F in (*) do (
    echo Checking folder: %%F

    REM Find all matching data*.html files
    set "FOUND=0"

    for %%H in ("%%F\data*.html") do (
        if exist "%%H" (
            set "FOUND=1"

            echo Found: %%H

            REM Use filename without extension for output
            set "BASE_NAME=%%~nH"
            set "OUTPUT_FILE=%%F\failure_report.xlsx"

            python "%SCRIPTS_DIR%\generate_report.py" ^
                --html_file "%%H" ^
                --output_file "!OUTPUT_FILE!"
        )
    )

    if !FOUND! == 0 (
        echo No data*.html files found in folder: %%F
    )

    echo.
)

echo All subfolders processed.