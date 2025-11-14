#!/bin/bash

echo "===================================="
echo " Nonlinear Equations Solver Setup"
echo "===================================="
echo

echo "[1/6] Creating virtual environment..."
python3 -m venv venv
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to create virtual environment. Make sure Python 3.8+ is installed."
    exit 1
fi

echo "[2/6] Activating virtual environment..."
source venv/bin/activate
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to activate virtual environment."
    exit 1
fi

echo "[3/6] Updating pip to latest version..."
python -m pip install --upgrade pip

echo "[4/6] Installing essential build tools..."
pip install setuptools wheel

echo "[5/6] Installing project dependencies..."
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install dependencies."
    echo "Please check the README.md troubleshooting section."
    exit 1
fi

echo "[6/6] Setting up database..."
python manage.py makemigrations
python manage.py migrate
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to set up database."
    exit 1
fi

echo
echo "===================================="
echo "       SETUP COMPLETE! ^_^"
echo "===================================="
echo
echo "To start the development server:"
echo "  1. source venv/bin/activate"
echo "  2. python manage.py runserver"
echo "  3. Open http://127.0.0.1:8000"
echo