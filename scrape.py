import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import pandas as pd
import io
from datetime import datetime

# List of predefined products with name only (specification removed)
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

def scrape_data(update_progress, update_data_display):
    # Set up Selenium WebDriver once
    options = Options()
    # options.add_argument('--headless')  # Run in headless mode
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    results = []
    num_products = len(products_list)
    
    for index, product in enumerate(products_list):
        query = product['product_name']
        
        try:
            driver.get(f"https://www.bigbasket.com/ps/?q={query}")

            # Wait for the elements to load
            wait = WebDriverWait(driver, 10)  # 10 seconds wait time
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'li.PaginateItems___StyledLi-sc-1yrbjdr-0.dDBqny')))

            # Extract product data
            items_list = driver.find_elements(By.CSS_SELECTOR, 'li.PaginateItems___StyledLi-sc-1yrbjdr-0.dDBqny')

            for item in items_list:
                try:
                    company = item.find_element(By.CSS_SELECTOR, "span.BrandName___StyledLabel2-sc-hssfrl-1.gJxZPQ.keQNWn").text
                    specification = item.find_element(By.CSS_SELECTOR, "div.break-words.h-10.w-full h3").text
                    unit = item.find_element(By.CSS_SELECTOR, "span.PackChanger___StyledLabel-sc-newjpv-1.gJxZPQ.cWbtUx").text
                    price = item.find_element(By.CSS_SELECTOR, "span.Pricing___StyledLabel-sc-pldi2d-1.gJxZPQ.AypOi").text

                    # Get the current date and time
                    date_time = datetime.now().strftime("%d.%m.%Y %H:%M")

                    # Append to the results list
                    result = {
                        "Product Name": product['product_name'],
                        "Company": company,
                        "Specification": specification,
                        "Unit": unit,
                        "Price": price,
                        "Date & Time of Collection": date_time
                    }
                    results.append(result)

                    # Update the display incrementally with the current product
                    update_data_display(pd.DataFrame([result]))

                except NoSuchElementException:
                    continue

        except (TimeoutException, Exception):
            continue

        # Update progress bar with +1% increment
        update_progress((index + 1) / num_products)

    driver.quit()
    return pd.DataFrame(results)

def main():
    st.title("Product Scraper")

    # Placeholder to display the scraped data incrementally
    data_placeholder = st.empty()

    # Placeholder for the progress bar
    progress_text = st.empty()

    # Button to start scraping
    if st.button("Start Scraping"):
        progress_bar = st.progress(0)

        # Function to update progress
        def update_progress(progress):
            progress_percentage = int(progress * 100)
            progress_bar.progress(progress_percentage)
            progress_text.text(f"Progress: {progress_percentage}%")

        # Function to update the data display incrementally
        def update_data_display(new_data):
            data_placeholder.dataframe(new_data, height=1)  # Adjust height as needed

        # Scrape the data
        df = scrape_data(update_progress, update_data_display)

        # Ensure progress bar reaches 100%
        progress_bar.progress(100)
        progress_text.text("Scraping completed!")

        # Display the number of products scraped
        num_scraped_products = len(df)
        st.write(f"Total products scraped: {num_scraped_products}")

        if not df.empty:
            # Allow user to download the complete dataset
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                df.to_excel(writer, index=False)
                writer.save()

            st.download_button(
                label="Download data as Excel",
                data=output.getvalue(),
                file_name="product_data.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        else:
            st.warning("No products found.")

if __name__ == "__main__":
    main()
