# Nonlinear Equations Solver

A Django web application implementing numerical methods for solving nonlinear equations. This project provides an interactive platform for finding roots of mathematical functions using three classical algorithms with comprehensive analysis and visualization capabilities.

## Project Overview

This application implements three fundamental numerical methods for root-finding problems:

- **Bisection Method**: Guaranteed convergence using the Intermediate Value Theorem
- **Newton-Raphson Method**: Rapid quadratic convergence using function derivatives
- **Secant Method**: Superlinear convergence without requiring derivatives

The system provides detailed iteration tracking, error analysis, convergence visualization, and comparison tools for educational and practical applications.

## Technical Implementation

### Core Technologies
- **Django 4.2.7**: Web framework with MVC architecture
- **Python 3.8+**: Backend programming language
- **SQLite**: Embedded database for results persistence
- **NumPy 1.24.3**: Numerical computations and array operations
- **SymPy 1.12**: Symbolic mathematics and automatic differentiation
- **Plotly 5.17.0**: Interactive function plotting and visualization
- **Matplotlib 3.7.2**: Additional plotting capabilities
- **Pandas 2.0.3**: Data manipulation and analysis

### Frontend Components
- **Tailwind CSS**: Utility-first CSS framework for responsive design
- **Plotly.js**: Client-side interactive charting
- **MathJax**: Mathematical notation rendering
- **Vanilla JavaScript**: Form handling and API interactions

### Application Architecture
```
nonlinear_equations_solver/
├── manage.py                         # Django command-line utility
├── requirements.txt                  # Python package dependencies
├── db.sqlite3                        # SQLite database file
│
├── project_settings/                  # Django project configuration
│   ├── settings.py                   # Application configuration
│   ├── urls.py                       # Root URL patterns
│   ├── wsgi.py                       # WSGI deployment interface
│   └── asgi.py                       # ASGI deployment interface
│
└── nonlinear_equations_solver/        # Main Django application
    ├── models.py                     # Database schema definitions
    ├── views.py                      # HTTP request handlers
    ├── urls.py                       # Application URL routing
    ├── numerical_methods.py          # Core algorithm implementations
    ├── admin.py                      # Django admin configuration
    │
    ├── templates/nonlinear_equations_solver/
    │   ├── base.html                 # Base template with navigation
    │   ├── index.html                # Main calculation interface
    │   ├── method_detail.html        # Individual method pages
    │   ├── history.html              # Calculation history viewer
    │   ├── theory.html               # Mathematical theory and code
    │   └── offline.html              # Offline fallback page
    │
    ├── static/nonlinear_equations_solver/
    │   └── css/
    │       └── fallback.css          # Offline CSS fallback
    │
    └── migrations/                   # Database migration files
        └── 0001_initial.py
```

## Implemented Features

### Core Numerical Methods
Each method includes comprehensive implementation with:
- Input validation and error handling
- Iteration-by-iteration tracking
- Convergence analysis
- Performance timing
- Detailed result reporting

**Bisection Method**
- Interval bracketing validation
- Guaranteed convergence for continuous functions
- Linear convergence rate analysis
- Error bound calculation: |error| ≤ (b-a)/2^n

**Newton-Raphson Method**  
- Automatic symbolic differentiation using SymPy
- Derivative zero detection and handling
- Quadratic convergence monitoring
- Initial guess sensitivity analysis

**Secant Method**
- Two-point finite difference approximation
- No derivative calculation required
- Superlinear convergence (order ≈ 1.618)
- Robust initial guess handling

### Web Application Features

**Interactive Interface**
- Real-time function input with syntax validation
- Method-specific parameter configuration
- Instant calculation with progress indication
- Responsive design for desktop and mobile devices

**Visualization Components**
- Interactive function plotting with Plotly.js
- Root location highlighting on graphs  
- Convergence history visualization
- Error progression analysis charts

