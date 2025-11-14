from django.contrib import admin
from .models import CalculationResult, ComparisonSession


@admin.register(CalculationResult)
class CalculationResultAdmin(admin.ModelAdmin):
    list_display = ['function_expression_short', 'method', 'root', 'iterations', 'converged', 'execution_time', 'created_at']
    list_filter = ['method', 'converged', 'created_at']
    search_fields = ['function_expression']
    readonly_fields = ['created_at', 'convergence_rate']
    
    fieldsets = (
        ('Function & Method', {
            'fields': ('function_expression', 'method', 'parameters')
        }),
        ('Results', {
            'fields': ('root', 'iterations', 'error', 'converged', 'execution_time', 'convergence_rate')
        }),
        ('Configuration', {
            'fields': ('tolerance', 'max_iterations')
        }),
        ('Details', {
            'fields': ('iteration_history', 'created_at'),
            'classes': ('collapse',)
        })
    )
    
    def function_expression_short(self, obj):
        return obj.function_expression[:50] + ('...' if len(obj.function_expression) > 50 else '')
    function_expression_short.short_description = 'Function'
    
    def get_queryset(self, request):
        return super().get_queryset(request).order_by('-created_at')


@admin.register(ComparisonSession)
class ComparisonSessionAdmin(admin.ModelAdmin):
    list_display = ['function_expression_short', 'tolerance', 'max_iterations', 'methods_compared', 'created_at']
    list_filter = ['created_at', 'tolerance']
    search_fields = ['function_expression']
    readonly_fields = ['created_at']
    
    fieldsets = (
        ('Function', {
            'fields': ('function_expression', 'tolerance', 'max_iterations')
        }),
        ('Method Parameters', {
            'fields': ('bisection_params', 'newton_params', 'secant_params')
        }),
        ('Results', {
            'fields': ('results_summary', 'created_at')
        })
    )
    
    def function_expression_short(self, obj):
        return obj.function_expression[:40] + ('...' if len(obj.function_expression) > 40 else '')
    function_expression_short.short_description = 'Function'
    
    def methods_compared(self, obj):
        methods = []
        if obj.bisection_params:
            methods.append('Bisection')
        if obj.newton_params:
            methods.append('Newton-Raphson')
        if obj.secant_params:
            methods.append('Secant')
        return ', '.join(methods)
    methods_compared.short_description = 'Methods'
    
    def get_queryset(self, request):
        return super().get_queryset(request).order_by('-created_at')
