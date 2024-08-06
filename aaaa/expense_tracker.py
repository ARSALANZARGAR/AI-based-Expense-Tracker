import json
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox
from sklearn.linear_model import LinearRegression
import numpy as np

class ExpenseTracker:
    def __init__(self, filename='expenses.json'):
        self.filename = filename
        self.expenses = []
        self.load_expenses()

    def load_expenses(self):
        try:
            with open(self.filename, 'r') as file:
                self.expenses = json.load(file)
        except FileNotFoundError:
            self.expenses = []

    def save_expenses(self):
        with open(self.filename, 'w') as file:
            json.dump(self.expenses, file, indent=4)

    def add_expense(self, description, amount, category, date=None):
        if date is None:
            date = datetime.now().strftime('%Y-%m-%d')
        self.expenses.append({
            'description': description,
            'amount': amount,
            'category': category,
            'date': date
        })
        self.save_expenses()

    def view_expenses(self, start_date=None, end_date=None):
        filtered_expenses = []
        for expense in self.expenses:
            expense_date = datetime.strptime(expense['date'], '%Y-%m-%d')
            if (start_date is None or expense_date >= start_date) and (end_date is None or expense_date <= end_date):
                filtered_expenses.append(expense)
        return filtered_expenses

    def total_expenses(self, start_date=None, end_date=None):
        total = 0
        for expense in self.expenses:
            expense_date = datetime.strptime(expense['date'], '%Y-%m-%d')
            if (start_date is None or expense_date >= start_date) and (end_date is None or expense_date <= end_date):
                total += expense['amount']
        return total

    def generate_report(self, start_date=None, end_date=None):
        category_totals = {}
        for expense in self.expenses:
            expense_date = datetime.strptime(expense['date'], '%Y-%m-%d')
            if (start_date is None or expense_date >= start_date) and (end_date is None or expense_date <= end_date):
                category = expense['category']
                category_totals[category] = category_totals.get(category, 0) + expense['amount']
        return category_totals

    def predict_expense(self):
        if len(self.expenses) < 2:
            return "Not enough data to make a prediction."

        dates = [datetime.strptime(exp['date'], '%Y-%m-%d') for exp in self.expenses]
        amounts = [exp['amount'] for exp in self.expenses]

        # Convert dates to numerical values for regression
        dates_num = np.array([(date - dates[0]).days for date in dates]).reshape(-1, 1)
        amounts_num = np.array(amounts)

        model = LinearRegression()
        model.fit(dates_num, amounts_num)

        future_date = (datetime.now() - dates[0]).days + 1
        predicted_amount = model.predict([[future_date]])[0]

        return f"Predicted expense for tomorrow: ${predicted_amount:.2f}"

