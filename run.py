#!/usr/bin/env python3
"""
AgriPredict Server Launcher
Simple script to set up and run the application inside a local virtual environment.
"""

import os
import subprocess
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
VENV_DIR = os.path.join(SCRIPT_DIR, '.venv')

if os.name == 'nt':
    VENV_PYTHON = os.path.join(VENV_DIR, 'Scripts', 'python.exe')
else:
    VENV_PYTHON = os.path.join(VENV_DIR, 'bin', 'python')

REQUIREMENTS = os.path.join(SCRIPT_DIR, 'requirements.txt')


def create_virtualenv():
    print('Creating virtual environment...')
    subprocess.check_call([sys.executable, '-m', 'venv', VENV_DIR])
    print('Virtual environment created at', VENV_DIR)


def install_dependencies(python_executable):
    print('Installing dependencies...')
    subprocess.check_call([python_executable, '-m', 'pip', 'install', '--upgrade', 'pip', 'setuptools', 'wheel'])
    subprocess.check_call([python_executable, '-m', 'pip', 'install', '-r', REQUIREMENTS])
    print('Dependencies installed.')


def run_server(python_executable):
    print('Starting AgriPredict server...')
    print('Server will be available at: http://localhost:5000')
    try:
        subprocess.call([python_executable, os.path.join(SCRIPT_DIR, 'app.py')])
    except KeyboardInterrupt:
        print('\nServer stopped.')
        sys.exit(0)


def main():
    if not os.path.exists(VENV_PYTHON):
        create_virtualenv()

    python_executable = VENV_PYTHON if os.path.exists(VENV_PYTHON) else sys.executable

    try:
        install_dependencies(python_executable)
    except subprocess.CalledProcessError:
        print('Failed to install dependencies. Please check your Python version and package compatibility.')
        sys.exit(1)

    run_server(python_executable)


if __name__ == '__main__':
    main()
