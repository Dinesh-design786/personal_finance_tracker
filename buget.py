# budget_manager.py
class BudgetManager:
    def __init__(self, db):
        self.db = db

    def set_budget(self, user_id, category_id, amount, month, year):
        """Set or update budget for category"""
        query = """INSERT OR REPLACE INTO budgets 
                  (user_id, category_id, amount, month, year)
                  VALUES (?, ?, ?, ?, ?)"""
        try:
            self.db.execute(query, (user_id, category_id, amount, month, year))
            return True
        except Exception as e:
            print(f"Error setting budget: {e}")
            return False

    def get_budgets(self, user_id, month, year):
        """Get all budgets for month"""
        query = """
            SELECT 
                b.budget_id,
                c.name as category_name,
                b.amount as budget_amount,
                COALESCE(SUM(t.amount), 0) as spent_amount
            FROM budgets b
            JOIN categories c ON b.category_id = c.category_id
            LEFT JOIN transactions t ON 
                t.category_id = b.category_id 
                AND t.user_id = b.user_id
                AND strftime('%m', t.date) = ?
                AND strftime('%Y', t.date) = ?
            WHERE b.user_id = ? 
                AND b.month = ? 
                AND b.year = ?
            GROUP BY b.budget_id, c.name
        """
        return self.db.fetch_all(query, (
            f"{month:02d}", str(year), user_id, month, year
        ))

    def check_budget_status(self, user_id, category_id, month, year):
        """Check status of specific budget"""
        query = """
            SELECT 
                b.amount as budget_amount,
                COALESCE(SUM(t.amount), 0) as spent_amount,
                b.amount - COALESCE(SUM(t.amount), 0) as remaining_amount
            FROM budgets b
            LEFT JOIN transactions t ON 
                t.category_id = b.category_id 
                AND t.user_id = b.user_id
                AND strftime('%m', t.date) = ?
                AND strftime('%Y', t.date) = ?
            WHERE b.user_id = ? 
                AND b.category_id = ?
                AND b.month = ? 
                AND b.year = ?
            GROUP BY b.amount
        """
        return self.db.fetch_one(query, (
            f"{month:02d}", str(year), user_id, category_id, month, year
        ))