class ExpenseTrackerGUI:
    def __init__(self, root):
        self.tracker = ExpenseTracker()
        self.root = root
        self.root.title("Expense Tracker")

        self.create_widgets()
        self.apply_styles()

    def create_widgets(self):
        self.tab_control = ttk.Notebook(self.root)

        self.add_expense_tab = ttk.Frame(self.tab_control)
        self.view_expense_tab = ttk.Frame(self.tab_control)
        self.total_expense_tab = ttk.Frame(self.tab_control)
        self.report_tab = ttk.Frame(self.tab_control)
        self.ai_tab = ttk.Frame(self.tab_control)

        self.tab_control.add(self.add_expense_tab, text="Add Expense")
        self.tab_control.add(self.view_expense_tab, text="View Expenses")
        self.tab_control.add(self.total_expense_tab, text="Total Expenses")
        self.tab_control.add(self.report_tab, text="Generate Report")
        self.tab_control.add(self.ai_tab, text="AI Predictions")

        self.tab_control.pack(expand=1, fill="both")

        self.create_add_expense_tab()
        self.create_view_expense_tab()
        self.create_total_expense_tab()
        self.create_report_tab()
        self.create_ai_tab()

    def create_add_expense_tab(self):
        ttk.Label(self.add_expense_tab, text="Description:").grid(row=0, column=0, padx=10, pady=10)
        self.description_entry = ttk.Entry(self.add_expense_tab)
        self.description_entry.grid(row=0, column=1, padx=10, pady=10)

        ttk.Label(self.add_expense_tab, text="Amount:").grid(row=1, column=0, padx=10, pady=10)
        self.amount_entry = ttk.Entry(self.add_expense_tab)
        self.amount_entry.grid(row=1, column=1, padx=10, pady=10)

        ttk.Label(self.add_expense_tab, text="Category:").grid(row=2, column=0, padx=10, pady=10)
        self.category_entry = ttk.Entry(self.add_expense_tab)
        self.category_entry.grid(row=2, column=1, padx=10, pady=10)

        ttk.Label(self.add_expense_tab, text="Date (YYYY-MM-DD):").grid(row=3, column=0, padx=10, pady=10)
        self.date_entry = ttk.Entry(self.add_expense_tab)
        self.date_entry.grid(row=3, column=1, padx=10, pady=10)

        self.add_button = ttk.Button(self.add_expense_tab, text="Add Expense", command=self.add_expense)
        self.add_button.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

    def create_view_expense_tab(self):
        self.start_date_entry = ttk.Entry(self.view_expense_tab)
        self.start_date_entry.grid(row=0, column=1, padx=10, pady=10)
        ttk.Label(self.view_expense_tab, text="Start Date (YYYY-MM-DD):").grid(row=0, column=0, padx=10, pady=10)

        self.end_date_entry = ttk.Entry(self.view_expense_tab)
        self.end_date_entry.grid(row=1, column=1, padx=10, pady=10)
        ttk.Label(self.view_expense_tab, text="End Date (YYYY-MM-DD):").grid(row=1, column=0, padx=10, pady=10)

        self.view_button = ttk.Button(self.view_expense_tab, text="View Expenses", command=self.view_expenses)
        self.view_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

        self.expense_listbox = tk.Listbox(self.view_expense_tab, width=50)
        self.expense_listbox.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

    def create_total_expense_tab(self):
        self.total_start_date_entry = ttk.Entry(self.total_expense_tab)
        self.total_start_date_entry.grid(row=0, column=1, padx=10, pady=10)
        ttk.Label(self.total_expense_tab, text="Start Date (YYYY-MM-DD):").grid(row=0, column=0, padx=10, pady=10)

        self.total_end_date_entry = ttk.Entry(self.total_expense_tab)
        self.total_end_date_entry.grid(row=1, column=1, padx=10, pady=10)
        ttk.Label(self.total_expense_tab, text="End Date (YYYY-MM-DD):").grid(row=1, column=0, padx=10, pady=10)

        self.total_button = ttk.Button(self.total_expense_tab, text="Calculate Total", command=self.calculate_total_expenses)
        self.total_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

        self.total_label = ttk.Label(self.total_expense_tab, text="")
        self.total_label.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

    def create_report_tab(self):
        self.report_start_date_entry = ttk.Entry(self.report_tab)
        self.report_start_date_entry.grid(row=0, column=1, padx=10, pady=10)
        ttk.Label(self.report_tab, text="Start Date (YYYY-MM-DD):").grid(row=0, column=0, padx=10, pady=10)

        self.report_end_date_entry = ttk.Entry(self.report_tab)
        self.report_end_date_entry.grid(row=1, column=1, padx=10, pady=10)
        ttk.Label(self.report_tab, text="End Date (YYYY-MM-DD):").grid(row=1, column=0, padx=10, pady=10)

        self.report_button = ttk.Button(self.report_tab, text="Generate Report", command=self.generate_report)
        self.report_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

        self.report_listbox = tk.Listbox(self.report_tab, width=50)
        self.report_listbox.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

    def create_ai_tab(self):
        self.ai_button = ttk.Button(self.ai_tab, text="Predict Next Expense", command=self.predict_expense)
        self.ai_button.pack(padx=10, pady=10)

        self.ai_label = ttk.Label(self.ai_tab, text="")
        self.ai_label.pack(padx=10, pady=10)

    def add_expense(self):
        description = self.description_entry.get()
        amount = float(self.amount_entry.get())
        category = self.category_entry.get()
        date = self.date_entry.get() or None
        self.tracker.add_expense(description, amount, category, date)
        messagebox.showinfo("Expense Tracker", "Expense added successfully!")

    def view_expenses(self):
        self.expense_listbox.delete(0, tk.END)
        start_date = self.parse_date(self.start_date_entry.get())
        end_date = self.parse_date(self.end_date_entry.get())
        expenses = self.tracker.view_expenses(start_date, end_date)
        for expense in expenses:
            self.expense_listbox.insert(tk.END, f"{expense['date']}: {expense['description']} - ${expense['amount']:.2f} [{expense['category']}]")

    def calculate_total_expenses(self):
        start_date = self.parse_date(self.total_start_date_entry.get())
        end_date = self.parse_date(self.total_end_date_entry.get())
        total = self.tracker.total_expenses(start_date, end_date)
        self.total_label.config(text=f"Total Expenses: ${total:.2f}")

    def generate_report(self):
        self.report_listbox.delete(0, tk.END)
        start_date = self.parse_date(self.report_start_date_entry.get())
        end_date = self.parse_date(self.report_end_date_entry.get())
        report = self.tracker.generate_report(start_date, end_date)
        for category, total in report.items():
            self.report_listbox.insert(tk.END, f"{category}: ${total:.2f}")

    def predict_expense(self):
        prediction = self.tracker.predict_expense()
        self.ai_label.config(text=prediction)

    @staticmethod
    def parse_date(date_str):
        return datetime.strptime(date_str, '%Y-%m-%d') if date_str else None

    def apply_styles(self):
        style = ttk.Style(self.root)
        style.theme_use('clam')
        
        style.configure('TNotebook', background='#6C3483')
        style.configure('TNotebook.Tab', background='#A569BD', foreground='white', padding=(10, 10))
        style.map('TNotebook.Tab', background=[('selected', '#5B2C6F')])

        style.configure('TFrame', background='#D7BDE2')
        style.configure('TLabel', background='#D7BDE2', foreground='#4A235A')
        style.configure('TEntry', fieldbackground='#F2F3F4', background='#E8DAEF')
        style.configure('TButton', background='#A569BD', foreground='white')
        style.map('TButton', background=[('active', '#884EA0')])

if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseTrackerGUI(root)
    root.mainloop()
