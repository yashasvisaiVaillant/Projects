@echo off
for /r %%F in (failure_report.xlsx) do (
    if exist "%%F" (
        del "%%F"
        echo Deleted: %%F
    )
)
pause