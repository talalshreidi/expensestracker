import sqlite3
import os
from datetime import datetime

class ExpenseDBHelper:
    def __init__(self):
        self.db_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
        if not os.path.exists(self.db_dir):
            os.makedirs(self.db_dir)

        self.db_path = os.path.join(self.db_dir, 'expenses.db')
        self.init_database()

    def init_database(self):
        """Initialize the database and create tables if they don't exist."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS entries (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date TEXT NOT NULL,
                    type TEXT NOT NULL,
                    category TEXT NOT NULL,
                    amount REAL NOT NULL,
                    note TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                ''')
                conn.commit()
        except sqlite3.Error as e:
            print(f"Error initializing database: {e}")

    def add_entry(self, entry_data):
        """Add a new entry to the database."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO entries (date, type, category, amount, note, created_at)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (entry_data['date'], entry_data['type'], entry_data['category'], entry_data['amount'], entry_data['note'], datetime.now()))
                conn.commit()
        except sqlite3.Error as e:
            print(f"Error adding entry: {e}")


    def get_all_entries(self):
        """Retrieve all entries from the database."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT * FROM entries')
                return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error retrieving entries: {e}")
            return []

    def get_totals(self):
        """Calculate total income, total expenses, and balance."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT SUM(amount) FROM entries WHERE type = "Income"')
                total_income = cursor.fetchone()[0] or 0.0
                cursor.execute('SELECT SUM(amount) FROM entries WHERE type = "Expense"')
                total_expense = cursor.fetchone()[0] or 0.0
                balance = total_income - total_expense
                return total_income, total_expense, balance
        except sqlite3.Error as e:
            print(f"Error calculating totals: {e}")
            return 0.0, 0.0, 0.0
        
    def update_entry(self, entry_id, entry_data):
        """Update an existing entry in the database."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    UPDATE entries 
                    SET date=?, type=?, category=?, amount=?, note=?
                    WHERE id=?
                ''', (entry_data['date'], entry_data['type'], entry_data['category'], 
                     entry_data['amount'], entry_data['note'], entry_id))
                conn.commit()
        except sqlite3.Error as e:
            print(f"Error updating entry: {e}")

    def delete_entry(self, entry_id):
        """Delete an entry from the database."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('DELETE FROM entries WHERE id=?', (entry_id,))
                conn.commit()
        except sqlite3.Error as e:
            print(f"Error deleting entry: {e}")

    def get_entry_by_id(self, entry_id):
        """Get a single entry by ID."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT * FROM entries WHERE id=?', (entry_id,))
                return cursor.fetchone()
        except sqlite3.Error as e:
            print(f"Error retrieving entry: {e}")
            return None
        
    def get_filtered_entries(self, from_date=None, to_date=None, category=None, entry_type=None):
        """Retrieve filtered entries from the database."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                query = "SELECT * FROM entries WHERE 1=1"
                params = []
                
                # Add date range filter - now properly handles DateEntry format
                if from_date:
                    query += " AND date >= ?"
                    params.append(from_date)
                
                if to_date:
                    query += " AND date <= ?"
                    params.append(to_date)
                
                # Add category filter - handle "Other" specially
                if category and category != "All":
                    if category == "Other":
                        # Filter for categories that are NOT in the predefined list
                        query += " AND category NOT IN ('Food', 'Transport', 'Utilities', 'Entertainment')"
                    else:
                        # Use LIKE for exact match (case-insensitive)
                        query += " AND LOWER(category) = LOWER(?)"
                        params.append(category)
                
                # Add type filter
                if entry_type and entry_type != "All":
                    query += " AND type = ?"
                    params.append(entry_type)
                
                query += " ORDER BY date DESC"
                
                print(f"Debug - Filter Query: {query}")  # Debug line
                print(f"Debug - Filter Params: {params}")  # Debug line
                
                cursor.execute(query, params)
                results = cursor.fetchall()
                print(f"Debug - Found {len(results)} entries")  # Debug line
                return results
                
        except sqlite3.Error as e:
            print(f"Error retrieving filtered entries: {e}")
            return []

    def get_filtered_totals(self, from_date=None, to_date=None, category=None, entry_type=None):
        """Calculate totals for filtered data."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                base_query = "SELECT SUM(amount) FROM entries WHERE 1=1"
                params = []
                
                # Add filters - now properly handles DateEntry format
                if from_date:
                    base_query += " AND date >= ?"
                    params.append(from_date)
                
                if to_date:
                    base_query += " AND date <= ?"
                    params.append(to_date)
                
                # Add category filter - handle "Other" specially
                if category and category != "All":
                    if category == "Other":
                        # Filter for categories that are NOT in the predefined list
                        base_query += " AND category NOT IN ('Food', 'Transport', 'Utilities', 'Entertainment')"
                    else:
                        base_query += " AND LOWER(category) = LOWER(?)"
                        params.append(category)
                
                # Calculate income
                income_query = base_query + " AND type = 'Income'"
                income_params = params.copy()
                if entry_type and entry_type == "Expense":
                    total_income = 0.0
                else:
                    cursor.execute(income_query, income_params)
                    total_income = cursor.fetchone()[0] or 0.0
                
                # Calculate expenses
                expense_query = base_query + " AND type = 'Expense'"
                expense_params = params.copy()
                if entry_type and entry_type == "Income":
                    total_expense = 0.0
                else:
                    cursor.execute(expense_query, expense_params)
                    total_expense = cursor.fetchone()[0] or 0.0
                
                balance = total_income - total_expense
                return total_income, total_expense, balance
                
        except sqlite3.Error as e:
            print(f"Error calculating filtered totals: {e}")
            return 0.0, 0.0, 0.0

    def get_all_categories(self):
        """Get all unique categories from the database."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT DISTINCT category FROM entries ORDER BY category')
                categories = [row[0] for row in cursor.fetchall()]
                return categories
        except sqlite3.Error as e:
            print(f"Error retrieving categories: {e}")
            return []

db = ExpenseDBHelper()