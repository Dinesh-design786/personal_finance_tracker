import sqlite3
import tabulate

def get_monthly_expense_sheet(user_id, year, month):
    conn = sqlite3.connect("finance_manager.db")
    cursor = conn.cursor()

    # Query to retrieve transactions for the given month and year
    query = """
    SELECT type, category, amount, date 
    FROM transactions
    WHERE user_id = ? AND strftime('%Y', date) = ? AND strftime('%m', date) = ?
    ORDER BY date
    """
    cursor.execute(query, (user_id, str(year), f"{int(month):02}"))
    transactions = cursor.fetchall()
    conn.close()

    if transactions:
        # Formatting the expense sheet
        headers = ["Type", "Category", "Amount", "Date"]
        print("Expense Sheet for {}-{}".format(year, f"{int(month):02}"))
        print(tabulate(transactions, headers=headers, tablefmt="grid"))
    else:
        print(f"No transactions found for {year}-{month}.")

# Example Usage
# Make sure there is data for user_id=1 for testing
get_monthly_expense_sheet(user_id=1, year=2024, month=11)
