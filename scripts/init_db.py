import sqlite3

# database path
conn = sqlite3.connect("data/cepea.db")
cursor = conn.cursor()

# Table creation
cursor.execute("""
CREATE TABLE IF NOT EXISTS prices (
    -- Date of the price, format will be stored as TEXT (in dd/mm/yyyy)
    date TEXT PRIMARY KEY,

    -- Price of fattened cattle
    fattened_cattle REAL,

    -- Price of rice
    rice REAL,

    -- Price of coffee
    coffee REAL
               
    -- Price of dolar
    dolar REAL

);
""")

conn.commit()
conn.close()

print("Database created successfully!")
