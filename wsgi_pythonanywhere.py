import os
import sys

# Add your project directory to the sys.path
# Replace 'yourusername' with your actual PythonAnywhere username
path = '/home/yourusername/nonlinear_equations_solver'
if path not in sys.path:
    sys.path.insert(0, path)

# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project_settings.settings_pythonanywhere')

# Import Django's WSGI handler
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()