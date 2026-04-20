#!/usr/bin/env bash
VENV_DIR=.venv
PYTHON=python3

if [ ! -d "$VENV_DIR" ]; then
  echo "Creating virtual environment in $VENV_DIR..."
  $PYTHON -m venv "$VENV_DIR"
fi

echo "Activating virtual environment..."
source "$VENV_DIR/bin/activate"

echo "Upgrading pip, setuptools, and wheel..."
python -m pip install --upgrade pip setuptools wheel

echo "Installing dependencies..."
python -m pip install -r requirements.txt

echo "Virtual environment is ready. Run the server with:"
echo "source $VENV_DIR/bin/activate"
echo "python app.py"
