# Root Finder - Numerical Methods for Nonlinear Equations

A Django web application implementing numerical methods for solving nonlinear equations including:
- Bisection Method
- Newton-Raphson Method  
- Secant Method

## Features
- Interactive web interface
- Real-time function plotting
- Convergence analysis and comparison
- Step-by-step iteration tracking
- Performance metrics

## Setup
1. Create virtual environment: `python -m venv venv`
2. Activate: `venv\Scripts\activate` (Windows)
3. Install dependencies: `pip install -r requirements.txt`
4. Run migrations: `python manage.py migrate`
5. Start server: `python manage.py runserver`

## Test Functions
- f(x) = x³ - 6x² + 11x - 6 (roots at x = 1, 2, 3)
- f(x) = cos(x) - x (root ≈ 0.739)
- f(x) = e^x - 3x² (root ≈ 0.620)