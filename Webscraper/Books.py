


from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

class BookScraper:
    def __init__(self, url):
        # Setup Chrome options
        options = webdriver.ChromeOptions()
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--headless")  # Optional: run in background

        # Initialize WebDriver
        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=options
        )

        self.url = url
        self.master_list = []

    def open_page(self):
        self.driver.get(self.url)
        time.sleep(2)  # Wait for page to load

    def scrape_books(self):
        # Locate all book elements using XPath
        books = self.driver.find_elements(By.XPATH, "//article[contains(@class, 'product_pod')]")

        # Extract data using dict comprehension
        self.master_list = [
            {
                "Title": book.find_element(By.XPATH, ".//h3/a").get_attribute("title"),
                "Price": book.find_element(By.XPATH, ".//p[contains(@class,'price_color')]").text,
                "Rating": book.find_element(By.XPATH, ".//p[contains(@class,'star-rating')]").get_attribute("class").replace("star-rating ", ""),
                "Link": book.find_element(By.XPATH, ".//h3/a").get_attribute("href")
            }
            for book in books
        ]

    def save_to_csv(self, filename="books.csv"):
        df = pd.DataFrame(self.master_list)
        df.to_csv(filename, index=False)
        print(df.head())

    def close(self):
        self.driver.quit()


if __name__ == "__main__":
    url = "https://books.toscrape.com/"
    scraper = BookScraper(url)
    scraper.open_page()
    scraper.scrape_books()
    scraper.save_to_csv()
    scraper.close()
