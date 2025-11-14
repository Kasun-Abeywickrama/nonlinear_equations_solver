from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Use non-GUI backend
import matplotlib.pyplot as plt
import plotly.graph_objs as go
import plotly.offline as pyo
from plotly.utils import PlotlyJSONEncoder
import io
import base64

from .numerical_methods import (
    parse_function, bisection_method, newton_raphson_method, 
    secant_method, compare_methods, get_test_functions
)
from .models import CalculationResult, ComparisonSession


def index(request):
    """Main page with method selection and input forms"""
    test_functions = get_test_functions()
    recent_results = CalculationResult.objects.all()[:5]
    
    context = {
        'test_functions': test_functions,
        'recent_results': recent_results,
    }
    return render(request, 'nonlinear_equations_solver/index.html', context)


def method_detail(request, method_name):
    """Detailed view for a specific numerical method"""
    if method_name not in ['bisection', 'newton', 'secant']:
        return redirect('index')
    
    test_functions = get_test_functions()
    
    context = {
        'method_name': method_name,
        'test_functions': test_functions,
    }
    return render(request, 'nonlinear_equations_solver/method_detail.html', context)


@csrf_exempt
@require_http_methods(["POST"])
def calculate_root(request):
    """AJAX endpoint to calculate root using specified method"""
    try:
        data = json.loads(request.body)
        
        method = data.get('method')
        function_expr = data.get('function')
        
        # Validate required fields
        if not method:
            return JsonResponse({'error': 'Method is required'}, status=400)
        if not function_expr:
            return JsonResponse({'error': 'Function expression is required'}, status=400)
            
        # Validate and parse numeric parameters
        try:
            tolerance = float(data.get('tolerance', 1e-6))
            max_iterations = int(data.get('max_iterations', 100))
            
            if tolerance <= 0:
                return JsonResponse({'error': 'Tolerance must be positive'}, status=400)
            if max_iterations <= 0:
                return JsonResponse({'error': 'Maximum iterations must be positive'}, status=400)
                
        except (ValueError, TypeError) as e:
            return JsonResponse({'error': f'Invalid numeric parameter: {str(e)}'}, status=400)
        
        # Parse function
        try:
            func, dfunc = parse_function(function_expr)
        except Exception as e:
            return JsonResponse({'error': f'Invalid function: {str(e)}'}, status=400)
        
        # Execute appropriate method with detailed error handling
        try:
            if method == 'bisection':
                try:
                    a = float(data.get('a'))
                    b = float(data.get('b'))
                except (ValueError, TypeError):
                    return JsonResponse({'error': 'Bisection method requires valid numeric values for left endpoint (a) and right endpoint (b)'}, status=400)
                
                if a >= b:
                    return JsonResponse({'error': f'Invalid interval: left endpoint (a={a}) must be less than right endpoint (b={b})'}, status=400)
                
                # Check if root is bracketed
                try:
                    fa, fb = func(a), func(b)
                    if fa * fb > 0:
                        return JsonResponse({
                            'error': f'Root not bracketed in interval [{a}, {b}]. Function values: f({a}) = {fa:.6f}, f({b}) = {fb:.6f}. Both have the same sign.'
                        }, status=400)
                except Exception as e:
                    return JsonResponse({'error': f'Cannot evaluate function at endpoints: {str(e)}'}, status=400)
                
                result = bisection_method(func, a, b, tolerance, max_iterations)
                parameters = {'a': a, 'b': b}
                
            elif method == 'newton':
                try:
                    x0 = float(data.get('x0'))
                except (ValueError, TypeError):
                    return JsonResponse({'error': 'Newton-Raphson method requires a valid numeric initial guess (x0)'}, status=400)
                
                # Check if derivative exists at initial point
                try:
                    fx0 = func(x0)
                    dfx0 = dfunc(x0)
                    if abs(dfx0) < 1e-14:
                        return JsonResponse({
                            'error': f'Derivative is zero or nearly zero at initial guess x0={x0}. f\'({x0}) = {dfx0:.2e}. Try a different initial guess.'
                        }, status=400)
                except Exception as e:
                    return JsonResponse({'error': f'Cannot evaluate function or derivative at x0={x0}: {str(e)}'}, status=400)
                
                result = newton_raphson_method(func, dfunc, x0, tolerance, max_iterations)
                parameters = {'x0': x0}
                
            elif method == 'secant':
                try:
                    x0 = float(data.get('x0'))
                    x1 = float(data.get('x1'))
                except (ValueError, TypeError):
                    return JsonResponse({'error': 'Secant method requires valid numeric values for both initial guesses (x0 and x1)'}, status=400)
                
                if abs(x1 - x0) < 1e-14:
                    return JsonResponse({'error': f'Initial guesses are too close: x0={x0}, x1={x1}. Use different values.'}, status=400)
                
                # Check if function can be evaluated at both points
                try:
                    fx0, fx1 = func(x0), func(x1)
                    if abs(fx1 - fx0) < 1e-14:
                        return JsonResponse({
                            'error': f'Function values are too close at initial guesses: f({x0}) = {fx0:.6f}, f({x1}) = {fx1:.6f}. Try different initial values.'
                        }, status=400)
                except Exception as e:
                    return JsonResponse({'error': f'Cannot evaluate function at initial guesses: {str(e)}'}, status=400)
                
                result = secant_method(func, x0, x1, tolerance, max_iterations)
                parameters = {'x0': x0, 'x1': x1}
                
            else:
                return JsonResponse({'error': f'Unknown method: {method}. Available methods: bisection, newton, secant'}, status=400)
            
            # Check if method failed with specific error messages
            if not result.converged:
                if result.iterations >= max_iterations:
                    error_msg = f'Method did not converge within {max_iterations} iterations. '
                    if hasattr(result, 'error') and result.error:
                        error_msg += f'Final error: {result.error:.2e}. '
                    error_msg += 'Try increasing max iterations or adjusting parameters.'
                    return JsonResponse({'error': error_msg, 'partial_result': result.to_dict()}, status=400)
                else:
                    # Check if there's a specific error in iteration history
                    if result.iteration_history and len(result.iteration_history) > 0:
                        last_step = result.iteration_history[-1]
                        if 'error' in last_step and isinstance(last_step['error'], str):
                            return JsonResponse({'error': f'Method failed: {last_step["error"]}'}, status=400)
                    
                    return JsonResponse({'error': f'Method failed to converge. Final result: {result.to_dict()}'}, status=400)
        
        except Exception as method_error:
            return JsonResponse({'error': f'Calculation error in {method} method: {str(method_error)}'}, status=500)
        
        # Save result to database
        try:
            calc_result = CalculationResult.objects.create(
                function_expression=function_expr,
                method=method,
                parameters=parameters,
                root=result.root if not np.isnan(result.root) else None,
                iterations=result.iterations,
                error=result.error if not np.isinf(result.error) else None,
                converged=result.converged,
                execution_time=result.execution_time,
                iteration_history=result.iteration_history,
                tolerance=tolerance,
                max_iterations=max_iterations
            )
        except Exception as db_error:
            # Don't fail the request if database save fails
            print(f"Database save error: {db_error}")
        
        # Generate function plot if possible
        print(f"DEBUG: Starting response generation for method {method}")
        try:
            print("DEBUG: Converting result to dict")
            response_data = result.to_dict()
            print(f"DEBUG: Result dict: {response_data}")
            
            print("DEBUG: Generating plot")
            plot_data = generate_function_plot(function_expr, result, parameters)
            response_data['plot'] = plot_data
            print("DEBUG: Plot generated successfully")
        except Exception as plot_error:
            print(f"DEBUG: Plot generation error: {plot_error}")
            response_data = result.to_dict()
            response_data['plot'] = None
            response_data['plot_error'] = str(plot_error)
            
        # Add convergence rate if available
        try:
            response_data['convergence_rate'] = calc_result.convergence_rate
        except:
            response_data['convergence_rate'] = None
        
        return JsonResponse(response_data)
        
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON data in request'}, status=400)
    except Exception as e:
        return JsonResponse({'error': f'Unexpected error: {str(e)}'}, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def compare_all_methods(request):
    """AJAX endpoint to compare all three methods"""
    try:
        data = json.loads(request.body)
        
        function_expr = data.get('function')
        tolerance = float(data.get('tolerance', 1e-6))
        max_iterations = int(data.get('max_iterations', 100))
        
        # Extract parameters for each method
        initial_params = {}
        
        if 'bisection' in data:
            initial_params['bisection'] = {
                'a': float(data['bisection']['a']),
                'b': float(data['bisection']['b'])
            }
            
        if 'newton' in data:
            initial_params['newton'] = {
                'x0': float(data['newton']['x0'])
            }
            
        if 'secant' in data:
            initial_params['secant'] = {
                'x0': float(data['secant']['x0']),
                'x1': float(data['secant']['x1'])
            }
        
        # Compare methods
        results = compare_methods(function_expr, initial_params, tolerance, max_iterations)
        
        if 'error' in results:
            return JsonResponse({'error': results['error']}, status=500)
        
        # Save comparison session
        comparison = ComparisonSession.objects.create(
            function_expression=function_expr,
            tolerance=tolerance,
            max_iterations=max_iterations,
            bisection_params=initial_params.get('bisection'),
            newton_params=initial_params.get('newton'),
            secant_params=initial_params.get('secant'),
            results_summary={k: v.to_dict() for k, v in results.items()}
        )
        
        # Convert results to dict format
        response_data = {}
        for method_name, result in results.items():
            response_data[method_name] = result.to_dict()
        
        # Generate comparison plot
        response_data['comparison_plot'] = generate_comparison_plot(function_expr, results)
        response_data['convergence_comparison'] = generate_convergence_plot(results)
        
        return JsonResponse(response_data)
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def generate_function_plot(function_expr, result, parameters):
    """Generate interactive plot of function and root"""
    try:
        # Check if we should generate plots (for cases where Plotly might fail)
        func, _ = parse_function(function_expr)
        
        # Determine plot range
        if 'a' in parameters and 'b' in parameters:
            # Bisection method - use interval
            x_min, x_max = parameters['a'] - 1, parameters['b'] + 1
        else:
            # Newton/Secant - use root vicinity
            root = result.root if not np.isnan(result.root) else 0
            x_min, x_max = root - 3, root + 3
        
        # Generate x values
        x = np.linspace(x_min, x_max, 1000)
        
        try:
            y = func(x)
            # Handle potential overflow/underflow
            y = np.clip(y, -1e10, 1e10)
        except:
            # Fallback for problematic functions
            y = [func(xi) for xi in x]
            y = np.array(y)
            y = np.clip(y, -1e10, 1e10)
        
        # Create plotly figure
        fig = go.Figure()
        
        # Add function curve
        fig.add_trace(go.Scatter(
            x=x, y=y,
            mode='lines',
            name=f'f(x) = {function_expr}',
            line=dict(color='blue', width=2)
        ))
        
        # Add x-axis (y=0 line)
        fig.add_hline(y=0, line_dash="dash", line_color="gray", opacity=0.7)
        
        # Add root point if converged
        if result.converged and not np.isnan(result.root):
            fig.add_trace(go.Scatter(
                x=[result.root], y=[0],
                mode='markers',
                name=f'Root ≈ {result.root:.6f}',
                marker=dict(color='red', size=10, symbol='circle')
            ))
        
        # Add iteration points for visualization
        if result.method_name == 'Bisection' and result.iteration_history:
            # Show interval convergence
            intervals_x = []
            intervals_y = []
            for step in result.iteration_history[-5:]:  # Last 5 intervals
                c = step.get('c', 0)
                fc = step.get('f(c)', 0)
                intervals_x.append(c)
                intervals_y.append(fc)
            
            if intervals_x:
                fig.add_trace(go.Scatter(
                    x=intervals_x, y=intervals_y,
                    mode='markers',
                    name='Iteration points',
                    marker=dict(color='green', size=6, symbol='cross')
                ))
        
        # Update layout
        fig.update_layout(
            title=f'{result.method_name} Method - {function_expr}',
            xaxis_title='x',
            yaxis_title='f(x)',
            showlegend=True,
            height=400,
            template='plotly_white'
        )
        
        return json.dumps(fig, cls=PlotlyJSONEncoder)
        
    except Exception as e:
        return json.dumps({'error': str(e)})


def generate_comparison_plot(function_expr, results):
    """Generate comparison plot showing all methods' performance"""
    try:
        # Create subplots for different metrics
        from plotly.subplots import make_subplots
        
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Iterations to Converge', 'Final Error', 'Execution Time', 'Convergence Rate'),
            specs=[[{'type': 'bar'}, {'type': 'bar'}],
                   [{'type': 'bar'}, {'type': 'bar'}]]
        )
        
        methods = []
        iterations = []
        errors = []
        times = []
        
        for method_name, result in results.items():
            methods.append(method_name.title())
            iterations.append(result.iterations if result.converged else 0)
            errors.append(result.error if result.error and not np.isinf(result.error) else 0)
            times.append(result.execution_time)
        
        # Add bar charts
        fig.add_trace(go.Bar(x=methods, y=iterations, name='Iterations'), row=1, col=1)
        fig.add_trace(go.Bar(x=methods, y=errors, name='Error'), row=1, col=2)
        fig.add_trace(go.Bar(x=methods, y=times, name='Time (s)'), row=2, col=1)
        
        fig.update_layout(height=600, showlegend=False, title_text="Methods Comparison")
        
        return json.dumps(fig, cls=PlotlyJSONEncoder)
        
    except Exception as e:
        return json.dumps({'error': str(e)})


