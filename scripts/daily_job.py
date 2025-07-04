import time
import subprocess

def run_script(script_name):
    print(f"\n📌 Executando {script_name}...")
    result = subprocess.run(['python', script_name], capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print("⚠️ Erro:", result.stderr)

while True:
    print("⏰ Iniciando rotina diária do CEPEA...\n")
    
    run_script("cepea_scraper.py")
    run_script("insert_data.py")
    run_script("modeling.py")
    
    print("\n✅ Scripts executados com sucesso! Aguardando 24h...\n")
    time.sleep(86200)  # espera 24h
