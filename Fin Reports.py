def generate_monthly_report(user_id, month, year):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
    SELECT type, SUM(amount) FROM transactions
    WHERE user_id = ? AND strftime('%m', date) = ? AND strftime('%Y', date) = ?
    GROUP BY type
    """, (user_id, f"{int(month):02d}", year))
    report = cursor.fetchall()
    conn.close()

    total_income = sum(amount for trans_type, amount in report if trans_type == 'income')
    total_expense = sum(amount for trans_type, amount in report if trans_type == 'expense')
    savings = total_income - total_expense

    print(f"\nMonthly Report for {month}/{year}:")
    print(f"Total Income: {total_income}")
    print(f"Total Expenses: {total_expense}")
    print(f"Savings: {savings}")
def generate_monthly_report(user_id, month, year):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
    SELECT type, SUM(amount) FROM transactions
    WHERE user_id = ? AND strftime('%m', date) = ? AND strftime('%Y', date) = ?
    GROUP BY type
    """, (user_id, f"{int(month):02d}", year))
    report = cursor.fetchall()
    conn.close()

    total_income = sum(amount for trans_type, amount in report if trans_type == 'income')
    total_expense = sum(amount for trans_type, amount in report if trans_type == 'expense')
    savings = total_income - total_expense

    print(f"\nMonthly Report for {month}/{year}:")
    print(f"Total Income: {total_income}")
    print(f"Total Expenses: {total_expense}")
    print(f"Savings: {savings}")
