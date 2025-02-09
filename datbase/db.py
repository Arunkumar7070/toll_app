import sqlite3
conn = sqlite3.connect("toll_management.db")
cursor = conn.cursor()
cursor.execute("PRAGMA foreign_keys = ON;")
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    carno TEXT PRIMARY KEY,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    name TEXT NOT NULL,
    balance REAL DEFAULT 0.0
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    carno TEXT NOT NULL,
    amount REAL NOT NULL,
    date DATE DEFAULT (DATE('now', 'localtime')),
    FOREIGN KEY (carno) REFERENCES users(carno) ON DELETE CASCADE
);
""")
conn.commit()
conn.close()
print("Database and tables created successfully!")