**Data Management**
- Persistent calculation history storage
- Result comparison across methods
- Export capabilities for analysis data
- Search and filter functionality for historical results

**Educational Content**
- Comprehensive mathematical theory explanations
- Method comparison and convergence analysis
- Expandable Python code sections showing actual implementation
- Interactive examples with predefined test functions

## Installation and Setup

### Prerequisites
- Python 3.8 or higher
- pip package manager
- Git version control

### Quick Setup (Automated)

**Windows:**
```cmd
setup.bat
```

**Linux/macOS:**
```bash
chmod +x setup.sh
./setup.sh
```

### Manual Installation Steps

1. **Clone Repository**
   ```bash
   git clone https://github.com/Kasun-Abeywickrama/nonlinear_equations_solver.git
   
   cd nonlinear_equations_solver
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv venv
   ```

3. **Activate Virtual Environment**
   ```bash
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

4. **Update pip and Install Build Tools**
   ```bash
   # Update pip to latest version
   python -m pip install --upgrade pip
   
   # Install essential build tools
   pip install setuptools wheel
   ```

5. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```
   

6. **Database Setup**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

7. **Start Development Server**
   ```bash
   python manage.py runserver
   ```

8. **Access Application**
   - Main application: http://127.0.0.1:8000
   - Admin interface: http://127.0.0.1:8000/admin

## Troubleshooting

### If you get "Cannot import 'setuptools.build_meta'" error:
1. Make sure you have the latest pip: `python -m pip install --upgrade pip`
2. Install build tools: `pip install setuptools wheel`
3. Use the individual package installation method above

