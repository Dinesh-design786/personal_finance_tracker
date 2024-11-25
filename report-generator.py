# report_generator.py
class ReportGenerator:
    def __init__(self, db):
        self.db = db

    def generate_monthly_report(self, user_id, month, year):
        """Generate monthly financial report"""
        # Get total income and expenses
        query = """
            SELECT 
                SUM(CASE WHEN type = 'income' THEN amount ELSE 0 END) as total_income,
                SUM(CASE WHEN type = 'expense' THEN amount ELSE 0 END) as total_expenses
            FROM transactions
            WHERE user_id = ?
                AND strftime('%m', date) = ?
                AND strftime('%Y', date) = ?
        """
        totals = self.db.fetch_one(query, (user_id, f"{month:02d}", str(year)))
        
        # Get category breakdown
        query = """
            SELECT 
                c.name,
                c.type,
                SUM(t.amount) as total_amount,
                COUNT(t.transaction_id) as transaction_count
            FROM transactions t
            JOIN categories c ON t.category_id = c.category_id
            WHERE t.user_id = ?
                AND strftime('%m', t.date) = ?
                AND strftime('%Y', t.date) = ?
            GROUP BY c.name, c.type
            ORDER BY c.type, total_amount DESC
        """
        categories = self.db.fetch_all(query, (user_id, f"{month:02d}", str(year)))
        
        # Get budget status
        query = """
            SELECT 
                c.name,
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
            GROUP BY c.name, b.amount
        """
        budgets = self.db.fetch_all(query, (
            f"{month:02d}", str(year), user_id, month, year
        ))
        
        return {
            'summary': totals,
            'categories': categories,
            'budgets': budgets
        }

    def generate_annual_report(self, user_id, year):
        """Generate annual financial report"""
        query = """
            SELECT 
                strftime('%m', date) as month,
                SUM(CASE WHEN type = 'income' THEN amount ELSE 0 END) as income,
                SUM(CASE WHEN type = 'expense' THEN amount ELSE 0 END) as expenses,
                COUNT(*) as transaction_count
            FROM transactions
            WHERE user_id = ?
                AND strftime('%Y', date) = ?
            GROUP BY strftime('%m', date)
            ORDER BY month
        """
        return self.db.fetch_all(query, (user_id, str(year)))
