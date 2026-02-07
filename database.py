# ============================================================
# DATABASE MODULE - Expense Tracker
# Author: Edward Colon (ESC)
# Copyright (c) 2026
# ============================================================

import sqlite3
from datetime import datetime
import hashlib

DATABASE = 'expenses.db'

def hash_password(password):
    """Hash password using SHA256"""
    return hashlib.sha256(password.encode()).hexdigest()

def init_db():
    """Initialize the database and create tables if they don't exist"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            name TEXT NOT NULL,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            due_date TEXT,
            user_id TEXT NOT NULL DEFAULT 'default',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS budget (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            month TEXT NOT NULL,
            amount REAL NOT NULL,
            user_id TEXT NOT NULL DEFAULT 'default',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(month, user_id)
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            role TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS currency_rates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            currency TEXT NOT NULL UNIQUE,
            rate REAL NOT NULL,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    cursor.execute('SELECT COUNT(*) FROM users')
    if cursor.fetchone()[0] == 0:
        admin_password = hash_password('admin123')
        user_password = hash_password('user123')
        cursor.execute('INSERT INTO users (username, password, role) VALUES (?, ?, ?)', 
                      ('admin', admin_password, 'admin'))
        cursor.execute('INSERT INTO users (username, password, role) VALUES (?, ?, ?)', 
                      ('user', user_password, 'user'))
    
    conn.commit()
    conn.close()

def migrate_from_csv():
    """Migrate existing CSV data to database"""
    import csv
    import os
    
    if not os.path.exists('data.csv'):
        return
    
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    # Check if data already migrated
    cursor.execute('SELECT COUNT(*) FROM expenses')
    if cursor.fetchone()[0] > 0:
        conn.close()
        return
    
    try:
        with open('data.csv', 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                if len(row) >= 4:
                    date = row[0]
                    name = row[1]
                    amount = float(row[2]) if row[2] else 0
                    category = row[3] if len(row) > 3 else 'Others'
                    due_date = row[4] if len(row) > 4 else ''
                    
                    cursor.execute('''
                        INSERT INTO expenses (date, name, amount, category, due_date)
                        VALUES (?, ?, ?, ?, ?)
                    ''', (date, name, amount, category, due_date))
        
        conn.commit()
    except Exception as e:
        pass
    finally:
        conn.close()

def get_all_expenses(page=1, per_page=50, search='', category='', user_id='default'):
    """Get expenses with pagination and filtering"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # Build query
    query = 'SELECT id, date, name, amount, category, due_date FROM expenses WHERE user_id = ?'
    params = [user_id]
    
    if search:
        query += ' AND (name LIKE ? OR category LIKE ?)'
        params.extend([f'%{search}%', f'%{search}%'])
    
    if category:
        query += ' AND category = ?'
        params.append(category)
    
    # Get total count
    count_query = query.replace('SELECT id, date, name, amount, category, due_date', 'SELECT COUNT(*)')
    cursor.execute(count_query, params)
    total = cursor.fetchone()[0]
    
    # Add pagination
    query += ' ORDER BY date DESC, id DESC LIMIT ? OFFSET ?'
    params.extend([per_page, (page - 1) * per_page])
    
    cursor.execute(query, params)
    expenses = cursor.fetchall()
    
    conn.close()
    
    return expenses, total

