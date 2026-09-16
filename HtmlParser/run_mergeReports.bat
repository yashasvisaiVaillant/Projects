@echo off
setlocal enabledelayedexpansion

REM Path to your scripts directory
set "SCRIPTS_DIR=\\vaders26\Reports\PHP2025\Scripts\HtmlParser"

REM Call merge script
echo Merging reports...
python "%SCRIPTS_DIR%\merge_reports.py"

echo Merging complete.
pause
endlocal