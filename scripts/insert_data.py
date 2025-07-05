import sqlite3
import pandas as pd
from pathlib import Path


def main():
    ################# CONVERT FILES WITH LIBRE OFFICE ##############
    import subprocess
    def converte_with_libreoffice(fold: str):
        files_xls = Path(fold).glob("*.xls")

        for files in files_xls:
            try:
                subprocess.run([
                    "/Applications/LibreOffice.app/Contents/MacOS/soffice",  # COMPLETE PATH
                    "--headless",
                    "--convert-to", "xlsx",
                    str(files),
                    "--outdir", str(files.parent)
                ], check=True)
                print(f"✅ Sucess: {files.with_suffix('.xlsx').name}")
            except subprocess.CalledProcessError as e:
                print(f"❌ Fail  {files.name}: {e}")

    #Execute
    converte_with_libreoffice("data/")
    #####################################################


    # Connect to the SQLite database
    conn = sqlite3.connect("data/cepea.db")
    cursor = conn.cursor()

    # Map Excel filenames to database column names
    file_column_map = {
        "fattened_cattle.xlsx": "fattened_cattle",
        "rice.xlsx": "rice",
        "coffee.xlsx": "coffee",
        "dollar.xlsx": "dollar"
    }

    # Loop through each Excel file and update the corresponding column
    for filename, column in file_column_map.items():
        file_path = Path("data") / filename

        # Read the Excel file, skipping the first 3 rows
        df = pd.read_excel(file_path, skiprows=3)

        # Rename the first two columns to standard names
        df = df.iloc[:, :2]  # select only the first two columns
        df.columns = ['date', 'price']  # rename columns for consistency

        # Convert 'data' column to string format dd/mm/yyyy
        df['date'] = pd.to_datetime(df['date'], dayfirst=True).dt.strftime('%Y-%m-%d')


        # Iterate over rows and update or insert into the database
        for _, row in df.iterrows():
            date = row['date']
            price = row['price']

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

    print("Data successfully updated!")

if __name__ == "__main__":
    main()
   