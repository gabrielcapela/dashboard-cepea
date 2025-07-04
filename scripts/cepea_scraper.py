import time
import os
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# --- SETTINGS ---
DOWNLOAD_FOLDER = "data"
INPUT_ID = ["boi", "arroz", "cafe", "dolar"]
OUTPUT_FILES = ["fattened_cattle.xls", "rice.xls", "coffee.xls", "dollar.xls"]
RESOLUCAO = "Diário"

# --- DATES ---
begin = datetime.strptime("04/01/2016", "%d/%m/%Y")
current_date = datetime.today()
start_date = begin.strftime('%d/%m/%Y')
end_date = current_date.strftime('%d/%m/%Y')

# --- CHROME PATHS FOR RENDER ---
CHROME_BINARY_PATH = "/usr/bin/chromium"
CHROMEDRIVER_PATH = "/usr/bin/chromedriver"

# --- WEBDRIVER CONFIG ---
chrome_options = Options()
chrome_options.binary_location = CHROME_BINARY_PATH

chrome_options.add_experimental_option("prefs", {
    "download.default_directory": os.path.abspath(DOWNLOAD_FOLDER),
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "safebrowsing.enabled": True
})

chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# --- INIT DRIVER ---
service = Service(executable_path=CHROMEDRIVER_PATH)
driver = webdriver.Chrome(service=service, options=chrome_options)
wait = WebDriverWait(driver, 40)


# --- LOOP FOR EACH INPUT ---
for i in range(len(INPUT_ID)):
    driver.get("https://www.cepea.org.br/br/consultas-ao-banco-de-dados-do-site.aspx")

    # Wait for main scrollable input area to be present
    scroll_element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "imagenet-wrap-produtos-checkbox")))
    driver.execute_script("arguments[0].scrollTop = 0;", scroll_element)

    # --- SELECT INPUT ---
    input_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, f"label[for='{INPUT_ID[i]}']")))
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", input_button)
    input_button.click()

    # --- SELECT SUBTYPE ---
    subtype_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "label[for='subtipo-0']")))
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", subtype_button)
    subtype_button.click()

    # --- SELECT RESOLUTION ---
    resolution_button = wait.until(EC.element_to_be_clickable((By.XPATH, f"//label[text()='{RESOLUCAO}']")))
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", resolution_button)
    resolution_button.click()

    # --- START DATE ---
    wait.until(EC.element_to_be_clickable((By.ID, "periodo-de"))).click()
    year_sel = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#periodo-de_root select.picker__select--year")))
    year_sel.find_element(By.CSS_SELECTOR, f"option[value='{begin.year}']").click()
    month_sel = driver.find_element(By.CSS_SELECTOR, "#periodo-de_root select.picker__select--month")
    month_sel.find_element(By.CSS_SELECTOR, f"option[value='{begin.month - 1}']").click()
    xpath_start_day = f"//div[@id='periodo-de_root']//div[contains(@class, 'picker__day') and @aria-label='{start_date}']"
    wait.until(EC.element_to_be_clickable((By.XPATH, xpath_start_day))).click()

    # --- END DATE ---
    wait.until(EC.element_to_be_clickable((By.ID, "periodo-ate"))).click()
    end_year_sel = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#periodo-ate_root select.picker__select--year")))
    end_year_sel.find_element(By.CSS_SELECTOR, f"option[value='{current_date.year}']").click()
    end_month_sel = driver.find_element(By.CSS_SELECTOR, "#periodo-ate_root select.picker__select--month")
    end_month_sel.find_element(By.CSS_SELECTOR, f"option[value='{current_date.month - 1}']").click()
    xpath_end_day = f"//div[@id='periodo-ate_root']//div[contains(@class, 'picker__day') and @aria-label='{end_date}']"
    wait.until(EC.element_to_be_clickable((By.XPATH, xpath_end_day))).click()

    # --- GENERATE EXCEL ---
    btn_excel = wait.until(EC.element_to_be_clickable((By.ID, "adicionar")))
    btn_excel.click()

    download_link = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "imagenet-btn-download-excel")))
    driver.get(download_link.get_attribute("href"))
    time.sleep(3)

    # --- RENAME FILE ---
    files = os.listdir(DOWNLOAD_FOLDER)
    files.sort(key=lambda x: os.path.getmtime(os.path.join(DOWNLOAD_FOLDER, x)), reverse=True)
    old_path = os.path.join(DOWNLOAD_FOLDER, files[0])
    new_path = os.path.join(DOWNLOAD_FOLDER, OUTPUT_FILES[i])
    if os.path.exists(new_path): os.remove(new_path)
    os.rename(old_path, new_path)

# --- CLOSE DRIVER ---
driver.quit()
