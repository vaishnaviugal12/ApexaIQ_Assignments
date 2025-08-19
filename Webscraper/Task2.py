# Troemner OIML Weight Sets scraper (Selenium + Python)
# Outputs: troemner_oiml_weight_sets.csv with columns:
# vendor, productName, model, description, productURL, cost

import time
import re
import pandas as pd
from dataclasses import dataclass, asdict
from urllib.parse import urljoin

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

BASE_URL = "https://www.troemner.com"
CATEGORY_URL = "https://www.troemner.com/Calibration-Weights/Balance-Calibration-Weights/OIML-Calibration-Weight-Sets/c/3944"
EXPECTED_MODELS = 162


@dataclass
class ProductRow:
    vendor: str
    productName: str
    model: str
    description: str
    productURL: str
    cost: str


class TroemnerOIMLScraper:
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
        self.rows: list[ProductRow] = []

    def _dismiss_overlays(self):
        candidates = [
            (By.XPATH, "//button[contains(., 'Accept') or contains(., 'I Agree')]"),
            (By.CSS_SELECTOR, "button#onetrust-accept-btn-handler"),
            (By.CSS_SELECTOR, "button[aria-label='Accept cookies']"),
        ]
        for by, sel in candidates:
            try:
                el = self.wait.until(EC.element_to_be_clickable((by, sel)))
                el.click()
                time.sleep(0.5)
                break
            except Exception:
                pass

    def open_category(self):
        self.driver.get(CATEGORY_URL)
        self._dismiss_overlays()
        self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "ul#resultsList")))
        time.sleep(1.5)

    def _scroll_to_bottom(self):
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    def load_all_products(self):
        seen, stagnant_rounds = 0, 0
        while True:
            self._scroll_to_bottom()
            time.sleep(0.8)

            items = self.driver.find_elements(By.CSS_SELECTOR, "ul#resultsList > li.product-item")
            count = len(items)

            if count == seen:
                stagnant_rounds += 1
                if stagnant_rounds >= 2:
                    break
            else:
                seen, stagnant_rounds = count, 0

        print(f"Discovered {seen} product tiles on listing pages.")

    def _text_or_none(self, root, by, sel):
        try:
            return root.find_element(by, sel).text.strip()
        except Exception:
            return None

    def parse_products(self):
        cards = self.driver.find_elements(By.CSS_SELECTOR, "ul#resultsList > li.product-item")
        for li in cards:
            try:
                vendor = "troemner"

                model = li.get_attribute("data-code") or ""
                if not model:
                    code_text = self._text_or_none(li, By.CSS_SELECTOR, "span.code")
                    if code_text:
                        m = re.search(r"\(([^)]+)\)", code_text)
                        model = m.group(1) if m else code_text.strip()

                name_el = li.find_element(By.CSS_SELECTOR, "h3.title a")
                product_name = name_el.text.strip()
                href = name_el.get_attribute("href")
                product_url = urljoin(BASE_URL, href)

                description = self._text_or_none(li, By.CSS_SELECTOR, "div.description.product-description") or ""

                try:
                    cost = li.find_element(By.CSS_SELECTOR, "div.price span.priceValue").text.strip()
                except:
                    cost = "N/A"

                self.rows.append(ProductRow(
                    vendor=vendor,
                    productName=product_name,
                    model=model,
                    description=description,
                    productURL=product_url,
                    cost=cost
                ))
            except Exception as e:
                print(f"[warn] could not parse product card: {e}")

        print(f"Parsed {len(self.rows)} rows.")

    def save_csv(self, path: str = "troemner_oiml_weight_sets.csv"):
        df = pd.DataFrame([asdict(r) for r in self.rows])
        df.to_csv(path, index=False, encoding="utf-8")
        print(df.head())
        print(f" Saved {len(df)} rows to {path}")


def main():
    scraper = TroemnerOIMLScraper(headless=True)
    scraper.open_category()
    scraper.load_all_products()
    scraper.parse_products()
    if len(scraper.rows) != EXPECTED_MODELS:
        print(f"[note] Expected {EXPECTED_MODELS} models, got {len(scraper.rows)}.")
    scraper.save_csv()
    scraper.driver.quit()


if __name__ == "__main__":
    main()

