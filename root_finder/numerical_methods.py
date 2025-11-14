"""
Numerical Methods for Solving Nonlinear Equations

This module implements three numerical methods for finding roots of nonlinear equations:
1. Bisection Method
2. Newton-Raphson Method  
3. Secant Method

Each method returns detailed results including:
- Estimated root
- Number of iterations
- Final error
- Convergence history
- Performance metrics
"""

import numpy as np
import time
import math
from typing import Callable, Tuple, List, Dict, Optional
from sympy import symbols, diff, lambdify, sympify, SympifyError


class NumericalMethodResult:
    """Class to store results from numerical methods"""
    
    def __init__(self, root: float, iterations: int, error: float, 
                 converged: bool, method_name: str, execution_time: float,
                 iteration_history: List[Dict] = None):
        self.root = root
        self.iterations = iterations
        self.error = error
        self.converged = converged
        self.method_name = method_name
        self.execution_time = execution_time
        self.iteration_history = iteration_history or []
        
    def to_dict(self):
        """Convert result to dictionary for JSON serialization"""
        return {
            'root': self.root,
            'iterations': self.iterations,
            'error': self.error,
            'converged': self.converged,
            'method_name': self.method_name,
            'execution_time': self.execution_time,
            'iteration_history': self.iteration_history
        }


def parse_function(func_str: str) -> Tuple[Callable, Optional[Callable]]:
    """
    Parse a string representation of a function and return callable functions.
    
    Args:
        func_str: String representation of function (e.g., "x**3 - 6*x**2 + 11*x - 6")
        
    Returns:
        Tuple of (function, derivative_function)
    """
    try:
        x = symbols('x')
        expr = sympify(func_str)
        
        # Create callable function
        f = lambdify(x, expr, 'numpy')
        
        # Create derivative function
        df_expr = diff(expr, x)
        df = lambdify(x, df_expr, 'numpy')
        
        return f, df
        
    except (SympifyError, Exception) as e:
        raise ValueError(f"Invalid function: {func_str}. Error: {str(e)}")


def bisection_method(func: Callable, a: float, b: float, 
                    tolerance: float = 1e-6, max_iterations: int = 100) -> NumericalMethodResult:
    """
    Implement the Bisection Method for finding roots.
    
    Theory:
    The bisection method uses the Intermediate Value Theorem. If f(a) and f(b) have
    opposite signs, then there exists a root in the interval [a,b]. The method
    repeatedly bisects the interval and selects the subinterval that contains the root.
    
    Convergence:
    - Linear convergence with rate 1/2
    - Error decreases by factor of 2 each iteration
    - Guaranteed convergence if initial interval brackets a root
    
    Args:
        func: Function for which to find the root
        a: Left endpoint of initial interval
        b: Right endpoint of initial interval
        tolerance: Convergence tolerance
        max_iterations: Maximum number of iterations
        
    Returns:
        NumericalMethodResult object containing results
    """
    
    start_time = time.time()
    iteration_history = []
    
    # Check if root is bracketed
    fa, fb = func(a), func(b)
    if fa * fb > 0:
        return NumericalMethodResult(
            root=np.nan, iterations=0, error=np.inf, converged=False,
            method_name="Bisection", execution_time=0,
            iteration_history=[{"error": "Root not bracketed in initial interval"}]
        )
    
    # Check if endpoints are roots
    if abs(fa) < tolerance:
        return NumericalMethodResult(
            root=a, iterations=0, error=abs(fa), converged=True,
            method_name="Bisection", execution_time=time.time() - start_time
        )
    if abs(fb) < tolerance:
        return NumericalMethodResult(
            root=b, iterations=0, error=abs(fb), converged=True,
            method_name="Bisection", execution_time=time.time() - start_time
        )
    
    for i in range(max_iterations):
        # Calculate midpoint
        c = (a + b) / 2
        fc = func(c)
        
        # Calculate error
        error = abs(b - a) / 2
        
        # Store iteration data
        iteration_history.append({
            'iteration': i + 1,
            'a': a,
            'b': b,
            'c': c,
            'f(c)': fc,
            'error': error,
            'interval_width': b - a
        })
        
        # Check convergence
        if abs(fc) < tolerance or error < tolerance:
            execution_time = time.time() - start_time
            return NumericalMethodResult(
                root=c, iterations=i + 1, error=error, converged=True,
                method_name="Bisection", execution_time=execution_time,
                iteration_history=iteration_history
            )
        
        # Update interval
        if fa * fc < 0:
            b = c
            fb = fc
        else:
            a = c
            fa = fc
    
    # Max iterations reached
    c = (a + b) / 2
    execution_time = time.time() - start_time
    return NumericalMethodResult(
        root=c, iterations=max_iterations, error=abs(b - a) / 2, converged=False,
        method_name="Bisection", execution_time=execution_time,
        iteration_history=iteration_history
    )


