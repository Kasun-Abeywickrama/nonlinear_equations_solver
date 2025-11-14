from django.db import models
import json

class CalculationResult(models.Model):
    """Model to store calculation results"""
    
    METHODS = [
        ('bisection', 'Bisection Method'),
        ('newton', 'Newton-Raphson Method'),
        ('secant', 'Secant Method'),
    ]
    
    function_expression = models.TextField(help_text="Mathematical function expression")
    method = models.CharField(max_length=20, choices=METHODS)
    
    # Parameters (stored as JSON)
    parameters = models.JSONField(default=dict, help_text="Method-specific parameters")
    
    # Results
    root = models.FloatField(null=True, blank=True)
    iterations = models.IntegerField(null=True, blank=True)
    error = models.FloatField(null=True, blank=True)
    converged = models.BooleanField(default=False)
    execution_time = models.FloatField(null=True, blank=True, help_text="Execution time in seconds")
    
    # Detailed results (stored as JSON)
    iteration_history = models.JSONField(default=list, help_text="Step-by-step iteration data")
    
    # Metadata
    tolerance = models.FloatField(default=1e-6)
    max_iterations = models.IntegerField(default=100)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        
    def __str__(self):
        return f"{self.get_method_display()} - {self.function_expression[:50]}"
    
    @property
    def convergence_rate(self):
        """Calculate convergence rate if applicable"""
        if not self.converged or len(self.iteration_history) < 2:
            return None
            
        errors = []
        for step in self.iteration_history:
            if 'error' in step:
                errors.append(step['error'])
        
        if len(errors) < 3:
            return None
            
        # Calculate convergence rate using consecutive error ratios
        ratios = []
        for i in range(1, len(errors) - 1):
            if errors[i] > 0 and errors[i+1] > 0:
                ratio = errors[i+1] / errors[i]
                if 0 < ratio < 1:  # Valid convergence ratio
                    ratios.append(ratio)
        
        return sum(ratios) / len(ratios) if ratios else None


class ComparisonSession(models.Model):
    """Model to store comparison sessions between methods"""
    
    function_expression = models.TextField()
    tolerance = models.FloatField(default=1e-6)
    max_iterations = models.IntegerField(default=100)
    
    # Store parameters for all methods
    bisection_params = models.JSONField(null=True, blank=True)
    newton_params = models.JSONField(null=True, blank=True)
    secant_params = models.JSONField(null=True, blank=True)
    
    # Results summary
    results_summary = models.JSONField(default=dict)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        
    def __str__(self):
        return f"Comparison - {self.function_expression[:50]} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"