def generate_convergence_plot(results):
    """Generate convergence history plot"""
    try:
        fig = go.Figure()
        
        for method_name, result in results.items():
            if result.iteration_history:
                iterations = []
                errors = []
                
                for i, step in enumerate(result.iteration_history):
                    iterations.append(i + 1)
                    error = step.get('error', 0)
                    if error > 0:
                        errors.append(error)
                    else:
                        errors.append(None)
                
                fig.add_trace(go.Scatter(
                    x=iterations, y=errors,
                    mode='lines+markers',
                    name=f'{method_name.title()} Method',
                    line=dict(width=2)
                ))
        
        fig.update_layout(
            title='Convergence History',
            xaxis_title='Iteration',
            yaxis_title='Error',
            yaxis_type='log',
            height=400,
            template='plotly_white'
        )
        
        return json.dumps(fig, cls=PlotlyJSONEncoder)
        
    except Exception as e:
        return json.dumps({'error': str(e)})


def results_history(request):
    """View calculation history"""
    results = CalculationResult.objects.all()[:20]
    comparisons = ComparisonSession.objects.all()[:10]
    
    context = {
        'results': results,
        'comparisons': comparisons,
    }
    return render(request, 'nonlinear_equations_solver/history.html', context)


def theoretical_background(request):
    """Display theoretical background information"""
    return render(request, 'nonlinear_equations_solver/theory.html')


@require_http_methods(["GET"])
def get_test_function(request, function_name):
    """Get predefined test function details"""
    test_functions = get_test_functions()
    
    if function_name in test_functions:
        return JsonResponse(test_functions[function_name])
    else:
        return JsonResponse({'error': 'Function not found'}, status=404)


@csrf_exempt
@require_http_methods(["POST"])
def clear_history(request):
    """Clear all calculation history"""
    try:
        # Delete all calculation results
        results_count = CalculationResult.objects.count()
        CalculationResult.objects.all().delete()
        
        # Delete all comparison sessions
        comparisons_count = ComparisonSession.objects.count()
        ComparisonSession.objects.all().delete()
        
        return JsonResponse({
            'success': True,
            'message': f'Successfully cleared {results_count} calculation results and {comparisons_count} comparison sessions.',
            'deleted_results': results_count,
            'deleted_comparisons': comparisons_count
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
