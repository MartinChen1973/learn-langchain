@echo off
:: Get today's date in yyyyMMdd format
for /f "tokens=1-4 delims=/-. " %%a in ('echo %date%') do (
    set yyyy=%%a
    set mm=%%b
    set dd=%%c
)
set today=%yyyy%%mm%%dd%

:: Create the output file name
set filename=%today%.txt

:: Get Python version and list installed packages
python --version > %filename%
pip list >> %filename%

:: Inform the user
echo Output written to %filename%
pause
