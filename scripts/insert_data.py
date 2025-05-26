import sqlite3
import pandas as pd
from pathlib import Path

# Path to the data folder and database file
data_dir = Path("data/")
db_path = data_dir / "cepea.db"

# Connect to the SQLite database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Map Excel filenames to database column names
file_column_map = {
    "fattened_cattle.xls": "fattened_cattle",
    "rice.xls": "rice",
    "coffee.xls": "coffee",
    "dolar.xls": "dollar"
}

# Loop through each Excel file and update the corresponding column
for filename, column in file_column_map.items():
    file_path = data_dir / filename

    # Read the Excel file, skipping the first 4 rows
    df = pd.read_excel(file_path, skiprows=4)

    # Rename the first two columns to standard names
    df = df.iloc[:, :2]  # select only the first two columns
    df.columns = ['data', 'preco']  # rename columns for consistency

    # Convert 'data' column to string format dd/mm/yyyy
    df['data'] = pd.to_datetime(df['data']).dt.strftime('%d/%m/%Y')

    # Iterate over rows and update or insert into the database
    for _, row in df.iterrows():
        date = row['data']
        price = row['preco']

        # Check if a row with this date already exists
        cursor.execute("SELECT * FROM prices WHERE date = ?", (date,))
        result = cursor.fetchone()

        if result:
            # If exists, update the specific column
            cursor.execute(f"UPDATE prices SET {column} = ? WHERE date = ?", (price, date))
        else:
            # If not exists, insert a new row with only this column filled
            cursor.execute(f"INSERT INTO prices (date, {column}) VALUES (?, ?)", (date, price))






# Commit changes and close connection
conn.commit()
conn.close()

print("Data successfully inserted or updated!")
