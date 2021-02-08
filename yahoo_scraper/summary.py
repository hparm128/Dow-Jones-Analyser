import requests
from bs4 import BeautifulSoup
import dow

#ticker = input("Enter ticker symbol: ").upper()
dow_volumes = []

for stock in dow.stocks:
    summary = requests.get('https://finance.yahoo.com/quote/' + stock + '?p=' + stock).content
    summary_soup = BeautifulSoup(summary, "html.parser")

    summary_items = summary_soup.findAll(name="span")
    summary_items = summary_items[9::]

    for num in range(len(summary_items)):
        summary_items[num] = summary_items[num].getText()

    close_index = summary_items.index("Previous Close")
    target_index = summary_items.index("1y Target Est") + 1

    data = summary_items[close_index:target_index]

    data.remove("Forward Dividend & Yield")
    data.remove("Ex-Dividend Date")

    data_keys = data[::2]
    data_values = data[1::2]

    for num in range(len(data_values)):
        if "," in data_values[num]:
            data_values[num] = data_values[num].replace(",", "")
        if " " not in data_values[num] \
                and data_values[num] != "N/A" \
                and "B" not in data_values[num] \
                and "M" not in data_values[num] \
                and "T" not in data_values[num]:
            data_values[num] = float(data_values[num])

    zipped = zip(data_keys, data_values)
    data_table = dict(zipped)

    average_volume = data_table["Avg. Volume"]
    dow_volumes.append({stock: average_volume})
