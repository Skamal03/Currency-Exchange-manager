# main.py
from admin import AdminGUI
from user import UserGUI
import tkinter as tk

def main():
    print("Welcome to Currency Exchange Manager")
    role = input("Login as (admin/user): ").strip().lower()

    root = tk.Tk()
    root.geometry("800x500")

    if role == 'admin':
        app = AdminGUI(root)
    elif role == 'user':
        app = UserGUI(root)
    else:
        print("Invalid role. Exiting.")
        return

    root.mainloop()


main()
