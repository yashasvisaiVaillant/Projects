@echo off
setlocal

REM Path to your scripts directory
set "SCRIPTS_DIR=C:\Yashasvi\Projects\HtmlParser"
REM set "SCRIPTS_DIR=\\vaders26\Reports\PHP2025\Scripts\HtmlParser"

REM Process each subfolder of the current directory
for /d %%F in (*) do call :ProcessFolder "%%~fF"

echo All subfolders processed.
echo Merging reports...
python "%SCRIPTS_DIR%\merge_reports.py"
echo Merging complete.
pause
endlocal
goto :eof

:ProcessFolder
set "FOLDER=%~1"
echo Checking folder: "%~nx1"

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