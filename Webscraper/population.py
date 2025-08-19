from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

class PopulationScraper:
    def __init__(self, url):
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--window-size=1920,1080")
        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=options
        )
        self.url = url
        self.master_list = []

    def scrape_table(self):
        self.driver.get(self.url)

        # Wait until the first table appears
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//table[contains(@class,"wikitable")][1]'))
        )

        # Locate all rows in the first wikitable
        rows = self.driver.find_elements(
            By.XPATH, '//table[contains(@class,"wikitable")][1]//tbody/tr'
        )

        for i, row in enumerate(rows, start=1):
            cols = row.find_elements(By.XPATH, './/th | .//td')

            # Skip header/empty rows
            if len(cols) < 5:
                continue

            country = cols[0].text.strip()
            population = cols[1].text.strip()
            world_share = cols[2].text.strip()
            date = cols[3].text.strip()
            source = cols[4].text.strip()

            self.master_list.append({
                "Rank": len(self.master_list) + 1,  # Auto-generated rank
                "Country": country,
                "Population": population,
                "World Share": world_share,
                "Date": date,
                "Source": source
            })

    def save_to_csv(self, filename="countries_population.csv"):
        df = pd.DataFrame(self.master_list)
        df.to_csv(filename, index=False, encoding="utf-8")
        print(df.head())

    def close(self):
        self.driver.quit()


if __name__ == "__main__":
    url = "https://en.wikipedia.org/wiki/List_of_countries_and_dependencies_by_population"
    scraper = PopulationScraper(url)
    scraper.scrape_table()
    scraper.save_to_csv()
    scraper.close()
