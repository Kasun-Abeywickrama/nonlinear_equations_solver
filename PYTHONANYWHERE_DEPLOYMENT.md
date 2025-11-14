# PythonAnywhere Deployment Guide for Nonlinear Equations Solver

## Step-by-Step PythonAnywhere Deployment

### Prerequisites
1. Create a free account at [pythonanywhere.com](https://www.pythonanywhere.com)
2. Your project should be on GitHub (we'll clone it on PythonAnywhere)

---

## 🚀 **STEP 1: Upload Your Code**

### Option A: Using GitHub (Recommended)
1. **Login to PythonAnywhere Dashboard**
2. **Open a Bash Console** (Dashboard → Tasks → Bash)
3. **Clone your repository:**
   ```bash
   git clone https://github.com/Kasun-Abeywickrama/nonlinear_equations_solver.git
   cd nonlinear_equations_solver
   ```

### Option B: Upload Files Manually
1. **Go to Files tab** in PythonAnywhere dashboard
2. **Create folder:** `/home/yourusername/nonlinear_equations_solver`
3. **Upload all your project files**

---

## 🚀 **STEP 2: Set Up Virtual Environment**

**In the Bash console, run:**
```bash
# Create virtual environment
python3.10 -m venv venv

# Activate it
source venv/bin/activate

# Install requirements
pip install -r requirements.txt
```

---

## 🚀 **STEP 3: Configure Django Settings**

**Create production settings file:**
```bash
cp project_settings/settings.py project_settings/settings_production.py
```

**Edit the production settings** (use nano or the Files editor):
```bash
nano project_settings/settings_production.py
```

**Make these changes:**
1. Set `DEBUG = False`
2. Add your PythonAnywhere domain to `ALLOWED_HOSTS`:
   ```python
   ALLOWED_HOSTS = ['yourusername.pythonanywhere.com']
   ```
3. Update static files configuration:
   ```python
   STATIC_ROOT = '/home/yourusername/nonlinear_equations_solver/static'
   ```

---

## 🚀 **STEP 4: Set Up Database**

**Run Django migrations:**
```bash
# Make sure you're in project directory and venv is activated
cd /home/yourusername/nonlinear_equations_solver
source venv/bin/activate

# Run migrations
python manage.py migrate --settings=project_settings.settings_production

# Collect static files
python manage.py collectstatic --noinput --settings=project_settings.settings_production

# Create superuser (optional)
python manage.py createsuperuser --settings=project_settings.settings_production
```

---

## 🚀 **STEP 5: Configure Web App**

1. **Go to Web tab** in PythonAnywhere dashboard
2. **Click "Add a new web app"**
3. **Choose "Manual configuration"**
4. **Select Python 3.10**
5. **Click Next**

### Configure WSGI File
1. **Click on WSGI configuration file link**
2. **Replace contents with:**
   ```python
   import os
   import sys

   # Add your project directory to Python path
   path = '/home/yourusername/nonlinear_equations_solver'
   if path not in sys.path:
       sys.path.insert(0, path)

   # Set Django settings module
   os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project_settings.settings_production')

   # Import Django WSGI application
   from django.core.wsgi import get_wsgi_application
   application = get_wsgi_application()
   ```

### Configure Virtual Environment
1. **In Web tab, find "Virtualenv" section**
2. **Enter path:** `/home/yourusername/nonlinear_equations_solver/venv`

### Configure Static Files
1. **In Web tab, find "Static files" section**
2. **Add mapping:**
   - **URL:** `/static/`
   - **Directory:** `/home/yourusername/nonlinear_equations_solver/static`

---

## 🚀 **STEP 6: Launch Your App**

1. **Click "Reload yourusername.pythonanywhere.com"** button
2. **Visit your app:** `https://yourusername.pythonanywhere.com`

---

## 🔧 **Troubleshooting**

### Check Error Logs
- **Web tab → Error log** - Check for Django errors
- **Web tab → Server log** - Check for server errors

### Common Issues & Fixes

**1. Import Errors:**
```bash
# Install missing packages
source venv/bin/activate
pip install missing-package-name
```

**2. Static Files Not Loading:**
```bash
# Re-collect static files
python manage.py collectstatic --noinput --settings=project_settings.settings_production
```

**3. Database Errors:**
```bash
# Re-run migrations
python manage.py migrate --settings=project_settings.settings_production
```

**4. Permission Errors:**
```bash
# Fix file permissions
chmod -R 755 /home/yourusername/nonlinear_equations_solver
```

---

## 🎯 **Free Tier Limitations**

- **CPU seconds:** Limited per day
- **Disk space:** 512MB
- **Custom domains:** Not available (use .pythonanywhere.com subdomain)
- **Always-on tasks:** Not available
- **Outbound internet:** Restricted

---

## 🚀 **Your App Features Will Include:**
- ✅ Bisection Method solver
- ✅ Newton-Raphson Method solver  
- ✅ Secant Method solver
- ✅ Interactive visualizations with Plotly
- ✅ Mathematical equation rendering
- ✅ Results history and analysis
- ✅ Responsive web interface

**Your mathematical equation solver will be live at:**
`https://yourusername.pythonanywhere.com`

Replace `yourusername` with your actual PythonAnywhere username in all the paths and URLs above!