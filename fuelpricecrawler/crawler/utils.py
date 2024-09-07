from decimal import Decimal
from datetime import datetime

def parse_date(date_str=""):
    if date_str:
        date_obj = datetime.strptime(date_str, '%b %d, %Y').date()
        return date_obj

def parse_price(price=""):
    p = price.split(" ")[0]
    return Decimal(p)