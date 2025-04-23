import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

# Set up Selenium options
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")

# Initialize Chrome driver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Read URLs and activities from CSV file
input_csv = "input_urls.csv"  # Change this to your actual CSV file
output_csv = "company_urls.csv"

# Open output CSV and write header
with open(output_csv, mode="w", encoding="utf-8", newline="") as out_file:
    writer = csv.writer(out_file)
    writer.writerow(["Small URL", "Activity"])  # Writing header

    # Read the input CSV file
    with open(input_csv, mode="r", encoding="utf-8") as in_file:
        reader = csv.reader(in_file)
        next(reader)  # Skip header if it exists
        
        for row in reader:
            if len(row) < 2:
                continue  # Skip invalid rows
            
            url_total, activity = row  # Get URL and activity
            print(f"Processing: {url_total} - Activity: {activity}")
            
            # Open URL in Selenium
            driver.get(url_total)
            wait = WebDriverWait(driver, 20)
            wait.until(EC.presence_of_element_located((By.CLASS_NAME, "stretched-link")))

            # Parse the page with BeautifulSoup
            soup = BeautifulSoup(driver.page_source, "html.parser")
            company_links = soup.find_all("a", class_="stretched-link")

            # Write extracted links to CSV
            for link in company_links:
                href = link.get("href")
                if href:
                    writer.writerow([href, activity])
                    print(f"Extracted: {href} - Activity: {activity}")

# Quit driver after processing all URLs
driver.quit()
print(f"Data extraction complete. URLs saved to {output_csv}")
