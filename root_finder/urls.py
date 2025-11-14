from django.urls import path
from . import views

app_name = 'root_finder'

urlpatterns = [
    path('', views.index, name='index'),
    path('method/<str:method_name>/', views.method_detail, name='method_detail'),
    path('api/calculate/', views.calculate_root, name='calculate_root'),
    path('api/compare/', views.compare_all_methods, name='compare_methods'),
    path('api/test-function/<str:function_name>/', views.get_test_function, name='get_test_function'),
    path('api/clear-history/', views.clear_history, name='clear_history'),
    path('history/', views.results_history, name='history'),
    path('theory/', views.theoretical_background, name='theory'),
]