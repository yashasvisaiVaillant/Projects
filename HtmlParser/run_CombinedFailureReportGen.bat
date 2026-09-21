@echo off
setlocal

REM Path to your scripts directory
set "SCRIPTS_DIR=C:\Yashasvi\Projects\HtmlParser"
REM set "SCRIPTS_DIR=\\vaders26\Reports\PHP2025\Scripts\HtmlParser"

REM Use the newest test-run results file in the current directory.
set "RESULTS_CSV="
for /f "delims=" %%C in ('dir /b /a-d /o-d "*.csv" 2^>nul') do if not defined RESULTS_CSV set "RESULTS_CSV=%%~fC"

if not defined RESULTS_CSV (
    echo No test-run CSV file found.
    pause
    exit /b 1
)

echo Using test results: "%RESULTS_CSV%"

REM Process each subfolder of the current directory
for /d %%F in (*) do call :ProcessFolder "%%~fF"

echo All subfolders processed.
echo Merging reports...
python "%SCRIPTS_DIR%\merge_reports.py" --results_csv "%RESULTS_CSV%"
echo Merging complete.
pause
endlocal
goto :eof

:ProcessFolder
set "FOLDER=%~1"
echo Checking folder: "%~nx1"

python "%SCRIPTS_DIR%\test_result_filter.py" --csv_file "%RESULTS_CSV%" --test_name "%~nx1"
if errorlevel 2 (
    echo Test verdict unavailable, skipping folder.
    echo(
    goto :eof
)
if errorlevel 1 (
    echo Test passed, skipping folder.
    echo(
    goto :eof
)

REM Skip if report already exists
if exist "%FOLDER%\failure_report.xlsx" (
    echo Report already exists, skipping folder.
    echo(
    goto :eof
)

REM Find the first matching data*.html (If there are multiple data files in the folder, choose only the first)
set "FIRST_HTML="
for /f "delims=" %%H in ('dir /b /a-d /o:n "%FOLDER%\data*.html" 2^>nul') do (
    set "FIRST_HTML=%FOLDER%\%%~H"
    goto :haveFirst
)

:haveFirst
if not defined FIRST_HTML (
    echo No data*.html files found in folder.
    echo(
    goto :eof
)

echo Found: "%FIRST_HTML%"
python "%SCRIPTS_DIR%\generate_report.py" ^
    --html_file "%FIRST_HTML%" ^
    --output_file "%FOLDER%\failure_report.xlsx"

REM Blank line after processing this folder
echo(
goto :eof