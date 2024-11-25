# user_manager.py
import hashlib
from datetime import datetime

class UserManager:
    def __init__(self, db):
        self.db = db

    def hash_password(self, password):
        """Create hash of password"""
        return hashlib.sha256(password.encode()).hexdigest()

    def register_user(self, username, password):
        """Register new user"""
        try:
            password_hash = self.hash_password(password)
            query = """INSERT INTO users (username, password_hash) 
                      VALUES (?, ?)"""
            self.db.execute(query, (username, password_hash))
            return True
        except Exception as e:
            print(f"Error registering user: {e}")
            return False

    def authenticate_user(self, username, password):
        """Authenticate user credentials"""
        try:
            password_hash = self.hash_password(password)
            query = """SELECT user_id, username 
                      FROM users 
                      WHERE username = ? AND password_hash = ?"""
            user = self.db.fetch_one(query, (username, password_hash))
            return user['user_id'] if user else None
        except Exception as e:
            print(f"Error authenticating user: {e}")
            return None

    def get_user_details(self, user_id):
        """Get user details"""
        query = "SELECT user_id, username, created_at FROM users WHERE user_id = ?"
        return self.db.fetch_one(query, (user_id,))
