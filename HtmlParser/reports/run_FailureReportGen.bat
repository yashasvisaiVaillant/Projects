@echo off
setlocal enabledelayedexpansion

REM Path to your scripts directory
set "SCRIPTS_DIR=C:\Yashasvi\Projects\HtmlParser"

REM Loop through each subfolder
for /d %%F in (*) do (
    REM Check if it's a directory
    if exist "%%F\" (
        REM Construct full path to data.html
        set "DATA_FILE=%%F\data.html"
        echo Checking: !DATA_FILE!
        if exist "!DATA_FILE!" (
            echo Found: !DATA_FILE!
            echo Processing %%F
            REM Run your script
            set "OUTPUT_FILE=%%F\failure_report.xlsx"
            python "%SCRIPTS_DIR%\generate_failure_report.py" --html_file "!DATA_FILE!" --output_file "!OUTPUT_FILE!"
        ) else (
            echo data.html not found in folder: %%F
        )
        echo.
    )
)

echo All subfolders processed.
pause
endlocal