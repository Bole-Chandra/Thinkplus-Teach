import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from api.models import User

# Create Superuser for Admin Dashboard
username = 'admin'
email = 'admin@thinkplus.com'
password = 'adminpassword123'

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username, email, password)
    print(f"✅ Superuser created!")
    print(f"👤 Username: {username}")
    print(f"🔑 Password: {password}")
else:
    print("ℹ️ Superuser already exists.")
