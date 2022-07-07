import requests
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import datetime
from datetime import timedelta
from fpdf import FPDF
import os
from dotenv import load_dotenv
import base64
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import (
    Mail, Attachment, FileContent, FileName, FileType, Disposition, ContentId)

load_dotenv()

CoinMarketCapKey = os.getenv("COIN_MARKET_CAP_KEY")
SendGridKey = os.getenv("SEND_GRID_KEY")

url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'

parameters = {
    'limit': '5000'
}

headers = {
    'X-CMC_PRO_API_KEY': CoinMarketCapKey
}

try:

    today = datetime.datetime.now()

    yesterday = str(today - timedelta(days=1))
    yesterday_datetime = yesterday

    currencies = []

    r = requests.get(url, params=parameters, headers=headers)
    data = r.json()

    for entry in data["data"]:
        symbol = entry["symbol"]
        date_added_str = entry["date_added"].replace(
            "T", " ").replace("Z", " ")

        if yesterday_datetime < date_added_str:
            currencies.append(symbol + ": " + date_added_str)
        else:
            pass

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=15)
    pdf.cell(200, 10, txt="New Cryptocurrencies on CoinMarketCap", ln=1, align='C')
    for text in currencies:
        pdf.cell(200, 10, txt=(text),
                 ln=20, align='C')
    pdf.output("NewCurrencies.pdf")

except (ConnectionError, Timeout, TooManyRedirects) as e:
    print(e)

message = Mail(
    from_email='tbz.testmail@gmail.com',
    to_emails='michel.studer@edu.tbz.ch',
    subject='New Crypto currrencies in the last 24 hours',
    html_content='<strong>See attachment for infos.</strong>'
)
file_path = 'NewCurrencies.pdf'
with open(file_path, 'rb') as f:
    data = f.read()
encoded = base64.b64encode(data).decode()
attachment = Attachment()
attachment.file_content = FileContent(encoded)
attachment.file_type = FileType('application/pdf')
attachment.file_name = FileName('NewCurrencies.pdf')
attachment.disposition = Disposition('attachment')
attachment.content_id = ContentId('PDF File')
message.attachment = attachment
try:
    sendgrid_client = SendGridAPIClient(SendGridKey)
    response = sendgrid_client.send(message)
except Exception as e:
    print(e.message)
