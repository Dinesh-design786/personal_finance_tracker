# main.py
from database import Database
from user_manager import UserManager
from transaction_manager import TransactionManager
from budget_manager import BudgetManager
from report_generator import ReportGenerator
from datetime import datetime

class FinanceManager:
    def __init__(self):
        self.db = Database()
        self.user_manager = UserManager(self.db)
        self.transaction_manager = TransactionManager(self.db)
        self.budget_manager = BudgetManager(self.db)
        self.report_generator = ReportGenerator(self.db)
        self.current_user_id = None

    def start(self):
        """Start the application"""
        print("\nWelcome to Personal Finance Manager!")
        self.setup_database()
        
        while True:
            try:
                if not self.current_user_id:
                    self.show_auth_menu()
                else:
                    self.show_main_menu()
            except KeyboardInterrupt:
                print("\nExiting application...")
                break
            except Exception as e:
                print(f"An error occurred: {e}")
                continue

    def setup_database(self):
        """Initialize database with schema and initial data"""
        try:
            self.db.execute_script('dataset.sql')
            self.db