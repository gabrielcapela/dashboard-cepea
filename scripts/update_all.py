import subprocess

subprocess.run(["python", "scripts/cepea_scraper.py"])
subprocess.run(["python", "scripts/insert_data.py"])
subprocess.run(["python", "scripts/modeling.py"])
