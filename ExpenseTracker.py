import tkinter as tk
from tkinter import ttk, messagebox

class Transaction:
    def __init__(self, amount, category, description):
        self.amount = amount
        self.category = category
        self.description = description

    def __str__(self):
        return f"{self.category}: ${self.amount:.2f} - {self.description}"

class User:
    def __init__(self, name):
        self.name = name
        self.transactions = []

    def add_transaction(self, transaction):
        self.transactions.append(transaction)

    def get_balance(self):
        return sum(t.amount for t in self.transactions)

class ExpenseTracker:
    def __init__(self):
        self.users = []

    def add_user(self, user):
        self.users.append(user)

    def get_user(self, name):
        for user in self.users:
            if user.name == name:
                return user
        return None

class ExpenseTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Expense Tracker")
        self.tracker = ExpenseTracker()

        # Initialize User Interface
        self.setup_ui()

    def setup_ui(self):
        # User Selection
        self.user_label = ttk.Label(self.root, text="Select or Add User:")
        self.user_label.grid(row=0, column=0, padx=10, pady=5, sticky="W")

        self.user_combobox = ttk.Combobox(self.root, values=self.get_user_list())
        self.user_combobox.grid(row=0, column=1, padx=10, pady=5, sticky="W")

        self.add_user_button = ttk.Button(self.root, text="Add User", command=self.add_user)
        self.add_user_button.grid(row=0, column=2, padx=10, pady=5, sticky="W")

        # Transaction Entry
        self.amount_label = ttk.Label(self.root, text="Amount:")
        self.amount_label.grid(row=1, column=0, padx=10, pady=5, sticky="W")

        self.amount_entry = ttk.Entry(self.root)
        self.amount_entry.grid(row=1, column=1, padx=10, pady=5, sticky="W")

        self.category_label = ttk.Label(self.root, text="Category:")
        self.category_label.grid(row=2, column=0, padx=10, pady=5, sticky="W")

        self.category_entry = ttk.Entry(self.root)
        self.category_entry.grid(row=2, column=1, padx=10, pady=5, sticky="W")

        self.description_label = ttk.Label(self.root, text="Description:")
        self.description_label.grid(row=3, column=0, padx=10, pady=5, sticky="W")

        self.description_entry = ttk.Entry(self.root)
        self.description_entry.grid(row=3, column=1, padx=10, pady=5, sticky="W")

        self.add_transaction_button = ttk.Button(self.root, text="Add Transaction", command=self.add_transaction)
        self.add_transaction_button.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

        # Transaction List
        self.transaction_list_label = ttk.Label(self.root, text="Transactions:")
        self.transaction_list_label.grid(row=5, column=0, padx=10, pady=5, sticky="W")

        self.transaction_listbox = tk.Listbox(self.root, width=50, height=10)
        self.transaction_listbox.grid(row=6, column=0, columnspan=3, padx=10, pady=5)

        # Report Button
        self.generate_report_button = ttk.Button(self.root, text="Generate Report", command=self.generate_report)
        self.generate_report_button.grid(row=7, column=0, columnspan=3, padx=10, pady=10)

    def get_user_list(self):
        return [user.name for user in self.tracker.users]

    def add_user(self):
        user_name = self.user_combobox.get()
        if user_name and not self.tracker.get_user(user_name):
            new_user = User(user_name)
            self.tracker.add_user(new_user)
            self.user_combobox["values"] = self.get_user_list()

    def add_transaction(self):
        user_name = self.user_combobox.get()
        user = self.tracker.get_user(user_name)

        if not user:
            messagebox.showerror("Error", "Please select a valid user.")
            return

        try:
            amount = float(self.amount_entry.get())
            category = self.category_entry.get()
            description = self.description_entry.get()

            if not category:
                raise ValueError("Category cannot be empty.")

            transaction = Transaction(amount, category, description)
            user.add_transaction(transaction)

            self.transaction_listbox.insert(tk.END, str(transaction))
            self.clear_transaction_fields()
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def clear_transaction_fields(self):
        self.amount_entry.delete(0, tk.END)
        self.category_entry.delete(0, tk.END)
        self.description_entry.delete(0, tk.END)

    def generate_report(self):
        user_name = self.user_combobox.get()
        user = self.tracker.get_user(user_name)

        if not user:
            messagebox.showerror("Error", "Please select a valid user.")
            return

        report_window = tk.Toplevel(self.root)
        report_window.title(f"Report for {user_name}")

        categories = {}
        for t in user.transactions:
            categories[t.category] = categories.get(t.category, 0) + t.amount

        report_text = tk.Text(report_window, wrap=tk.WORD, width=50, height=20)
        report_text.pack(padx=10, pady=10)

        report_text.insert(tk.END, f"Expense Report for {user_name}:\n")
        for category, total in categories.items():
            report_text.insert(tk.END, f"{category}: ${total:.2f}\n")

        report_text.insert(tk.END, f"\nTotal Balance: ${user.get_balance():.2f}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseTrackerApp(root)
    root.mainloop()