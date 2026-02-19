import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from api.models import User, Assignment

# Create a demo user if it doesn't exist
user, created = User.objects.get_or_create(username='demo_user')
if created:
    user.set_password('pass123')
    user.save()

# Create a demo assignment
Assignment.objects.get_or_create(
    title='Introduction to AI',
    description='Explain the concepts of machine learning and neural networks.',
    created_by=user
)

print("Database seeded with demo user and assignment.")
