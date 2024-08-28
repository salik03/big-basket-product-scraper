from flask import Flask, jsonify
from flask_cors import CORS
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import chromedriver_autoinstaller
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Ensure ChromeDriver is installed
chromedriver_autoinstaller.install()

# List of predefined products
products_list = [
    {"product_name": "Rice"},
    {"product_name": "Wheat"},
    {"product_name": "Jowar"},
    {"product_name": "Tomato"},
    {"product_name": "Potato"},
    {"product_name": "Onion"},
    {"product_name": "Garlic"},
    {"product_name": "Ginger"},
    {"product_name": "Sugar"},
    {"product_name": "Tea-leaf"},
    {"product_name": "Coffee Powder"}
]

@app.route('/scrape', methods=['GET'])
def scrape_data():
    # Set up Chrome options for headless operation
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.binary_location = "/opt/chrome/google-chrome"

    # Initialize WebDriver
    driver = webdriver.Chrome(options=options)
    
    results = []
    
    for product in products_list:
        query = product['product_name']
        
        try:
            driver.get(f"https://www.bigbasket.com/ps/?q={query}")

            wait = WebDriverWait(driver, 10)
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'li.PaginateItems___StyledLi-sc-1yrbjdr-0.dDBqny')))

            items_list = driver.find_elements(By.CSS_SELECTOR, 'li.PaginateItems___StyledLi-sc-1yrbjdr-0.dDBqny')

            for item in items_list:
                try:
                    company = item.find_element(By.CSS_SELECTOR, "span.BrandName___StyledLabel2-sc-hssfrl-1.gJxZPQ.keQNWn").text
                    specification = item.find_element(By.CSS_SELECTOR, "div.break-words.h-10.w-full h3").text
                    unit = item.find_element(By.CSS_SELECTOR, "span.PackChanger___StyledLabel-sc-newjpv-1.gJxZPQ.cWbtUx").text
                    price = item.find_element(By.CSS_SELECTOR, "span.Pricing___StyledLabel-sc-pldi2d-1.gJxZPQ.AypOi").text
                    date_time = datetime.now().strftime("%d.%m.%Y %H:%M")

                    result = {
                        "Product Name": product['product_name'],
                        "Company": company,
                        "Specification": specification,
                        "Unit": unit,
                        "Price": price,
                        "Date & Time of Collection": date_time
                    }
                    results.append(result)
                except NoSuchElementException:
                    continue
        except (TimeoutException, Exception):
            continue
    
    driver.quit()
    
    return jsonify(results)

if __name__ == "__main__":
    app.run(debug=True)