def newton_raphson_method(func: Callable, dfunc: Callable, x0: float,
                         tolerance: float = 1e-6, max_iterations: int = 100) -> NumericalMethodResult:
    """
    Implement the Newton-Raphson Method for finding roots.
    
    Theory:
    Uses the formula: x_{n+1} = x_n - f(x_n)/f'(x_n)
    The method uses linear approximation (tangent line) at each point to
    estimate the location of the root.
    
    Convergence:
    - Quadratic convergence near simple roots
    - Requires f'(x) ≠ 0 near the root
    - May diverge if initial guess is poor or f'(x) = 0
    
    Args:
        func: Function for which to find the root
        dfunc: Derivative of the function
        x0: Initial guess
        tolerance: Convergence tolerance
        max_iterations: Maximum number of iterations
        
    Returns:
        NumericalMethodResult object containing results
    """
    
    start_time = time.time()
    iteration_history = []
    
    x = x0
    
    for i in range(max_iterations):
        fx = func(x)
        dfx = dfunc(x)
        
        # Check if derivative is zero (method fails)
        if abs(dfx) < 1e-12:
            execution_time = time.time() - start_time
            return NumericalMethodResult(
                root=x, iterations=i, error=abs(fx), converged=False,
                method_name="Newton-Raphson", execution_time=execution_time,
                iteration_history=iteration_history + [{"error": "Derivative too close to zero"}]
            )
        
        # Newton-Raphson iteration
        x_new = x - fx / dfx
        error = abs(x_new - x)
        
        # Store iteration data
        iteration_history.append({
            'iteration': i + 1,
            'x': x,
            'f(x)': fx,
            "f'(x)": dfx,
            'x_new': x_new,
            'error': error,
            'step_size': abs(fx / dfx)
        })
        
        # Check convergence
        if error < tolerance or abs(fx) < tolerance:
            execution_time = time.time() - start_time
            return NumericalMethodResult(
                root=x_new, iterations=i + 1, error=error, converged=True,
                method_name="Newton-Raphson", execution_time=execution_time,
                iteration_history=iteration_history
            )
        
        x = x_new
    
    # Max iterations reached
    execution_time = time.time() - start_time
    return NumericalMethodResult(
        root=x, iterations=max_iterations, error=abs(func(x)), converged=False,
        method_name="Newton-Raphson", execution_time=execution_time,
        iteration_history=iteration_history
    )


def secant_method(func: Callable, x0: float, x1: float,
                 tolerance: float = 1e-6, max_iterations: int = 100) -> NumericalMethodResult:
    """
    Implement the Secant Method for finding roots.
    
    Theory:
    Uses the formula: x_{n+1} = x_n - f(x_n) * (x_n - x_{n-1}) / (f(x_n) - f(x_{n-1}))
    Approximates the derivative using finite differences instead of analytical derivative.
    
    Convergence:
    - Superlinear convergence (order ≈ 1.618, golden ratio)
    - Faster than bisection, slower than Newton-Raphson
    - Does not require derivative calculation
    - May fail if f(x_n) ≈ f(x_{n-1})
    
    Args:
        func: Function for which to find the root
        x0: First initial guess
        x1: Second initial guess
        tolerance: Convergence tolerance
        max_iterations: Maximum number of iterations
        
    Returns:
        NumericalMethodResult object containing results
    """
    
    start_time = time.time()
    iteration_history = []
    
    fx0 = func(x0)
    fx1 = func(x1)
    
    for i in range(max_iterations):
        # Check if function values are too close (method fails)
        if abs(fx1 - fx0) < 1e-12:
            execution_time = time.time() - start_time
            return NumericalMethodResult(
                root=x1, iterations=i, error=abs(fx1), converged=False,
                method_name="Secant", execution_time=execution_time,
                iteration_history=iteration_history + [{"error": "Function values too close"}]
            )
        
        # Secant method iteration
        x2 = x1 - fx1 * (x1 - x0) / (fx1 - fx0)
        fx2 = func(x2)
        error = abs(x2 - x1)
        
        # Store iteration data
        iteration_history.append({
            'iteration': i + 1,
            'x0': x0,
            'x1': x1,
            'f(x0)': fx0,
            'f(x1)': fx1,
            'x2': x2,
            'f(x2)': fx2,
            'error': error,
            'secant_slope': (fx1 - fx0) / (x1 - x0) if x1 != x0 else float('inf')
        })
        
        # Check convergence
        if error < tolerance or abs(fx2) < tolerance:
            execution_time = time.time() - start_time
            return NumericalMethodResult(
                root=x2, iterations=i + 1, error=error, converged=True,
                method_name="Secant", execution_time=execution_time,
                iteration_history=iteration_history
            )
        
        # Update for next iteration
        x0, x1 = x1, x2
        fx0, fx1 = fx1, fx2
    
    # Max iterations reached
    execution_time = time.time() - start_time
    return NumericalMethodResult(
        root=x1, iterations=max_iterations, error=abs(fx1), converged=False,
        method_name="Secant", execution_time=execution_time,
        iteration_history=iteration_history
    )


