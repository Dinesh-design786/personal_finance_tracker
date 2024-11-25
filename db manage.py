# database.py
import sqlite3
from datetime import datetime
import os

class Database:
    def __init__(self, db_name='finance.db'):
        self.db_name = db_name
        self.conn = None
        self.connect()
        
    def connect(self):
        """Establish database connection"""
        try:
            self.conn = sqlite3.connect(self.db_name)
            self.conn.row_factory = sqlite3.Row
        except sqlite3.Error as e:
            print(f"Error connecting to database: {e}")
            raise

    def execute_script(self, script_file):
        """Execute SQL script file"""
        try:
            with open(script_file, 'r') as file:
                script = file.read()
                self.conn.executescript(script)
                self.conn.commit()
        except sqlite3.Error as e:
            print(f"Error executing script: {e}")
            self.conn.rollback()
            raise

    def execute(self, query, params=None):
        """Execute single SQL query"""
        try:
            cursor = self.conn.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            self.conn.commit()
            return cursor
        except sqlite3.Error as e:
            print(f"Error executing query: {e}")
            self.conn.rollback()
            raise

    def fetch_one(self, query, params=None):
        """Fetch single row"""
        cursor = self.execute(query, params)
        return cursor.fetchone()

    def fetch_all(self, query, params=None):
        """Fetch all rows"""
        cursor = self.execute(query, params)
        return cursor.fetchall()

    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
