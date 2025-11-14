@echo off
echo ====================================
echo  Nonlinear Equations Solver Setup
echo ====================================
echo.

echo [1/6] Creating virtual environment...
python -m venv venv
if %errorlevel% neq 0 (
    echo ERROR: Failed to create virtual environment. Make sure Python is installed.
    pause
    exit /b 1
)

echo [2/6] Activating virtual environment...
call venv\Scripts\activate
if %errorlevel% neq 0 (
    echo ERROR: Failed to activate virtual environment.
    pause
    exit /b 1
)

echo [3/6] Updating pip to latest version...
python -m pip install --upgrade pip

echo [4/6] Installing essential build tools...
pip install setuptools wheel

echo [5/6] Installing project dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ERROR: Failed to install dependencies.
    echo Please check the README.md troubleshooting section.
    pause
    exit /b 1
)

echo [6/6] Setting up database...
python manage.py makemigrations
python manage.py migrate
if %errorlevel% neq 0 (
    echo ERROR: Failed to set up database.
    pause
    exit /b 1
)

echo.
echo ====================================
echo       SETUP COMPLETE! ^_^
echo ====================================
echo.
echo To start the development server:
echo   1. venv\Scripts\activate
echo   2. python manage.py runserver
echo   3. Open http://127.0.0.1:8000
echo.
pause