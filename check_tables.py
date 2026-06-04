import sqlite3
conn = sqlite3.connect('stock_market.db')
print(conn.execute('PRAGMA table_info(stock_prices)').fetchall())