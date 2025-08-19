# Palo Alto Software EOL scraper (Selenium + Python)
# Extracts: Software Name, Version, Release Date, EOL Date
# Output: paloalto_software_eol.csv

import time
import pandas as pd
from dataclasses import dataclass, asdict
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

try:
    from webdriver_manager.chrome import ChromeDriverManager
    CHROMEDRIVER = ChromeDriverManager().install()
except Exception:
    CHROMEDRIVER = None

URL = "https://www.paloaltonetworks.com/services/support/end-of-life-announcements/end-of-life-summary"


@dataclass
class SoftwareRow:
    softwareName: str
    version: str
    releaseDate: str
    eolDate: str


def normalize_date(date_str: str) -> str:
    """Convert date to yyyy-mm-dd if possible, else return original"""
    if not date_str:
        return ""
    try:
        return datetime.strptime(date_str.strip(), "%B %d, %Y").strftime("%Y-%m-%d")
    except Exception:
        try:
            return datetime.strptime(date_str.strip(), "%b %d, %Y").strftime("%Y-%m-%d")
        except Exception:
            return date_str.strip()


class PaloAltoSoftwareScraper:
    def __init__(self, headless: bool = True, timeout: int = 20):
        chrome_opts = Options()
        if headless:
            chrome_opts.add_argument("--headless=new")
        chrome_opts.add_argument("--disable-gpu")
        chrome_opts.add_argument("--no-sandbox")
        chrome_opts.add_argument("--window-size=1400,900")
        chrome_opts.add_argument("--disable-dev-shm-usage")
        chrome_opts.add_argument("--start-maximized")
        chrome_opts.add_argument("--log-level=3")

        if CHROMEDRIVER:
            self.driver = webdriver.Chrome(service=Service(CHROMEDRIVER), options=chrome_opts)
        else:
            self.driver = webdriver.Chrome(options=chrome_opts)

        self.wait = WebDriverWait(self.driver, timeout)
        self.rows: list[SoftwareRow] = []

    def open_page(self):
        self.driver.get(URL)
        #  Wait for tables
        self.wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.oneColumnPlain table")))
        time.sleep(1.5)

    def parse_tables(self):
        tables = self.driver.find_elements(By.CSS_SELECTOR, "div.oneColumnPlain table")

        for table in tables:
            try:
                software_name = "Unknown Software"

                # 🔹 Try different possible heading formats in order
                try:
                    heading = table.find_element(By.CSS_SELECTOR, "th[colspan] p b")
                    software_name = heading.text.strip()
                except Exception:
                    try:
                        heading = table.find_element(By.CSS_SELECTOR, "td[colspan] p b")
                        software_name = heading.text.strip()
                    except Exception:
                        try:
                            heading = table.find_element(By.XPATH, "./preceding::p[1]/b")
                            software_name = heading.text.strip()
                        except Exception:
                            try:
                                heading = table.find_element(By.XPATH, "./preceding::h2[1] | ./preceding::h3[1]")
                                software_name = heading.text.strip()
                            except Exception:
                                pass

                # Extract table rows
                rows = table.find_elements(By.CSS_SELECTOR, "tbody tr")
                for row in rows:
                    cols = [td.text.strip() for td in row.find_elements(By.TAG_NAME, "td")]
                    # skip header rows
                    if len(cols) >= 3 and cols[0] != "Version":
                        version = cols[0]
                        release_date = normalize_date(cols[1])
                        eol_date = normalize_date(cols[2])
                        self.rows.append(SoftwareRow(
                            softwareName=software_name,
                            version=version,
                            releaseDate=release_date,
                            eolDate=eol_date
                        ))
            except Exception as e:
                print(f"[warn] failed to parse table: {e}")

        print(f"Parsed {len(self.rows)} rows from {len(tables)} tables.")

    def save_csv(self, path: str = "paloalto_software_eol.csv"):
        df = pd.DataFrame([asdict(r) for r in self.rows])
        df.to_csv(path, index=False, encoding="utf-8")
        print(df.head())
        print(f" Saved {len(df)} rows to {path}")


def main():
    scraper = PaloAltoSoftwareScraper(headless=True)
    scraper.open_page()
    scraper.parse_tables()
    scraper.save_csv()
    scraper.driver.quit()


if __name__ == "__main__":
    main()
