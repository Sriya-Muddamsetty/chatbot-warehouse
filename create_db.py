import sqlite3

def create_database():
    # Connect to SQLite database (it will create the database if it doesn't exist)
    conn = sqlite3.connect('orders.db')
    cursor = conn.cursor()

    # Create the orders table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS orders (
        order_id TEXT PRIMARY KEY,
        status TEXT
    )''')

    # Insert sample data
    cursor.executemany('''
    INSERT OR REPLACE INTO orders (order_id, status) VALUES (?, ?)
    ''', [
        ("ORD123", "Dispatched and on the way!"),
        ("ORD456", "Pending confirmation."),
        ("ORD789", "Delivered successfully.")
    ])

    # Commit and close the connection
    conn.commit()
    conn.close()

create_database()
