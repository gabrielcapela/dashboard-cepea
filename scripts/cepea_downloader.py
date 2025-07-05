import requests
import os
from datetime import datetime
import time

def download_cepea_excel(table_id, filename, start_date, end_date, resolution=1):
    """
    Sends a request to CEPEA and downloads the generated Excel file based on the returned JSON response.
    """
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Referer": "https://www.cepea.org.br/br/consultas-ao-banco-de-dados-do-site.aspx",
    }

    url = "https://www.cepea.org.br/br/consultas-ao-banco-de-dados-do-site.aspx"
    params = {
        "tabela_id": table_id,
        "data_inicial": start_date,
        "periodicidade": resolution,
        "data_final": end_date
    }

    print("📨 Requesting file generation...")
    response = requests.get(url, params=params, headers=headers)
    if response.status_code != 200:
        print("❌ Failed to contact CEPEA.")
        return

    try:
        data = response.json()
        excel_url = data["arquivo"].replace("\\/", "/")
        print(f"🔗 Excel file ready at: {excel_url}")
    except Exception as e:
        print(f"❌ Could not parse response: {e}")
        return

    # Download the Excel file
    excel_response = requests.get(excel_url, headers=headers)
    if excel_response.status_code == 200:
        os.makedirs("data", exist_ok=True)
        filepath = os.path.join("data", filename)
        with open(filepath, "wb") as f:
            f.write(excel_response.content)
        print(f"✅ Downloaded: {filepath}")
    else:
        print("❌ Failed to download the Excel file.")


def main():
    # --- Define CEPEA table IDs and output filenames --
    table_ids = [2, 91, 23, 'dolar']  # Example IDs for: cattle, rice, coffee, dollar
    output_files = ["fattened_cattle.xls", "rice.xls", "coffee.xls", "dollar.xls"]
    start_date = "04/01/2016"
    end_date = datetime.today().strftime("%d/%m/%Y")

    # --- Download loop ---
    for i in range(len(table_ids)):
        print(f"\n📥 Downloading {output_files[i]}...")
        download_cepea_excel(
            table_id=table_ids[i],
            filename=output_files[i],
            start_date=start_date,
            end_date=end_date,
            resolution=1
        )
        time.sleep(2)

if __name__ == "__main__":
    main()
    print("✅ All downloads completed.")