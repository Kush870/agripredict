@echo off
set VENV_DIR=.venv
set PYTHON_EXE=%VENV_DIR%\Scripts\python.exe

if not exist "%PYTHON_EXE%" (
    echo Creating virtual environment in %VENV_DIR%...
    python -m venv "%VENV_DIR%"
    if errorlevel 1 (
        echo Failed to create virtual environment. Make sure Python is installed and available on PATH.
        pause
        exit /b 1
    )
)

echo Upgrading pip inside virtual environment...
"%PYTHON_EXE%" -m pip install --upgrade pip setuptools wheel

echo Installing dependencies...
"%PYTHON_EXE%" -m pip install -r requirements.txt

echo Virtual environment is ready. To start the server:
echo %VENV_DIR%\Scripts\activate
echo python app.py
pause
