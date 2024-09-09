import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from crawler.utils import parse_price, parse_date

_logger = logging.getLogger(__name__)

base_url = "https://www.ndtv.com/fuel-prices"

chrome_options = Options()
chrome_options.add_argument("--headless") 
chrome_options.add_argument("--ignore-certificate-errors")

service = Service(ChromeDriverManager().install())
# service = Service(ChromeDriverManager(driver_version="128.0.6613.120").install())
driver = webdriver.Chrome(service=service, options=chrome_options)

def parse_page_url(city):
    city = "-".join(city.lower().split(" "))
    url = f"{base_url}/petrol-price-in-{city}-city"
    return url

def extract_fuelprice_history(city, source):
    
    state = source.find('span', class_="brdCrumb").find_all('a')[2].get_text()
    try:
        last10_days_fp_tbl = source.find_all('table')[0]
    except Exception as e:
        _logger.error(f"[Error]: Fuel Price History Not Available.")
    
    rows = last10_days_fp_tbl.find_all("tr")
    rows.pop(0)
    rec ={
        "city": city,
        "state": state,
        "data":[],
    }
    for row in rows[:7]:               
        tds = row.find_all('td')
        date = parse_date(tds[0].get_text())
        price = parse_price(tds[1].get_text())
        
        rec["data"].append({               
            "date": date,
            "price": price,
            "fuel": "petrol",
        })
    
    return rec

def get_page_content(page_url):
    
    # Load the page
    driver.get(page_url)
    WebDriverWait(driver, 2).until(
        EC.presence_of_element_located((By.CLASS_NAME, "city_selct"))
    )
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, "html.parser")
    
    return soup
    
def get_available_cities():
    CITIES = []
    
    content = get_page_content(base_url)
    city_dropdown = content.find(id="cdropdown")
    cities = city_dropdown.find_all("option")
    cities.pop(0)
    for city in cities:
        CITIES.append(city.get_text())
    
    return CITIES
