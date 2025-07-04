from cepea_scraper import main as run_scraper
from insert_data import main as run_insert
from modeling import main as run_model


print("🛠️Starting the daily routine")

run_scraper()
print("✅ Scraping completed.")
run_insert()
print("✅ Inserting data completed.")
run_model()
print("✅ Modeling completed.")

print("✅ Update completed.")
