from symtable import Symbol
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
from Keys import CoinMarketCapKey
import datetime
from datetime import date, timedelta

url = 'https://sandbox-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
parameters = {
    'start': '1',
    'limit': '5000',
    'convert': 'USD'
}
headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': CoinMarketCapKey,
}

session = Session()
session.headers.update(headers)

try:
    response = session.get(url, params=parameters)
    data = json.loads(response.text)

    today = date.today()
    yesterday = str(today - timedelta(days=1))
    yesterday_datetime = datetime.datetime.strptime(yesterday, '%Y-%m-%d')

    for entry in data["data"]:
        symbol = entry["symbol"]

        date_added_str = entry["date_added"][:10]
        date_added = datetime.datetime.strptime(date_added_str, '%Y-%m-%d')

        if yesterday_datetime < date_added:
            print(symbol + ": " + date_added_str)
        else:
            pass

except (ConnectionError, Timeout, TooManyRedirects) as e:
    print(e)
