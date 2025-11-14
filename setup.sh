#!/bin/bash

echo "Setting up Nonlinear Equations Solver..."
echo

echo "Creating virtual environment..."
python3 -m venv venv
if [ $? -ne 0 ]; then
    echo "Error creating virtual environment. Make sure Python 3.8+ is installed."
    exit 1
fi

echo "Activating virtual environment..."
source venv/bin/activate
if [ $? -ne 0 ]; then
    echo "Error activating virtual environment."
    exit 1
fi

echo "Updating pip and installing build tools..."
python -m pip install --upgrade pip
pip install setuptools wheel

echo "Installing dependencies..."
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "Error installing dependencies. Trying flexible versions..."
    pip install -r requirements-flexible.txt
    if [ $? -ne 0 ]; then
        echo "Installation failed. Please check the README for manual installation steps."
        exit 1
    fi
fi

echo "Setting up database..."
python manage.py makemigrations
python manage.py migrate

echo
echo "Setup complete! To start the server, run:"
echo "  source venv/bin/activate"
echo "  python manage.py runserver"
echo