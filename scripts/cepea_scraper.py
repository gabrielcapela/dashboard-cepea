import time
import os
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# --- SETTINGS---
DOWNLOAD_FOLDER = "data"
INPUT_ID = ["boi","arroz","cafe","dolar"]
#SUBTYPE = ["INDICADOR DO BOI GORDO CEPEA/ESALQ", "INDICADOR DO ARROZ EM CASCA CEPEA/IRGA-RS", "INDICADOR DO CAFÉ ARÁBICA CEPEA/ESALQ", "Dólar"]
OUTPUT_FILES = ["fattened_cattle.xls", "rice.xls", "coffee.xls", "dollar.xls"]
RESOLUCAO = "Diário"

#
# --- DATES ---
begin= datetime.strptime("04/01/2016", "%d/%m/%Y")  # fix date, 2016/01/04, 
current_date = datetime.today() 

start_date = begin.strftime('%d/%m/%Y')
end_date = current_date.strftime('%d/%m/%Y')

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



# --- LOOP FOR EACH INPUT ---
for i in range(len(INPUT_ID)):

    # --- ACCESS THE SITE ---
    driver.get("https://www.cepea.org.br/br/consultas-ao-banco-de-dados-do-site.aspx")
    driver.maximize_window()

    # --- SELECT PRODUCT ---
    # Scrolls to the top of the input selection window
    scroll_element = driver.find_element(By.CLASS_NAME, "imagenet-wrap-produtos-checkbox")
    driver.execute_script("arguments[0].scrollTop = 0;", scroll_element)

    # --- SELECT INPUT---
    input_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, f"label[for='{INPUT_ID[i]}']")))
    # Scroll to center the button on the screen
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


    

    # --- SELECT START DATE ("FROM") ---
    # Click on the start date field
    from_button = wait.until(EC.element_to_be_clickable((By.ID, "periodo-de")))
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", from_button)
    from_button.click()

    # Select the year
    begin_year = begin.year
    from_year_field = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#periodo-de_root select.picker__select--year")))
    from_year_field.click()
    from_year_field.find_element(By.CSS_SELECTOR, f"option[value='{begin_year}']").click()

     # Select the year
    begin_month = begin.month - 1  # january is 0 in picker
    from_month_field = driver.find_element(By.CSS_SELECTOR, "#periodo-de_root select.picker__select--month")
    from_month_field.click()
    from_month_field .find_element(By.CSS_SELECTOR, f"option[value='{begin_month}']").click()

    # Select the day
    xpath_begin_day = f"//div[@id='periodo-de_root']//div[contains(@class, 'picker__day') and @aria-label='{start_date}']"
    wait.until(EC.element_to_be_clickable((By.XPATH, xpath_begin_day))).click()


    # --- SELECT THE CURRENT DATA ("UNTIL") ---
    # ClicK in the current date field
    wait.until(EC.element_to_be_clickable((By.ID, "periodo-ate"))).click()

     # Select the year
    current_year = current_date.year
    until_year_field = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#periodo-ate_root select.picker__select--year")))
    until_year_field.click()
    until_year_field.find_element(By.CSS_SELECTOR, f"option[value='{current_year}']").click()

    # Select the month
    current_month = current_date.month - 1
    until_month_field = driver.find_element(By.CSS_SELECTOR, "#periodo-ate_root select.picker__select--month")
    until_month_field.click()
    until_month_field.find_element(By.CSS_SELECTOR, f"option[value='{current_month}']").click()

    # Select the day
    xpath_until_day = f"//div[@id='periodo-ate_root']//div[contains(@class, 'picker__day') and @aria-label='{end_date}']"
    wait.until(EC.element_to_be_clickable((By.XPATH, xpath_until_day))).click()




    # --- CLICK IN "GERAR EXCEL" ---
    btn_excel = wait.until(EC.element_to_be_clickable((By.ID, "adicionar")))
    btn_excel.click()

    # --- WAIT FOR THE DOWNLOAD BUTTON TO APPEAR ---
    download_link = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "imagenet-btn-download-excel")))
    download_url = download_link.get_attribute("href")

    # --- DOWNLOAD DIRECTLY ---
    print("⏳ Downloading...")
    driver.get(download_url)
    time.sleep(3)
    print("Download completed!")




    # --- RENAME THE DOWNLOADED FILE ---
    files = os.listdir(DOWNLOAD_FOLDER)
    files.sort(key=lambda x: os.path.getmtime(os.path.join(DOWNLOAD_FOLDER, x)), reverse=True)
    downloaded_file = files[0]
    old_path = os.path.join(DOWNLOAD_FOLDER, downloaded_file)
    new_path = os.path.join(DOWNLOAD_FOLDER, OUTPUT_FILES[i])

    # Remove previous file (if exists), then rename
    if os.path.exists(new_path):
        os.remove(new_path)
    os.rename(old_path, new_path)


    
        
driver.quit()