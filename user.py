import tkinter as tk
from tkinter import ttk, messagebox
from models import Transaction
from manager import ExchangeManager

class UserGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("User Interface - Currency Exchange System")
        self.root.geometry("900x600")
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
        self.create_header("Currency Exchange User Dashboard")

        main_frame = tk.Frame(self.root, bg=self.colors['background'])
        main_frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)

        options = [
            ("Exchange Currency", self.exchange_ui),
            ("View Exchange Rates", self.view_exchange_rates),
            ("Exit", self.exit_program)
        ]

        for label, command in options:
            btn = self.create_button(main_frame, label, command)
            btn.pack(pady=15)

    def exchange_ui(self):
        self.clear_window()
        self.create_header("Exchange Currency")

        form_frame = tk.Frame(self.root, bg=self.colors['background'])
        form_frame.pack(expand=True, pady=20)

        labels = [
            ("User ID", "Enter user ID"),
            ("From Currency", "Enter currency code (e.g., USD)"),
            ("To Currency", "Enter currency code (e.g., EUR)"),
            ("Amount", "Enter amount"),
            ("Exchange Rate", "Enter exchange rate")
        ]
        entries = {}

        for label, placeholder in labels:
            tk.Label(form_frame, text=label, font=('Helvetica', 12),
                     bg=self.colors['background']).pack(pady=5)
            entry, entry_frame = self.create_entry(form_frame, placeholder)
            entry_frame.pack()
            entries[label] = entry

        def submit():
            try:
                user_id_text = entries["User ID"].get()
                from_currency = entries["From Currency"].get().upper()
                to_currency = entries["To Currency"].get().upper()
                amount_text = entries["Amount"].get()
                rate_text = entries["Exchange Rate"].get()

                if (user_id_text == "Enter user ID" or
                    from_currency == "Enter currency code (e.g., USD)" or
                    to_currency == "Enter currency code (e.g., EUR)" or
                    amount_text == "Enter amount" or
                    rate_text == "Enter exchange rate" or
                    not user_id_text or not from_currency or not to_currency or
                    not amount_text or not rate_text):
                    messagebox.showerror("Error", "Please fill all fields.")
                    return

                user_id = int(user_id_text)
                amount = float(amount_text)
                rate = float(rate_text)

                if not self.manager.user_exists(user_id):
                    messagebox.showerror("Error", "User ID does not exist.")
                    return

                transaction = Transaction(user_id, from_currency, to_currency, amount, 0, rate)
                exchanged = self.manager.exchange_currency(transaction)
                messagebox.showinfo("Success", f"Exchanged {amount:.2f} {from_currency} to {exchanged:.2f} {to_currency}")
                self.main_menu()
            except ValueError:
                messagebox.showerror("Error", "Please enter valid numeric values for User ID, Amount, and Exchange Rate.")
            except Exception as e:
                messagebox.showerror("Error", str(e))

        button_frame = tk.Frame(form_frame, bg=self.colors['background'])
        button_frame.pack(pady=20)
        self.create_button(button_frame, "Submit", submit).pack(side=tk.LEFT, padx=10)
        self.create_button(button_frame, "Back", self.main_menu).pack(side=tk.LEFT, padx=10)

    def view_exchange_rates(self):
        self.clear_window()
        self.create_header("Exchange Rates")

        tree_frame = tk.Frame(self.root, bg=self.colors['background'])
        tree_frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)

        tree = ttk.Treeview(tree_frame, columns=["From", "To", "Rate"], show="headings", height=15)
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        tree.configure(yscrollcommand=scrollbar.set)

        for col in ["From", "To", "Rate"]:
            tree.heading(col, text=col)
            tree.column(col, anchor=tk.CENTER, width=200)

        rows = self.manager.get_exchange_rates()
        for row in rows:
            tree.insert("", tk.END, values=row)

        button_frame = tk.Frame(self.root, bg=self.colors['background'])
        button_frame.pack(pady=10)
        self.create_button(button_frame, "Back", self.main_menu).pack()

    def exit_program(self):
        if messagebox.askyesno("Exit", "Are you sure you want to exit?"):
            self.manager.close()
            self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = UserGUI(root)
    root.mainloop()