# transaction_manager.py
from datetime import datetime

class TransactionManager:
    def __init__(self, db):
        self.db = db

    def add_transaction(self, user_id, category_id, amount, description, type_):
        """Add new transaction"""
        query = """INSERT INTO transactions 
                  (user_id, category_id, amount, description, type)
                  VALUES (?, ?, ?, ?, ?)"""
        try:
            self.db.execute(query, (user_id, category_id, amount, description, type_))
            return True
        except Exception as e:
            print(f"Error adding transaction: {e}")
            return False

    def get_transactions(self, user_id, start_date=None, end_date=None):
        """Get user transactions with optional date range"""
        query = """
            SELECT t.*, c.name as category_name 
            FROM transactions t
            JOIN categories c ON t.category_id = c.category_id
            WHERE t.user_id = ?
        """
        params = [user_id]
        
        if start_date and end_date:
            query += " AND t.date BETWEEN ? AND ?"
            params.extend([start_date, end_date])
            
        query += " ORDER BY t.date DESC"
        return self.db.fetch_all(query, params)

    def get_category_summary(self, user_id, month, year):
        """Get category-wise summary for month"""
        query = """
            SELECT 
                c.name,
                c.type,
                SUM(t.amount) as total_amount
            FROM transactions t
            JOIN categories c ON t.category_id = c.category_id
            WHERE t.user_id = ? 
                AND strftime('%m', t.date) = ? 
                AND strftime('%Y', t.date) = ?
            GROUP BY c.name, c.type
            ORDER BY c.type, total_amount DESC
        """
        return self.db.fetch_all(query, (user_id, f"{month:02d}", str(year)))

    def delete_transaction(self, user_id, transaction_id):
        """Delete a transaction"""
        query = "DELETE FROM transactions WHERE user_id = ? AND transaction_id = ?"
        try:
            self.db.execute(query, (user_id, transaction_id))
            return True
        except Exception as e:
            print(f"Error deleting transaction: {e}")
            return False
