import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

def scrape_data(url):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Exécuter en arrière-plan
    options.add_argument("--start-maximized")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(url)

    wait = WebDriverWait(driver, 20)
    wait.until(EC.presence_of_element_located((By.ID, "company-contact-information")))

    soup = BeautifulSoup(driver.page_source, "html.parser")
    driver.quit()

    data = {}
    rows = soup.find_all("div", class_="d-flex mb-1")

    for row in rows:
        label_div = row.find("div", class_="w-90px flex-shrink-0")
        value_div = row.find("div", class_="w-100 text-truncate text-dark font-weight-semibold")
        if label_div and value_div:
            label = label_div.get_text(strip=True)
            value = value_div.get_text(separator=" ", strip=True)
            data[label] = value

    # Enregistrement dans un fichier CSV
    csv_filename = "one_page_scrape.csv"
    with open(csv_filename, "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = list(data.keys())
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerow(data)

    return data
