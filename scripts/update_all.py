from cepea_downloader import main as run_scraper
from insert_data import main as run_insert
from modeling import main as run_model
import os
from datetime import datetime

print("🛠️Starting the daily routine")

run_scraper()
print("✅ Scraping completed.")
run_insert()
print("✅ Inserting data completed.")
run_model()
print("✅ Modeling completed.")

print("✅ Update completed.")


github_user = os.getenv("GITHUB_USER")
github_token = os.getenv("GITHUB_TOKEN")

repo_url = f"https://{github_user}:{github_token}@github.com/gabrielcapela/dashboard-cepea.git"

# Atualiza o remote origin
os.system(f"git remote set-url origin {repo_url}")


# Send updates to GitHub
os.system("git config --global user.email 'gabrielcapela02@gmail.com'")
os.system("git config --global user.name 'gabrielcapela'")
os.system("git add .")
os.system(f"git commit -m 'automatic update: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}' || echo 'Nada para commitar'")
os.system("git push origin main")