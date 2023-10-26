import os
import sys

# Set the Django environment settings module.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

# Ensure that Django is imported.
try:
    import django
except ImportError:
    raise ImportError("Django is not installed. Make sure it's in your project's virtual environment.")

# Initialize Django.
django.setup()

def installingdependencies():
    print("Installing dependencies")
    os.system("pip install -r requirements.txt")

def apply_migrations():
    print("Applying migrations...")
    os.system("python manage.py makemigrations")
    os.system("python manage.py migrate")

def create_superuser():
    print("Creating superuser...")
    from django.contrib.auth.models import User
    User.objects.create_superuser('admin', 'admin@example.com', 'adminpassword')

def run_server():
    print("Starting development server...")
    os.system("python manage.py runserver")

