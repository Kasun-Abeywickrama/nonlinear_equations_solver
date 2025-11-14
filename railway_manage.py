#!/usr/bin/env python
import os
import sys
from django.core.management import execute_from_command_line

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project_settings.settings")
    
    # Automatically collect static files in production
    if 'collectstatic' not in sys.argv:
        if os.environ.get('RAILWAY_ENVIRONMENT'):
            execute_from_command_line(['manage.py', 'collectstatic', '--noinput'])
    
    execute_from_command_line(sys.argv)