def add_expense(date, name, amount, category, due_date='', user_id='default'):
    """Add new expense"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO expenses (date, name, amount, category, due_date, user_id)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (date, name, amount, category, due_date, user_id))
    
    conn.commit()
    conn.close()

def update_expense(expense_id, date, name, amount, category, due_date='', user_id='default'):
    """Update existing expense"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    cursor.execute('''
        UPDATE expenses 
        SET date=?, name=?, amount=?, category=?, due_date=?
        WHERE id=? AND user_id=?
    ''', (date, name, amount, category, due_date, expense_id, user_id))
    
    conn.commit()
    conn.close()

def delete_expense(expense_id, user_id='default'):
    """Delete expense"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    cursor.execute('DELETE FROM expenses WHERE id=? AND user_id=?', (expense_id, user_id))
    
    conn.commit()
    conn.close()
def delete_all_expenses(user_id='default'):
    """Delete all expenses from database for specific user"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    cursor.execute('DELETE FROM expenses WHERE user_id=?', (user_id,))
    
    conn.commit()
    conn.close()
def get_expense_by_id(expense_id, user_id='default'):
    """Get single expense by ID"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute('SELECT id, date, name, amount, category, due_date FROM expenses WHERE id=? AND user_id=?', (expense_id, user_id))
    expense = cursor.fetchone()
    
    conn.close()
    return expense

def get_report_data(user_id='default'):
    """Get aggregated data for reports"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # Total
    cursor.execute('SELECT SUM(amount) FROM expenses WHERE user_id=?', (user_id,))
    total = cursor.fetchone()[0] or 0
    
    # Category totals
    cursor.execute('SELECT category, SUM(amount) FROM expenses WHERE user_id=? GROUP BY category', (user_id,))
    category_totals = dict(cursor.fetchall())
    
    # Monthly totals
    cursor.execute('''
        SELECT substr(date, 1, 7) as month, SUM(amount) 
        FROM expenses 
        WHERE user_id=?
        GROUP BY month
    ''', (user_id,))
    monthly_totals = dict(cursor.fetchall())
    
    # All expenses for export
    cursor.execute('SELECT date, name, amount, category, due_date FROM expenses WHERE user_id=? ORDER BY date DESC', (user_id,))
    all_expenses = cursor.fetchall()
    
    conn.close()
    
    return {
        'total': total,
        'category_totals': category_totals,
        'monthly_totals': monthly_totals,
        'all_expenses': all_expenses
    }

def get_budget(month=None, user_id='default'):
    """Get budget for specific month (default: current month)"""
    if not month:
        month = datetime.now().strftime('%Y-%m')
    
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    cursor.execute('SELECT amount FROM budget WHERE month = ? AND user_id = ?', (month, user_id))
    result = cursor.fetchone()
    
    conn.close()
    return result[0] if result else 0

def set_budget(amount, month=None, user_id='default'):
    """Set or update budget for specific month"""
    if not month:
        month = datetime.now().strftime('%Y-%m')
    
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO budget (month, amount, user_id) 
        VALUES (?, ?, ?)
        ON CONFLICT(month, user_id) DO UPDATE SET amount = ?
    ''', (month, amount, user_id, amount))
    
    conn.commit()
    conn.close()

def clear_budget(month=None, user_id='default'):
    """Clear/delete budget for specific month"""
    if not month:
        month = datetime.now().strftime('%Y-%m')
    
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    cursor.execute('DELETE FROM budget WHERE month = ? AND user_id = ?', (month, user_id))
    
    conn.commit()
    conn.close()

def get_budget_status(month=None, user_id='default'):
    """Get budget status with spent and remaining amounts"""
    if not month:
        month = datetime.now().strftime('%Y-%m')
    
    budget = get_budget(month, user_id)
    
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    # Get total spent for the month
    cursor.execute('''
        SELECT SUM(amount) FROM expenses 
        WHERE substr(date, 1, 7) = ? AND user_id = ?
    ''', (month, user_id))
    
    spent = cursor.fetchone()[0] or 0
    conn.close()
    
    remaining = budget - spent
    percentage = (spent / budget * 100) if budget > 0 else 0
    
    return {
        'budget': budget,
        'spent': spent,
        'remaining': remaining,
        'percentage': percentage,
        'month': month
    }

def verify_user(username, password):
    """Verify user credentials and return user info"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    hashed = hash_password(password)
    cursor.execute('SELECT id, username, role FROM users WHERE username = ? AND password = ?', 
                  (username, hashed))
    user = cursor.fetchone()
    
    conn.close()
    
    if user:
        return {'id': user[0], 'username': user[1], 'role': user[2]}
    return None

def create_user(username, password, role='user'):
    """Create new user"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    try:
        hashed = hash_password(password)
        cursor.execute('INSERT INTO users (username, password, role) VALUES (?, ?, ?)',
                      (username, hashed, role))
        conn.commit()
        conn.close()
        return True
    except:
        conn.close()
        return False

def update_currency_rates(rates):
    """Update currency rates in database"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    for currency, rate in rates.items():
        cursor.execute('''
            INSERT OR REPLACE INTO currency_rates (currency, rate, updated_at)
            VALUES (?, ?, CURRENT_TIMESTAMP)
        ''', (currency, rate))
    
    conn.commit()
    conn.close()

def get_currency_rates():
    """Get currency rates from database with timestamp"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute('SELECT currency, rate, updated_at FROM currency_rates')
    rows = cursor.fetchall()
    conn.close()
    
    if not rows:
        return None, None
    
    rates = {row['currency']: row['rate'] for row in rows}
    # Get the most recent update timestamp
    cursor = sqlite3.connect(DATABASE).cursor()
    cursor.execute('SELECT MAX(updated_at) FROM currency_rates')
    last_update = cursor.fetchone()[0]
    
    return rates, last_update

# Initialize database on import
init_db()
migrate_from_csv()
