import json
from datetime import datetime

class ExpenseTracker:
    def __init__(self, filename='expenses.json'):
        print("Initializing Expense Tracker")
        self.filename = filename
        self.expenses = []
        self.load_expenses()

    def load_expenses(self):
        print("Loading expenses from file")
        try:
            with open(self.filename, 'r') as file:
                self.expenses = json.load(file)
        except FileNotFoundError:
            self.expenses = []

    def save_expenses(self):
        print("Saving expenses to file")
        with open(self.filename, 'w') as file:
            json.dump(self.expenses, file, indent=4)

    def add_expense(self, description, amount, category, date=None):
        if date is None:
            date = datetime.now().strftime('%Y-%m-%d')
        print(f"Adding expense: {description}, {amount}, {category}, {date}")
        self.expenses.append({
            'description': description,
            'amount': amount,
            'category': category,
            'date': date
        })
        self.save_expenses()

    def view_expenses(self, start_date=None, end_date=None):
        print("Viewing expenses")
        for expense in self.expenses:
            expense_date = datetime.strptime(expense['date'], '%Y-%m-%d')
            if (start_date is None or expense_date >= start_date) and (end_date is None or expense_date <= end_date):
                print(f"{expense['date']}: {expense['description']} - ${expense['amount']:.2f} [{expense['category']}]")

    def total_expenses(self, start_date=None, end_date=None):
        print("Calculating total expenses")
        total = 0
        for expense in self.expenses:
            expense_date = datetime.strptime(expense['date'], '%Y-%m-%d')
            if (start_date is None or expense_date >= start_date) and (end_date is None or expense_date <= end_date):
                total += expense['amount']
        return total

    def generate_report(self, start_date=None, end_date=None):
        print("Generating report")
        category_totals = {}
        for expense in self.expenses:
            expense_date = datetime.strptime(expense['date'], '%Y-%m-%d')
            if (start_date is None or expense_date >= start_date) and (end_date is None or expense_date <= end_date):
                category = expense['category']
                category_totals[category] = category_totals.get(category, 0) + expense['amount']
        return category_totals

def parse_date(date_str):
    print(f"Parsing date: {date_str}")
    return datetime.strptime(date_str, '%Y-%m-%d') if date_str else None

def main():
    print("Starting Expense Tracker")
    tracker = ExpenseTracker()

    while True:
        print("\nExpense Tracker")
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. Total Expenses")
        print("4. Generate Report")
        print("5. Exit")

        choice = input("Choose an option: ")

        if choice == '1':
            description = input("Enter description: ")
            amount = float(input("Enter amount: "))
            category = input("Enter category: ")
            date = input("Enter date (YYYY-MM-DD) or leave blank for today: ")
            tracker.add_expense(description, amount, category, date or None)
        elif choice == '2':
            start_date = parse_date(input("Enter start date (YYYY-MM-DD) or leave blank: "))
            end_date = parse_date(input("Enter end date (YYYY-MM-DD) or leave blank: "))
            tracker.view_expenses(start_date, end_date)
        elif choice == '3':
            start_date = parse_date(input("Enter start date (YYYY-MM-DD) or leave blank: "))
            end_date = parse_date(input("Enter end date (YYYY-MM-DD) or leave blank: "))
            total = tracker.total_expenses(start_date, end_date)
            print(f"Total Expenses: ${total:.2f}")
        elif choice == '4':
            start_date = parse_date(input("Enter start date (YYYY-MM-DD) or leave blank: "))
            end_date = parse_date(input("Enter end date (YYYY-MM-DD) or leave blank: "))
            report = tracker.generate_report(start_date, end_date)
            for category, total in report.items():
                print(f"{category}: ${total:.2f}")
        elif choice == '5':
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
