import requests
from bs4 import BeautifulSoup

from summary import dow_volumes

good_with_volume = 0
bad_with_volume = 0

for num in range(len(dow_volumes)):
    ticker = dow_volumes[num].keys()
    ticker = list(ticker)
    ticker = ticker[0]

    print(ticker)

    values = dow_volumes[num].values()
    values = list(values)
    average_volume = values[0]

    history = requests.get('https://finance.yahoo.com/quote/' + ticker + '/history?p=' + ticker).content
    history_soup = BeautifulSoup(history, "html.parser")

    history_items = history_soup.findAll(name="span")

    for num in range(len(history_items)):
        history_items[num] = history_items[num].getText()

    last_month = history_items[63:224]
    print(last_month)

    for num in range(len(last_month)):
        if "," in last_month[num]:
            last_month[num] = last_month[num].replace(",", "")

    if "Dividend" in last_month:
        dividend_location = last_month.index("Dividend")
        last_month.pop(dividend_location-1)
        last_month.remove("Dividend")

    last_month_volumes = last_month[6::7]
    last_month_opens = last_month[1::7]
    last_month_closes = last_month[4::7]

    days = int(len(last_month) / 7)

    for num in range(days):
        if float(last_month_opens[num]) < float(last_month_closes[num]):
            if float(last_month_volumes[num]) > float(average_volume):
                good_with_volume += 1

        elif float(last_month_opens[num]) > float(last_month_closes[num]):
            if float(last_month_volumes[num]) > float(average_volume):
                bad_with_volume += 1

    if good_with_volume >= 3 and bad_with_volume <= 3:
        print(ticker.upper() + ": Good Volume!")
    else:
        print(ticker.upper() + ": Bad Volume")
