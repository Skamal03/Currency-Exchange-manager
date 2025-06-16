import tkinter as tk
from tkinter import ttk, messagebox
from models import User, Currency, ExchangeRate
from manager import ExchangeManager

class AdminGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Admin Interface - Currency Exchange System")
        self.root.geometry("1000x650")
        self.root.configure(bg="#f0f2f5")
        self.root.resizable(False, False)

        # Define color palette
        self.colors = {
            'primary': '#2c3e50',    # Dark blue
            'secondary': '#3498db',  # Bright blue
            'accent': '#e74c3c',     # Red accent
            'background': '#f0f2f5', # Light gray
            'text': '#333333',       # Dark text
            'entry_bg': '#ffffff',   # White entry
            'button_hover': '#2980b9' # Hover blue
        }

        # Configure styles
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure('TButton', font=('Helvetica', 12, 'bold'), padding=10)
        self.style.configure('TLabel', font=('Helvetica', 12), background=self.colors['background'])
        self.style.configure('Treeview', font=('Helvetica', 10), rowheight=25)
        self.style.configure('Treeview.Heading', font=('Helvetica', 11, 'bold'), 
                           background=self.colors['primary'], foreground='white')

        self.manager = ExchangeManager()
        self.main_menu()

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def create_header(self, text):
        header_frame = tk.Frame(self.root, bg=self.colors['primary'], pady=10)
        header_frame.pack(fill=tk.X)
        tk.Label(header_frame, text=text, font=('Helvetica', 18, 'bold'), 
                 fg='white', bg=self.colors['primary']).pack(pady=5)

    def create_button(self, parent, text, command):
        btn = tk.Button(parent, text=text, command=command, 
                       bg=self.colors['secondary'], fg='white',
                       font=('Helvetica', 11, 'bold'), bd=0, 
                       activebackground=self.colors['button_hover'],
                       activeforeground='white', width=25, pady=8)
        btn.bind('<Enter>', lambda e: btn.config(bg=self.colors['button_hover']))
        btn.bind('<Leave>', lambda e: btn.config(bg=self.colors['secondary']))
        return btn

    def create_entry(self, parent, placeholder):
        entry_frame = tk.Frame(parent, bg=self.colors['background'])
        entry = tk.Entry(entry_frame, font=('Helvetica', 11), 
                        bg=self.colors['entry_bg'], fg=self.colors['text'],
                        bd=1, relief=tk.SOLID, width=30)
        entry.pack(pady=5, padx=10, ipady=5)
        entry.insert(0, placeholder)
        entry.bind('<FocusIn>', lambda e: self.clear_placeholder(entry, placeholder))
        entry.bind('<FocusOut>', lambda e: self.add_placeholder(entry, placeholder))
        return entry, entry_frame

    def clear_placeholder(self, entry, placeholder):
        if entry.get() == placeholder:
            entry.delete(0, tk.END)
            entry.config(fg=self.colors['text'])

    def add_placeholder(self, entry, placeholder):
        if not entry.get():
            entry.insert(0, placeholder)
            entry.config(fg='#7f8c8d')

    def main_menu(self):
        self.clear_window()
        self.create_header("Currency Exchange Admin Dashboard")

        main_frame = tk.Frame(self.root, bg=self.colors['background'])
        main_frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)

        options = [
            ("Add User", self.add_user_ui),
            ("Add Currency", self.add_currency_ui),
            ("Set Exchange Rate", self.set_exchange_rate_ui),
            ("View All Users", self.view_users),
            ("View Exchange Rates", self.view_exchange_rates),
            ("Transaction Summary", self.view_transaction_summary),
            ("Top Currency Pair", self.view_top_currency_pair),
            ("Users Above Avg Transaction", self.view_above_avg_users),
            ("User Transaction History", self.view_user_transaction_history),
            ("Exit", self.exit_program)
        ]

        for i, (label, command) in enumerate(options):
            btn = self.create_button(main_frame, label, command)
            btn.grid(row=i//2, column=i%2, padx=10, pady=10, sticky='ew')

    def add_user_ui(self):
        self.clear_window()
        self.create_header("Add New User")

        form_frame = tk.Frame(self.root, bg=self.colors['background'])
        form_frame.pack(expand=True, pady=20)

        tk.Label(form_frame, text="Name", font=('Helvetica', 12), 
                 bg=self.colors['background']).pack(pady=5)
        name_entry, name_frame = self.create_entry(form_frame, "Enter name")
        name_frame.pack()

        tk.Label(form_frame, text="Email", font=('Helvetica', 12), 
                 bg=self.colors['background']).pack(pady=5)
        email_entry, email_frame = self.create_entry(form_frame, "Enter email")
        email_frame.pack()

        def submit():
            name = name_entry.get()
            email = email_entry.get()
            if name == "Enter name" or email == "Enter email" or not name or not email:
                messagebox.showerror("Error", "Please fill all fields.")
                return
            self.manager.add_user(User(name, email))
            messagebox.showinfo("Success", "User added successfully.")
            self.main_menu()

        button_frame = tk.Frame(form_frame, bg=self.colors['background'])
        button_frame.pack(pady=20)
        self.create_button(button_frame, "Submit", submit).pack(side=tk.LEFT, padx=10)
        self.create_button(button_frame, "Back", self.main_menu).pack(side=tk.LEFT, padx=10)

    def add_currency_ui(self):
        self.clear_window()
        self.create_header("Add New Currency")

        form_frame = tk.Frame(self.root, bg=self.colors['background'])
        form_frame.pack(expand=True, pady=20)

        tk.Label(form_frame, text="Currency Code", font=('Helvetica', 12), 
                 bg=self.colors['background']).pack(pady=5)
        code_entry, code_frame = self.create_entry(form_frame, "Enter currency code (e.g., USD)")
        code_frame.pack()

        tk.Label(form_frame, text="Currency Name", font=('Helvetica', 12), 
                 bg=self.colors['background']).pack(pady=5)
        name_entry, name_frame = self.create_entry(form_frame, "Enter currency name")
        name_frame.pack()

        def submit():
            code = code_entry.get().upper()
            name = name_entry.get()
            if code == "Enter currency code (e.g., USD)" or name == "Enter currency name" or not code or not name:
                messagebox.showerror("Error", "Please fill all fields.")
                return
            self.manager.add_currency(Currency(code, name))
            messagebox.showinfo("Success", "Currency added successfully.")
            self.main_menu()

        button_frame = tk.Frame(form_frame, bg=self.colors['background'])
        button_frame.pack(pady=20)
        self.create_button(button_frame, "Submit", submit).pack(side=tk.LEFT, padx=10)
        self.create_button(button_frame, "Back", self.main_menu).pack(side=tk.LEFT, padx=10)

    def set_exchange_rate_ui(self):
        self.clear_window()
        self.create_header("Set Exchange Rate")

        form_frame = tk.Frame(self.root, bg=self.colors['background'])
        form_frame.pack(expand=True, pady=20)

        tk.Label(form_frame, text="From Currency", font=('Helvetica', 12), 
                 bg=self.colors['background']).pack(pady=5)
        from_entry, from_frame = self.create_entry(form_frame, "Enter currency code (e.g., USD)")
        from_frame.pack()

        tk.Label(form_frame, text="To Currency", font=('Helvetica', 12), 
                 bg=self.colors['background']).pack(pady=5)
        to_entry, to_frame = self.create_entry(form_frame, "Enter currency code (e.g., EUR)")
        to_frame.pack()

        tk.Label(form_frame, text="Exchange Rate", font=('Helvetica', 12), 
                 bg=self.colors['background']).pack(pady=5)
        rate_entry, rate_frame = self.create_entry(form_frame, "Enter rate (e.g., 1.2)")
        rate_frame.pack()

        def submit():
            from_cur = from_entry.get().upper()
            to_cur = to_entry.get().upper()
            rate_text = rate_entry.get()
            if (from_cur == "Enter currency code (e.g., USD)" or 
                to_cur == "Enter currency code (e.g., EUR)" or 
                rate_text == "Enter rate (e.g., 1.2)" or 
                not from_cur or not to_cur or not rate_text):
                messagebox.showerror("Error", "Please fill all fields.")
                return
            try:
                rate = float(rate_text)
                self.manager.set_exchange_rate(ExchangeRate(from_cur, to_cur, rate))
                messagebox.showinfo("Success", "Exchange rate set successfully.")
                self.main_menu()
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid rate.")

        button_frame = tk.Frame(form_frame, bg=self.colors['background'])
        button_frame.pack(pady=20)
        self.create_button(button_frame, "Submit", submit).pack(side=tk.LEFT, padx=10)
        self.create_button(button_frame, "Back", self.main_menu).pack(side=tk.LEFT, padx=10)

    def show_treeview(self, columns, rows, title):
        self.clear_window()
        self.create_header(title)

        tree_frame = tk.Frame(self.root, bg=self.colors['background'])
        tree_frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)

        tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=15)
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        tree.configure(yscrollcommand=scrollbar.set)

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, anchor=tk.CENTER, width=150)

        for row in rows:
            tree.insert("", tk.END, values=row)

        button_frame = tk.Frame(self.root, bg=self.colors['background'])
        button_frame.pack(pady=10)
        self.create_button(button_frame, "Back", self.main_menu).pack()

    def view_users(self):
        rows = self.manager.get_users()
        self.show_treeview(["ID", "Name", "Email"], rows, "All Users")

    def view_exchange_rates(self):
        rows = self.manager.get_exchange_rates()
        self.show_treeview(["From", "To", "Rate"], rows, "Exchange Rates")

    def view_transaction_summary(self):
        rows = self.manager.get_transaction_summary()
        self.show_treeview(["User", "Email", "Total Exchanged"], rows, "Transaction Summary")

    def view_top_currency_pair(self):
        row = self.manager.get_top_currency_pair()
        self.show_treeview(["From", "To", "Count"], [row], "Top Currency Pair")

    def view_above_avg_users(self):
        rows = self.manager.get_above_avg_users()
        self.show_treeview(["Name", "Email"], rows, "Users Above Average Transaction")

    def view_user_transaction_history(self):
        self.clear_window()
        self.create_header("User Transaction History")

        form_frame = tk.Frame(self.root, bg=self.colors['background'])
        form_frame.pack(expand=True, pady=20)

        tk.Label(form_frame, text="User ID", font=('Helvetica', 12), 
                 bg=self.colors['background']).pack(pady=5)
        id_entry, id_frame = self.create_entry(form_frame, "Enter user ID")
        id_frame.pack()

        def submit():
            id_text = id_entry.get()
            if id_text == "Enter user ID" or not id_text:
                messagebox.showerror("Error", "Please enter a user ID.")
                return
            try:
                user_id = int(id_text)
                if not self.manager.user_exists(user_id):
                    messagebox.showerror("Error", "User ID does not exist.")
                    return
                transactions = self.manager.get_user_transaction_history(user_id)
                self.show_treeview(
                    ["ID", "From", "To", "Amount", "Exchanged", "Rate", "Date"],
                    transactions, f"Transaction History for User ID {user_id}"
                )
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid user ID.")

        button_frame = tk.Frame(form_frame, bg=self.colors['background'])
        button_frame.pack(pady=20)
        self.create_button(button_frame, "Submit", submit).pack(side=tk.LEFT, padx=10)
        self.create_button(button_frame, "Back", self.main_menu).pack(side=tk.LEFT, padx=10)

    def exit_program(self):
        if messagebox.askyesno("Exit", "Are you sure you want to exit?"):
            self.manager.close()
            self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = AdminGUI(root)
    root.mainloop()