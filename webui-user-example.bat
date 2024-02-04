@echo off

call venv\Scripts\activate.bat
if %ERRORLEVEL% == 0 (
    echo VirtualEnv Loaded
    if "%~1" == "--http" (
        echo Launching main
        py main.py --listen --preview-method auto
    ) else (
        echo Launching main_https
        py main_https.py --listen --preview-method auto
    )
) else (
    echo Error, venv not launched, closing
)