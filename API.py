# This example uses Python 2.7 and the python-request library.
import time
from requests import Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json

url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/trending/latest"
parameters = {
    "time_period": "12h",
    "convert": "USD"
}
headers = {
    "Accepts": "application/json",
    "X-CMC_PRO_API_KEY": "API KEY",
}

session = Session()
session.headers.update(headers)

while True:
    try:
        response = session.get(url, params=parameters)
        data = json.loads(response.text)
        price = data["data"][10]["quote"]["USD"]["price"]
        print(price)

    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)
    time.sleep(5)
