import sqlite3

# database path
conn = sqlite3.connect("data/cepea.db")
cursor = conn.cursor()

# Table creation
cursor.execute("""
CREATE TABLE IF NOT EXISTS prices (
    date TEXT PRIMARY KEY,
    fattened_cattle REAL,
    rice REAL,
    coffee REAL,
    dollar REAL
);
""")

conn.commit()
conn.close()

print("Database created successfully!")
