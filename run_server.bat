@echo off
setlocal enabledelayedexpansion

set VENV_DIR=.venv
set PYTHON_EXE=%VENV_DIR%\Scripts\python.exe

if not exist "%PYTHON_EXE%" (
    echo Creating virtual environment in %VENV_DIR% ...
    python -m venv "%VENV_DIR%"
    if errorlevel 1 (
        echo Failed to create virtual environment. Make sure Python is installed and available on PATH.
        pause
        exit /b 1
    )
)

echo Installing dependencies in virtual environment...
"%PYTHON_EXE%" -m pip install --upgrade pip setuptools wheel
"%PYTHON_EXE%" -m pip install -r requirements.txt

if errorlevel 1 (
    echo Dependency installation failed.
    pause
    exit /b 1
)

echo Starting AgriPredict Backend Server...
"%PYTHON_EXE%" app.py

pause