# Predefined test functions
def get_test_functions():
    """Return dictionary of predefined test functions"""
    return {
        'polynomial': {
            'expression': 'x**3 - 6*x**2 + 11*x - 6',
            'description': 'f(x) = x³ - 6x² + 11x - 6 (roots at x = 1, 2, 3)',
            'roots': [1, 2, 3],
            'domain': [0, 4]
        },
        'transcendental1': {
            'expression': 'cos(x) - x',
            'description': 'f(x) = cos(x) - x (root ≈ 0.739)',
            'roots': [0.7390851332],
            'domain': [-2, 2]
        },
        'transcendental2': {
            'expression': 'exp(x) - 3*x**2',
            'description': 'f(x) = eˣ - 3x² (root ≈ 0.620)',
            'roots': [0.6200860387],
            'domain': [-1, 3]
        },
        'trigonometric': {
            'expression': 'sin(x) - x/2',
            'description': 'f(x) = sin(x) - x/2',
            'roots': [0, 1.8955494267],
            'domain': [-1, 3]
        },
        'exponential': {
            'expression': 'x*exp(x) - 1',
            'description': 'f(x) = x·eˣ - 1',
            'roots': [0.5671432904],
            'domain': [0, 1]
        }
    }


def compare_methods(func_str: str, initial_params: Dict, tolerance: float = 1e-6, 
                   max_iterations: int = 100) -> Dict:
    """
    Compare all three methods on the same function with given parameters.
    
    Args:
        func_str: String representation of function
        initial_params: Dictionary with method-specific parameters
        tolerance: Convergence tolerance
        max_iterations: Maximum iterations for each method
        
    Returns:
        Dictionary containing results from all methods
    """
    
    try:
        func, dfunc = parse_function(func_str)
        results = {}
        
        # Bisection method
        if 'bisection' in initial_params:
            params = initial_params['bisection']
            results['bisection'] = bisection_method(
                func, params['a'], params['b'], tolerance, max_iterations
            )
        
        # Newton-Raphson method  
        if 'newton' in initial_params:
            params = initial_params['newton']
            results['newton'] = newton_raphson_method(
                func, dfunc, params['x0'], tolerance, max_iterations
            )
        
        # Secant method
        if 'secant' in initial_params:
            params = initial_params['secant']
            results['secant'] = secant_method(
                func, params['x0'], params['x1'], tolerance, max_iterations
            )
        
        return results
        
    except Exception as e:
        return {'error': str(e)}


if __name__ == "__main__":
    # Test the implementations
    test_functions = get_test_functions()
    
    # Test polynomial function
    func_str = test_functions['polynomial']['expression']
    f, df = parse_function(func_str)
    
    print("Testing Polynomial Function: f(x) = x³ - 6x² + 11x - 6")
    print("=" * 60)
    
    # Test bisection method
    result_bis = bisection_method(f, 0.5, 1.5, tolerance=1e-6)
    print(f"Bisection: Root = {result_bis.root:.6f}, Iterations = {result_bis.iterations}")
    
    # Test Newton-Raphson method
    result_nr = newton_raphson_method(f, df, 0.5, tolerance=1e-6)
    print(f"Newton-Raphson: Root = {result_nr.root:.6f}, Iterations = {result_nr.iterations}")
    
    # Test secant method
    result_sec = secant_method(f, 0.5, 1.5, tolerance=1e-6)
    print(f"Secant: Root = {result_sec.root:.6f}, Iterations = {result_sec.iterations}")