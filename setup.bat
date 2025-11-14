@echo off
echo Setting up Nonlinear Equations Solver...
echo.

echo Creating virtual environment...
python -m venv venv
if %errorlevel% neq 0 (
    echo Error creating virtual environment. Make sure Python is installed.
    pause
    exit /b 1
)

echo Activating virtual environment...
call venv\Scripts\activate
if %errorlevel% neq 0 (
    echo Error activating virtual environment.
    pause
    exit /b 1
)

echo Updating pip and installing build tools...
python -m pip install --upgrade pip
pip install setuptools wheel

echo Installing dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo Error installing dependencies. Trying flexible versions...
    pip install -r requirements-flexible.txt
    if %errorlevel% neq 0 (
        echo Installation failed. Please check the README for manual installation steps.
        pause
        exit /b 1
    )
)

echo Setting up database...
python manage.py makemigrations
python manage.py migrate

echo.
echo Setup complete! To start the server, run:
echo   venv\Scripts\activate
echo   python manage.py runserver
echo.
pause