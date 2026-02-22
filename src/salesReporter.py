"""
Sales Reporting Module — generates reports from order data.
Uses an in-memory SQLite database for portability.

Author: Finance Engineering Team
"""

import sqlite3
from typing import Dict, List


class SalesReporter:
    def __init__(self, db_path=':memory:'):
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        self._create_tables()

    def _create_tables(self):
        cursor = self.conn.cursor()
        cursor.executescript('''
            CREATE TABLE IF NOT EXISTS customers (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                email TEXT UNIQUE,
                region TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY,
                customer_id INTEGER NOT NULL,
                amount DECIMAL(10,2) NOT NULL,
                order_date DATE NOT NULL,
                status TEXT DEFAULT 'completed',
                FOREIGN KEY (customer_id) REFERENCES customers(id)
            );

            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                price DECIMAL(10,2) NOT NULL,
                category TEXT
            );

            CREATE TABLE IF NOT EXISTS order_items (
                order_id INTEGER,
                product_id INTEGER,
                quantity INTEGER NOT NULL,
                FOREIGN KEY (order_id) REFERENCES orders(id),
                FOREIGN KEY (product_id) REFERENCES products(id)
            );
        ''')
        self.conn.commit()

    def seed_data(self):
        cursor = self.conn.cursor()
        cursor.executescript('''
            INSERT INTO customers VALUES (1, 'Alice', 'alice@test.com', 'North');
            INSERT INTO customers VALUES (2, 'Bob', 'bob@test.com', 'South');
            INSERT INTO customers VALUES (3, 'Charlie', 'charlie@test.com', 'North');
            INSERT INTO customers VALUES (4, 'Diana', 'diana@test.com', 'South');

            INSERT INTO orders VALUES (101, 1, 150.00, '2026-01-15', 'completed');
            INSERT INTO orders VALUES (102, 1, 200.00, '2026-02-10', 'completed');
            INSERT INTO orders VALUES (103, 2, 75.00, '2026-01-20', 'completed');
            INSERT INTO orders VALUES (104, 3, 300.00, '2026-02-25', 'completed');
            INSERT INTO orders VALUES (105, 2, 50.00, '2026-03-05', 'cancelled');
        ''')
        self.conn.commit()

    def revenue_by_region(self) -> List[Dict]:
        # Should use INNER JOIN and WHERE status = 'completed'
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT c.region, SUM(o.amount) as total_revenue
            FROM customers c
            LEFT JOIN orders o ON c.id = o.customer_id
            GROUP BY c.region
        ''')
        return [dict(row) for row in cursor.fetchall()]

    def customer_order_report(self) -> List[Dict]:
        # This creates a cartesian product (every customer x every order)
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT c.name, c.region, COUNT(*) as order_count, SUM(o.amount) as total_spent
            FROM customers c, orders o
            GROUP BY c.name
        ''')
        return [dict(row) for row in cursor.fetchall()]

    def monthly_revenue(self) -> List[Dict]:
        # %M is minutes, %m is month!
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT strftime('%Y-%M', order_date) as month, SUM(amount) as revenue
            FROM orders
            WHERE status = 'completed'
            GROUP BY strftime('%Y-%M', order_date)
            ORDER BY month
        ''')
        return [dict(row) for row in cursor.fetchall()]

    def close(self):
        self.conn.close()
