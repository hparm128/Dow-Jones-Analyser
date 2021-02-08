import requests
from bs4 import BeautifulSoup

dow = requests.get("https://finance.yahoo.com/quote/%5EDJI/components?p=%5EDJI").text
dow_soup = BeautifulSoup(dow, "html.parser")

dow_stocks = dow_soup.findAll(name="a")

for num in range(len(dow_stocks)):
    dow_stocks[num] = dow_stocks[num].getText()

stocks = dow_stocks[38:67]
