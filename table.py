def print_table(data, headers):
    # Calculate column widths
    widths = [max(len(str(row[i])) for row in data + [headers]) for i in range(len(headers))]
    row_format = " | ".join(f"{{:<{w}}}" for w in widths)
    print(row_format.format(*headers))
    print("-" * (sum(widths) + 3 * (len(headers) - 1)))
    for row in data:
        print(row_format.format(*row))

def get_monthly_expense_sheet(user_id, year, month):
    conn = sqlite3.connect("finance_manager.db")
    cursor = conn.cursor()

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
        headers = ["Type", "Category", "Amount", "Date"]
        print(f"Expense Sheet for {year}-{month}")
        print_table(transactions, headers)
    else:
        print(f"No transactions found for {year}-{month}.")

# Example Usage
get_monthly_expense_sheet(user_id=1, year=2024, month=11)
