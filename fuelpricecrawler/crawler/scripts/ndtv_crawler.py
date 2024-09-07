from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from crawler.utils import parse_price, parse_date

base_url = "https://www.ndtv.com/fuel-prices"
CITIES = []
TARGET_URLS = []
DATA=[]
chrome_options = Options()
chrome_options.add_argument("--headless") 
chrome_options.add_argument("--ignore-certificate-errors")

service = Service(ChromeDriverManager().install())
# Initialize driver
driver = webdriver.Chrome(service=service, options=chrome_options)

def parse_page_url(city):
    city = "-".join(city.lower().split(" "))
    url = f"{base_url}/petrol-price-in-{city}-city"
    return url

def get_city(url):
    
    city = url.split("/")[-1].replace(f"petrol-price-in-", "").replace("-city", "")
    city = " ".join(city.split("-")).title()
    return city


def get_page_content(page_url):
    
    try:
        # Load the page
        driver.get(page_url)
        WebDriverWait(driver, 2).until(
            EC.presence_of_element_located((By.CLASS_NAME, "city_selct"))
        )
        # Get the page source
        page_source = driver.page_source
        # get page source
        soup = BeautifulSoup(page_source, "html.parser")
        return soup
    except Exception as e:
        print(f"Exception while crawling : {page_url}")
    
    
def crawl_fuelprices():
    content = get_page_content(base_url)
    city_dropdown = content.find(id="cdropdown") # target city dropdown menu
    cities = city_dropdown.find_all("option")  # get all city options
    cities.pop(0)
    for city in cities:
        CITIES.append(city.get_text())
    
    print(f"Cities:{CITIES}")
    for city in CITIES:
        url = parse_page_url(city)
        
        try:
            r = get_page_content(url)
            if r is None:
                continue
            
            print(f"[Info]: Crawling '{url}'")
            state = r.find('span', class_="brdCrumb").find_all('a')[2].get_text()
            last10_days_fp_tbl = r.find_all('table')[0]
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
            
            DATA.append(rec)
        except:
            continue
    return DATA