### Package Version Notes for Python 3.13:
- **NumPy**: Use `numpy>=1.26.0` (earlier versions don't support Python 3.13)
- **Matplotlib**: Use `matplotlib>=3.8.0` (3.7.x requires C++ build tools)
- **Other packages**: Use the versions specified in requirements.txt

### Python Version Compatibility:
- **Supported:** Python 3.8 - 3.13
- **Recommended:** Python 3.10 - 3.12
- **Python 3.7 or lower:** Not supported

## Usage Examples

### Function Input Format
The application accepts functions in Python/SymPy syntax:

**Polynomial Functions:**
- `x**3 - 6*x**2 + 11*x - 6` (cubic polynomial)
- `x**2 - 2` (quadratic)
- `x**4 - x - 1` (quartic)

**Transcendental Functions:**
- `cos(x) - x` (trigonometric)
- `exp(x) - 3*x**2` (exponential)
- `sin(x) - x/2` (trigonometric)
- `x*exp(x) - 1` (mixed)

### Method-Specific Parameters

**Bisection Method Example:**
- Function: `x**3 - 2*x - 5`
- Left endpoint (a): `2`
- Right endpoint (b): `3`
- Expected root: ≈ 2.094551

**Newton-Raphson Method Example:**
- Function: `x**2 - 2`
- Initial guess: `1.5`
- Expected root: ≈ 1.414214 (√2)

**Secant Method Example:**
- Function: `x**3 - x - 1`
- First guess: `1.0`
- Second guess: `1.5`
- Expected root: ≈ 1.324718

## Features and Capabilities

### Core Functionality
- **Three Numerical Methods**: Complete implementation with error handling
- **Interactive Interface**: Real-time parameter input and validation
- **Function Parsing**: Supports complex mathematical expressions
- **Convergence Analysis**: Detailed iteration tracking and error progression
- **Performance Metrics**: Execution time and efficiency comparison

### Visualization
- **Function Plotting**: Interactive graphs using Plotly.js
- **Root Visualization**: Graphical representation of found roots
- **Convergence Plots**: Error reduction over iterations
- **Method Comparison**: Side-by-side analysis charts

### Data Management
- **Calculation History**: Persistent storage of all computations
- **Result Export**: JSON format for further analysis
- **Search and Filter**: Find previous calculations by method or function
- **Database Integration**: Django ORM with SQLite backend

### Educational Content
- **Theoretical Background**: Mathematical foundations and proofs
- **Implementation Code**: Expandable Python code sections
- **Convergence Theory**: Analysis of convergence rates and conditions
- **Practical Examples**: Predefined test functions with known solutions

## Database Schema

### CalculationResult Model
```python
class CalculationResult(models.Model):
    function_expression = models.TextField()      # Input function
    method = models.CharField(max_length=20)      # Solution method
    parameters = models.JSONField()               # Method parameters
    root = models.FloatField()                    # Found root
    iterations = models.IntegerField()            # Number of iterations
    error = models.FloatField()                   # Final error
    converged = models.BooleanField()             # Convergence status
    execution_time = models.FloatField()          # Performance metric
    iteration_history = models.JSONField()        # Step-by-step data
    tolerance = models.FloatField()               # Convergence tolerance
    max_iterations = models.IntegerField()        # Iteration limit
    created_at = models.DateTimeField()           # Timestamp
```

### ComparisonSession Model
```python
class ComparisonSession(models.Model):
    function_expression = models.TextField()      # Compared function
    results = models.JSONField()                  # All method results
    created_at = models.DateTimeField()           # Session timestamp
```

## API Endpoints

### Core Endpoints
- `GET /` - Main application interface
- `GET /method/<method_name>/` - Individual method pages
- `GET /history/` - Calculation history
- `GET /theory/` - Mathematical theory and implementation

### AJAX API
- `POST /api/calculate/` - Execute numerical method
- `POST /api/compare/` - Compare all methods
- `GET /api/test-function/<name>/` - Get predefined test functions
- `POST /api/clear-history/` - Clear calculation history

## Testing and Validation

### Unit Testing
```bash
python manage.py test
```

### Manual Testing
```bash
python manage.py shell
```
```python
from nonlinear_equations_solver.numerical_methods import *

# Test function parsing
f, df = parse_function('x**3 - 6*x**2 + 11*x - 6')

# Test bisection method
result = bisection_method(f, 0, 4)
print(f"Root: {result.root}, Converged: {result.converged}")

# Test Newton-Raphson method
result = newton_raphson_method(f, df, 1.5)
print(f"Root: {result.root}, Iterations: {result.iterations}")

# Test secant method
result = secant_method(f, 0.5, 1.5)
print(f"Root: {result.root}, Error: {result.error}")
```

## Configuration Options

### Development Settings
- Debug mode enabled
- SQLite database
- Local static files
- Detailed error reporting

### Production Considerations
- Set `DEBUG = False` in production
- Configure allowed hosts
- Use production database (PostgreSQL/MySQL)
- Enable static file serving via web server
- Implement proper secret key management

## Educational Applications

### Course Integration
- **Numerical Analysis**: Fundamental root-finding algorithms
- **Computational Mathematics**: Practical implementation techniques
- **Software Engineering**: Web application development with Django
- **Data Visualization**: Mathematical plotting and analysis

### Learning Outcomes
- Understanding convergence theory and analysis
- Comparing algorithmic efficiency and reliability
- Implementing mathematical algorithms in Python
- Creating interactive web-based mathematical tools

## Contributing

### Development Guidelines
- Follow PEP 8 Python style guidelines
- Include comprehensive docstrings
- Add unit tests for new features
- Maintain backward compatibility
- Update documentation for changes

### Code Quality
- Type hints for function parameters
- Error handling and input validation
- Performance optimization for large datasets
- Cross-browser compatibility for frontend

## License

This project is developed for educational purposes as part of numerical methods coursework. Please refer to institutional guidelines for usage and distribution.

## Acknowledgments

- **Mathematical References**: Burden & Faires "Numerical Analysis"
- **Django Framework**: Django Software Foundation
- **Scientific Python**: NumPy, SymPy, and SciPy communities
- **Visualization**: Plotly development team

---

**Project Status**: Active development as part of numerical methods coursework
**Last Updated**: November 2025