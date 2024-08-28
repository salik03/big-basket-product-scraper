import streamlit as st
import pandas as pd
import requests
import io

def main():
    st.title("Product Scraper")

    # Placeholder to display the scraped data incrementally
    data_placeholder = st.empty()

    # Placeholder for the progress bar
    progress_text = st.empty()

    # Button to start scraping
    if st.button("Start Scraping"):
        progress_bar = st.progress(0)

        response = requests.get("https://product-scraper-tlp5.onrender.com/scrape")

        if response.status_code == 200:
            results = response.json()
            df = pd.DataFrame(results)

            # Incremental display of data
            for i, row in df.iterrows():
                progress_bar.progress((i + 1) / len(df))
                data_placeholder.dataframe(df.iloc[:i + 1])

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
        else:
            st.error("Failed to retrieve data from the API.")

if __name__ == "__main__":
    main()
