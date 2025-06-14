import time
import os
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# --- CONFIGURAÇÕES ---
DOWNLOAD_FOLDER = os.path.join(os.path.dirname(__file__), "../data")
INSUMO_ID = ["boi","arroz","cafe","dolar"]
#SUBTIPO = ["INDICADOR DO BOI GORDO CEPEA/ESALQ", "INDICADOR DO ARROZ EM CASCA CEPEA/IRGA-RS", "INDICADOR DO CAFÉ ARÁBICA CEPEA/ESALQ", "Dólar"]
ARQUIVOS_SAIDA = ["fattened_cattle.xls", "rice.xls", "coffee.xls", "dollar.xls"]
RESOLUCAO = "Diário"

#
# --- DATAS ---
inicio = datetime.strptime("04/01/2016", "%d/%m/%Y")  # Data fixa
fim = datetime.today()  # Data atual

data_inicio_br = inicio.strftime('%d/%m/%Y')
data_fim_br = fim.strftime('%d/%m/%Y')

# --- WEBDRIVER ---
chrome_options = Options()
#chrome_options.add_argument("--window-size=1920x1080")
chrome_options.add_experimental_option("prefs", {
    "download.default_directory": os.path.abspath(DOWNLOAD_FOLDER),
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "safebrowsing.enabled": True
})
driver = webdriver.Chrome(options=chrome_options)
wait = WebDriverWait(driver, 40)



# --- LOOP PARA CADA INSUMO ---
for i in range(len(INSUMO_ID)):

    # --- ACESSA O SITE ---
    driver.get("https://www.cepea.org.br/br/consultas-ao-banco-de-dados-do-site.aspx")
    driver.maximize_window()

    # --- SELECIONA PRODUTO ---

    # Rola para o topo da janela seletora dos insumos
    elemento_scroll = driver.find_element(By.CLASS_NAME, "imagenet-wrap-produtos-checkbox")
    driver.execute_script("arguments[0].scrollTop = 0;", elemento_scroll)

    # --- SELECIONA O INSUMO ---
    botao_insumo = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, f"label[for='{INSUMO_ID[i]}']")))
    # Dá scroll para centralizar o botão na tela
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", botao_insumo)
    botao_insumo.click()

    # --- SELECIONA SUBTIPO ---
    botao_subtipo = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "label[for='subtipo-0']")))
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", botao_subtipo)
    botao_subtipo.click()


    

    # --- SELECIONA RESOLUÇÃO ---
    botao_resolucao = wait.until(EC.element_to_be_clickable((By.XPATH, f"//label[text()='{RESOLUCAO}']")))
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", botao_resolucao )
    botao_resolucao.click()

    # --- SELECIONA DATA DE INÍCIO ("DE") ---
    # Clica no campo de data inicial
    botao_de = wait.until(EC.element_to_be_clickable((By.ID, "periodo-de")))
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", botao_de)
    botao_de.click()
    # Seleciona o ano
    ano_inicio = inicio.year
    campo_ano_de = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#periodo-de_root select.picker__select--year")))
    campo_ano_de.click()
    campo_ano_de.find_element(By.CSS_SELECTOR, f"option[value='{ano_inicio}']").click()

    # Seleciona o mês
    mes_inicio = inicio.month - 1  # janeiro é 0 no picker
    campo_mes_de = driver.find_element(By.CSS_SELECTOR, "#periodo-de_root select.picker__select--month")
    campo_mes_de.click()
    campo_mes_de.find_element(By.CSS_SELECTOR, f"option[value='{mes_inicio}']").click()

    # Seleciona o dia
    xpath_dia_inicio = f"//div[@id='periodo-de_root']//div[contains(@class, 'picker__day') and @aria-label='{data_inicio_br}']"
    wait.until(EC.element_to_be_clickable((By.XPATH, xpath_dia_inicio))).click()


    # --- SELECIONA DATA DE FIM ("ATÉ") ---
    # Clica no campo de data final
    wait.until(EC.element_to_be_clickable((By.ID, "periodo-ate"))).click()

    # Seleciona o ano
    ano_fim = fim.year
    campo_ano_ate = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#periodo-ate_root select.picker__select--year")))
    campo_ano_ate.click()
    campo_ano_ate.find_element(By.CSS_SELECTOR, f"option[value='{ano_fim}']").click()

    # Seleciona o mês
    mes_fim = fim.month - 1
    campo_mes_ate = driver.find_element(By.CSS_SELECTOR, "#periodo-ate_root select.picker__select--month")
    campo_mes_ate.click()
    campo_mes_ate.find_element(By.CSS_SELECTOR, f"option[value='{mes_fim}']").click()

    # Seleciona o dia
    xpath_dia_fim = f"//div[@id='periodo-ate_root']//div[contains(@class, 'picker__day') and @aria-label='{data_fim_br}']"
    wait.until(EC.element_to_be_clickable((By.XPATH, xpath_dia_fim))).click()







    # --- CLICA EM "GERAR EXCEL" ---
    btn_excel = wait.until(EC.element_to_be_clickable((By.ID, "adicionar")))
    btn_excel.click()

    # --- AGUARDA BOTÃO DE DOWNLOAD APARECER ---
    download_link = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "imagenet-btn-download-excel")))
    download_url = download_link.get_attribute("href")

    # --- FAZ O DOWNLOAD DIRETAMENTE ---
    print("⏳ Baixando arquivo...")
    driver.get(download_url)
    time.sleep(3)
    print("✅ Download concluído!")




    # --- RENOMEIA O ARQUIVO BAIXADO ---
    arquivos = os.listdir(DOWNLOAD_FOLDER)
    arquivos.sort(key=lambda x: os.path.getmtime(os.path.join(DOWNLOAD_FOLDER, x)), reverse=True)
    arquivo_baixado = arquivos[0]
    caminho_antigo = os.path.join(DOWNLOAD_FOLDER, arquivo_baixado)
    caminho_novo = os.path.join(DOWNLOAD_FOLDER, ARQUIVOS_SAIDA[i])

    # Remove arquivo anterior (se existir), depois renomeia
    if os.path.exists(caminho_novo):
        os.remove(caminho_novo)
    os.rename(caminho_antigo, caminho_novo)


    
        
driver.quit()