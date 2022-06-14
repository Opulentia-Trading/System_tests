#from fcntl import F_SEAL_SEAL
import json
from math import ceil
import requests
from matplotlib import pyplot as plt, dates as mdates
from datetime import datetime

url = "https://fapi.binance.com/fapi/v1/fundingRate"

payload = {
    "symbol": "BTCUSDT",
    # "startTime": 1000,
    # "endTime": 1010,
    "limit": 500
}

res = requests.get(url, params=payload)

x_axis = []
y_axis = []
for data in res.json():
    x_axis.append(datetime.fromtimestamp(data['fundingTime']/1000.0))
    y_axis.append(float(data['fundingRate']))


ax = plt.gca()
formatter = mdates.DateFormatter("%Y-%m-%d %H")
ax.xaxis.set_major_formatter(formatter)
ax.xaxis.set_major_locator(mdates.HourLocator(byhour=[3, 11, 19]))
plt.plot(x_axis, y_axis)
plt.xlabel('Datetime of funding rate')
plt.ylabel('Funding rate')
plt.show()
