#!/usr/bin/env python
"""
Simple script to set admin password
Run with: python set_admin_password.py
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'personal_website.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()
admin = User.objects.get(username='admin')
admin.set_password('admin123')  # Change this to a secure password
admin.save()
print("Admin password set to: admin123")
print("Username: admin")
print("\nPlease change this password after first login!")
