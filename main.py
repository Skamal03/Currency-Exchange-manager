# main.py
from admin import admin_interface
from user import user_interface

print("Welcome to Currency Exchange Manager")
role=input("Login as (admin/user): ").strip().lower()

if role=='admin':
    admin_interface()
elif role=='user':
    user_interface()
else:
    print("Invalid role. Exiting.")

