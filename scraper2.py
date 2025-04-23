import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

def scrape_company_details(input_csv="company_urls.csv", output_csv="company_data.csv"):
    # Set up Selenium options
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    # options.add_argument("--headless")  # Uncomment to run headless

    # Initialize the Chrome driver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    wait = WebDriverWait(driver, 20)

    # Read URLs and activities from the CSV file
    urls_activities = []
    with open(input_csv, "r", encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip header row if it exists
        urls_activities = [(row[0], row[1]) for row in reader if len(row) > 1]  # Get URL and activity

    all_data = []  # List to store dictionaries from each URL

    for url, activity in urls_activities:
        print(f"Processing: {url}")
        driver.get(url)
        
        try:
            wait.until(EC.presence_of_element_located((By.ID, "company-contact-information")))
        except Exception as e:
            print(f"Timeout or error for {url}: {e}")
            continue

        soup = BeautifulSoup(driver.page_source, "html.parser")
        
        data = {"Activity": activity}  # Store activity in data dictionary
        # Find all rows that contain label and value pairs
        rows = soup.find_all("div", class_="d-flex mb-1")
        for row in rows:
            label_div = row.find("div", class_="w-90px flex-shrink-0")
            value_div = row.find("div", class_="w-100 text-truncate text-dark font-weight-semibold")
            if label_div and value_div:
                label = label_div.get_text(strip=True)
                value = value_div.get_text(separator=" ", strip=True)
                data[label] = value

        # Optionally, print the extracted data for each URL for debugging
        for key, value in data.items():
            print(f"{key}: {value}")
        print("-" * 50)
        
        all_data.append(data)

    driver.quit()

    # Determine the union of all keys (in case not all pages have the same fields)
    fieldnames = set()
    for record in all_data:
        fieldnames.update(record.keys())
    fieldnames = list(fieldnames)

    # Write the collected data to a CSV file
    with open(output_csv, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for record in all_data:
            writer.writerow(record)

    print(f"Data saved to {output_csv}")
    return all_data