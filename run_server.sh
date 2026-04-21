#!/bin/bash

VENV_DIR=".venv"
PYTHON_EXE="$VENV_DIR/bin/python"

if [ ! -f "$PYTHON_EXE" ]; then
    echo "Creating virtual environment in $VENV_DIR ..."
    python3 -m venv "$VENV_DIR"
    if [ $? -ne 0 ]; then
        echo "Failed to create virtual environment. Make sure Python 3 is installed."
        exit 1
    fi
fi

echo "Installing dependencies in virtual environment..."
"$PYTHON_EXE" -m pip install --upgrade pip setuptools wheel
"$PYTHON_EXE" -m pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "Dependency installation failed."
    exit 1
fi

echo "Starting AgriPredict Backend Server..."
"$PYTHON_EXE" app.py
