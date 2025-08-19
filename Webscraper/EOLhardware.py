# palo_alto_hardware_eol_scraper.py
# Outputs: palo_alto_hardware_eol.csv with normalized EOL_Date (yyyy-mm-dd)

import re
import time
import csv
from dataclasses import dataclass, asdict
from urllib.parse import urljoin
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

try:
    # optional: auto-manage chromedriver
    from webdriver_manager.chrome import ChromeDriverManager
    CHROMEDRIVER = ChromeDriverManager().install()
except Exception:
    CHROMEDRIVER = None

try:
    from dateutil import parser as dateparser
except ImportError:
    raise ImportError("Please install python-dateutil: pip install python-dateutil")

BASE_URL = "https://www.paloaltonetworks.com"
TARGET_URL = "https://www.paloaltonetworks.com/services/support/end-of-life-announcements/hardware-end-of-life-dates"


@dataclass
class Row:
    vendor: str
    productName: str
    EOL_Date: str
    resource: str
    Recommended_replacement: str


def _collapse(text: str) -> str:
    if not text:
        return ""
    return re.sub(r"\s+", " ", text).strip()


def _cell_text_lines(cell_el) -> str:
    inner = cell_el.get_attribute("innerText") or ""
    lines = [ln.strip() for ln in re.split(r"[\r\n]+", inner) if ln.strip()]
    return " | ".join(lines)


def _normalize_date(date_str: str) -> str:
    """
    Convert to yyyy-mm-dd if possible, otherwise return original (like 'TBD').
    """
    date_str = date_str.strip()
    if not date_str or date_str.lower() in {"tbd", "n/a", "-"}:
        return date_str

    try:
        dt = dateparser.parse(date_str, dayfirst=False, fuzzy=True)
        return dt.strftime("%Y-%m-%d")
    except Exception:
        return date_str


def make_driver(headless: bool = True, timeout: int = 20):
    opts = Options()
    if headless:
        opts.add_argument("--headless=new")
    opts.add_argument("--disable-gpu")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    opts.add_argument("--window-size=1400,900")
    opts.add_argument("--log-level=3")

    if CHROMEDRIVER:
        driver = webdriver.Chrome(service=Service(CHROMEDRIVER), options=opts)
    else:
        driver = webdriver.Chrome(options=opts)

    wait = WebDriverWait(driver, timeout)
    return driver, wait


def scrape(headless: bool = True, out_csv: str = "palo_alto_hardware_eol.csv"):
    driver, wait = make_driver(headless=headless)
    rows: list[Row] = []

    try:
        driver.get(TARGET_URL)

        # accept cookie banner if present
        for by, sel in [
            (By.CSS_SELECTOR, "button#onetrust-accept-btn-handler"),
            (By.XPATH, "//button[contains(., 'Accept')]"),
            (By.XPATH, "//button[contains(., 'I Agree')]"),
        ]:
            try:
                btn = WebDriverWait(driver, 4).until(
                    EC.element_to_be_clickable((by, sel))
                )
                btn.click()
                time.sleep(0.3)
                break
            except Exception:
                pass

        table = wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "table.table.table-striped.table-hover")
            )
        )

        tr_list = table.find_elements(By.CSS_SELECTOR, "tbody > tr")

        for tr in tr_list:
            tds = tr.find_elements(By.TAG_NAME, "td")
            if len(tds) < 6:
                continue

            product_name = _collapse(_cell_text_lines(tds[0]))
            eol_date_raw = _collapse(tds[2].text)
            eol_date = _normalize_date(eol_date_raw)

            links = tds[3].find_elements(By.TAG_NAME, "a")
            abs_links = []
            for a in links:
                href = a.get_attribute("href")
                if href:
                    abs_links.append(urljoin(BASE_URL, href))
            resource = " | ".join(abs_links)

            recommended = _collapse(_cell_text_lines(tds[5]))

            rows.append(
                Row(
                    vendor="Palo Alto",
                    productName=product_name,
                    EOL_Date=eol_date,
                    resource=resource,
                    Recommended_replacement=recommended,
                )
            )

        fieldnames = [
            "vendor",
            "productName",
            "EOL_Date",
            "resource",
            "Recommended_replacement",
        ]
        with open(out_csv, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for r in rows:
                writer.writerow(asdict(r))

        print(f"✅ Saved {len(rows)} rows to {out_csv}")

    finally:
        driver.quit()


if __name__ == "__main__":
    scrape(headless=True)
