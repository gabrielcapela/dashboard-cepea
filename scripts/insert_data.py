import pandas as pd
import psycopg2
from pathlib import Path
import subprocess
import os
from dotenv import load_dotenv

# Load environment variables from .env file (optional but recommended)
load_dotenv()

def main():
    # ---------- Convert XLS to XLSX using LibreOffice ----------
    def convert_with_libreoffice(folder: str):
        files_xls = Path(folder).glob("*.xls")

        for file in files_xls:
            try:
                subprocess.run([
                    #"soffice",
                    "/Applications/LibreOffice.app/Contents/MacOS/soffice",  
                    "--headless",
                    "--convert-to", "xlsx",
                    str(file),
                    "--outdir", str(file.parent)
                ], check=True)
                print(f"✅ Converted: {file.with_suffix('.xlsx').name}")
            except subprocess.CalledProcessError as e:
                print(f"❌ Conversion failed for {file.name}: {e}")
            except FileNotFoundError:
                print("❌ LibreOffice (soffice) not found in PATH.")

    convert_with_libreoffice("data/")

    # ---------- Connect to PostgreSQL ----------
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        port=os.getenv("DB_PORT", 5432)
    )
    cursor = conn.cursor()

    # ---------- File to Column Mapping ----------
    file_column_map = {
        "fattened_cattle.xlsx": "fattened_cattle",
        "rice.xlsx": "rice",
        "coffee.xlsx": "coffee",
        "dollar.xlsx": "dollar"
    }

    # ---------- Load each file and update the database ----------
    for filename, column in file_column_map.items():
        file_path = Path("data") / filename
        print(f"📄 Processing {filename}...") 

        if not file_path.exists():
            print(f"⚠️ File not found: {filename}")
            continue

        # Read the Excel file (skip metadata rows)
        df = pd.read_excel(file_path, skiprows=3465)
        #df = pd.read_excel(file_path, skiprows=3)
        df = df.iloc[:, :2]
        df.columns = ['date', 'price']
        df['date'] = pd.to_datetime(df['date'], dayfirst=True).dt.strftime('%Y-%m-%d')

        df['price'] = df['price'].astype(str) \
            .str.replace(".", "", regex=False) \
            .str.replace(",", ".", regex=False) \
            .astype(float)


        for _, row in df.iterrows():
            date = row['date']
            price = row['price']
            print(f"📌 Inserting: {date} - {column} = {price}")


            # Check if the date already exists
            cursor.execute("SELECT 1 FROM prices WHERE date = %s", (date,))
            exists = cursor.fetchone()

            if exists:
                # Update column
                cursor.execute(f"UPDATE prices SET {column} = %s WHERE date = %s", (price, date))
            else:
                # Insert new row with only one column
                cursor.execute(f"""
                    INSERT INTO prices (date, {column})
                    VALUES (%s, %s)
                    ON CONFLICT (date)
                    DO UPDATE SET {column} = EXCLUDED.{column}
                """, (date, price))

    conn.commit()
    cursor.close()
    conn.close()
    print("✅ Data successfully updated!")

if __name__ == "__main__":
    main()
