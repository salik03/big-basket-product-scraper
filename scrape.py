import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
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

def scrape_data(update_progress):
    # Set up Selenium WebDriver once
    options = Options()
    options.add_argument('--headless')  # Run in headless mode
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    results = []
    num_products = len(products_list)
    for index, product in enumerate(products_list):
        query = product['product_name']
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
                results.append({
                    "Product Name": product['product_name'],
                    "Specification": specification,
                    "Unit": unit,
                    "Price": price,
                    "Date & Time of Collection": date_time
                })
            except NoSuchElementException:
                continue

        # Update progress bar
        update_progress((index + 1) / num_products)

    driver.quit()
    return pd.DataFrame(results)

def main():
    st.title("Product Scraper")

    # Button to start scraping
    if st.button("Start Scraping"):
        with st.spinner('Scraping data...'):
            # Show a progress bar
            progress_bar = st.progress(0)

            # Define a function to update progress
            def update_progress(progress):
                progress_bar.progress(progress)

            df = scrape_data(update_progress)

            # Ensure progress bar reaches 100%
            progress_bar.progress(1.0)

            if not df.empty:
                # Display the DataFrame in Streamlit
                st.dataframe(df)

                # Save the DataFrame to an Excel file in memory
                output = io.BytesIO()
                with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                    df.to_excel(writer, index=False)
                    writer.save()
                
                # Display a download button for the Excel file
                st.download_button(
                    label="Download data as Excel",
                    data=output.getvalue(),
                    file_name="product_data.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
            else:
                st.warning("No products found.")
    else:
        st.info("Click the button to start scraping.")

if __name__ == "__main__":
    main()
