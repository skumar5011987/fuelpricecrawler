# FuelPriceCrawler
 Fuel Price Crawler and API

Overview

This project is a Django-based solution designed to crawl daily updated fuel prices (petrol) from 'https://www.ndtv.com/fuel-prices', store them locally in a PostgreSQL database, and exposes API's to retrieve cities & fuel prices for a given city and state. The system is robust, scalable, and handles errors gracefully.

Main Features:

1. Crawl fuel prices from 'https://www.ndtv.com/fuel-prices' and store them in a local PostgreSQL database.
2. API to display petrol prices for a specific city and state over the last 7 days.
3. Custom Django management command to trigger the crawling process.
4. Celery task task scheduler to run management command daily.

Table of Contents:

1. Technologies Used
2. Installation and Setup
3. API Endpoints
4. Crawling Task
5. Custom Management Command
6. Task Scheduling
7. Caching
8. Error Handling

Technologies Used:

1. Python: 3.9+
2. Django: 4.x
3. PostgreSQL: 14.x or above
4. Celery: 5.x (for task scheduling)
5. Redis: 5.x (for caching and Celery)
7. BeautifulSoup4 & Selenium: For crawling

Installation and Setup:
1. Create a virtual environment:

    conda create -n venv python==3.11
    conda activate venv
    OR
    python -m venv venv
    source venv/bin/activate # On Windows: venv\Scripts\activate

2. Clone the repository:

    git clone 'https://github.com/skumar5011987/fuelpricecrawler.git'
    cd fuelpricecrawler

3. Install the dependencies:

    pip install -r requirements.txt

4. Set up PostgreSQL:

    Install PostgreSQL(14.+) and create a database
    Install PGAdmin4 for Database GUI for adimn

5. Update settings.py with your database configuration:

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'fuelprices',
            'USER': 'your-db-username',
            'PASSWORD': 'your-db-password',
            'HOST': 'localhost',
            'PORT': '5432',
        }
    }

6. Run migrations:

    python manage.py migrate

7. Start the development server:

    python manage.py runserver

8. Makesure redis is up and running:

    redis-cli ping
    PONG
    OR
    first install and run redis server
    Link: https://redis.io/docs/latest/operate/oss_and_stack/install/install-stack/

API Endpoints:

1. Home:

    URL: http://localhost:8000
    Method: GET
    Description: Welcome, Check Petrol price for all states and cities in India.

2. List Available Cities:

    URL: http://localhost:8000/list-cities
    Method: GET
    Description: Retrieves a list of all available cities for which fuel prices have been crawled.

3. Fuel Prices for a City/State:

    URL: http://localhost:8000/fuel-price
    Method: GET
    Description: Fetches the fuel prices for a given city and state over the last 7 days.
    Parameters:
        city (required)
        state (optional)
    
    Sample Response:
    {
    "city": "New Delhi",
    "state": "Delhi",
    "data": [
            {"date": "2023-08-01", "fuel": "petrol", "price": 96.23},
            {"date": "2023-08-02", "fuel": "petrol", "price": 96.50}
        ]
    }

Crawling Task:

    The crawling logic is handled by the CrawlAPIView, which fetches the petrol prices from the 'https://www.ndtv.com/fuel-prices' and stores the data in the FuelPrice model.
    Exception handling is implemented to ensure that the system skips pages or URLs that may not respond correctly.

Custom Management Command:

    Command Name: crawl_fuel_prices
    Trigger:
        python manage.py crawl_fuel_prices
    Description: Manually triggers the ndtv fuel price crawler.

Task Scheduling:

    To schedule the crawling task periodically, Celery is used.

Setup Celery:

    Celery & Redis get installed withe requirements or 
    Install Redis and Celery manually
        pip install redis celery

Start Celery worker:

    celery -A fuelpricecrwaler worker --pool=solo -l info

Start Celery Beat:

    celery -A fuelpricecrwaler beat -l info

Caching:

    To reduce frequent hits on the database for the same data, caching has been implemented using Redis. Make sure to install Redis and configure it in settings.py.

Error Handling:

    Stale Data Handling: The system handles stale data by verifying if the fuel price has already been stored for the current day before inserting new records.
    Exception Handling: Both the API and the crawling logic implement exception handling to gracefully manage any unforeseen issues during execution.
    Data Validation: The data is validated before inserting it into the database, ensuring only correct and meaningful data is stored.