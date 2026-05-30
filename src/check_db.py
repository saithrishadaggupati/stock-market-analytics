import sqlite3

conn = sqlite3.connect("stock_market.db")
cursor = conn.cursor()

# Check table names
print("TABLES IN DATABASE:")
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
print(cursor.fetchall())

# Check column names
print("\nCOLUMNS IN TABLE:")
cursor.execute("PRAGMA table_info(stock_prices)")
print(cursor.fetchall())

conn.close()