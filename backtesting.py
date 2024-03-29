import requests
import pandas as pd
import yfinance as yf
from indicators import Indicators
from helperfunctions import trade, get_data
# import time
# import base64
# import hashlib

"""
base_url = "https://www.quantconnect.com/api/v2"

# Get timestamp
timestamp = str(int(time.time()))
time_stamped_token = "e83694bcdcdff310ddb71dffa8631d0e95cd1f9de28d583ae1596bf8188e2bd6" + ":" + timestamp

# Get hased API token
hashed_token = hashlib.sha256(time_stamped_token.encode("utf-8")).hexdigest()
authentication = "{}:{}".format(280243, hashed_token)
api_token = base64.b64encode(authentication.encode("utf-8")).decode("ascii")
"""
cash = 1000000
ticker_symbol = "MSFT"
data = yf.download(ticker_symbol, start='2007-01-01', end='2022-12-31')
data = data[["Adj Close"]]
data = data.rename(columns={"Adj Close": "Price"})

# print(data)

lst1 = [0,0,]
lst2 = [0,0,]
lst3 = [0,0,]
lst4 = [0,0,]
lst5 = [0,0,]
lst6 = [0,0,]
for i in range(1, len(data)):
    try:
        indicators = Indicators(data=data[:i], day="YESTERDAY")
        previous_indicators = Indicators(data=data[:i], day="DAY BEFORE YESTERDAY")
        rsi1 = indicators.count_rsi()
        rsi2 = previous_indicators.count_rsi()
        sma1 = indicators.short_term_ma
        # print(sma1)
        sma2 = previous_indicators.short_term_ma
        lma1 = indicators.long_term_ma
        lma2 = previous_indicators.long_term_ma
        # print(f"CIA {rsiv}")
        lst1.append(rsi1)
        lst2.append(rsi2)
        lst3.append(sma1)
        lst4.append(sma2)
        lst5.append(lma1)
        lst6.append(lma2)
    except:
        pass
data["RSI1"] = lst1
data["RSI2"] = lst2
data["sma1"] = lst3
data["sma2"] = lst4
data["lma1"] = lst5
data["lma2"] = lst6

trd = []
for i in range(len(data)):
    row = data.iloc[i]
    trdr = trade(row.RSI1,row.RSI2,row.sma1,row.sma2,row.lma1,row.lma2)
    trd.append(trdr)

data["t"] = trd
# print(max(data.lma1))
# for i in range(len(data)):
#     print(data.iloc[i])

pos = 0
l = []
for i in range(len(data)):
    row = data.iloc[i]
    if pos == 0 and row.t == 2:
        pos = 1
    elif pos == 0 and row.t == 1:
        pos = -1
    elif pos == 1 and row.t == 1:
        pos = -1
    elif pos == -1 and row.t == 2:
        pos = 1
    elif pos == 1 and row.t == -2:
        pos = 0
    elif pos == -1 and row.t == -1:
        pos = 0
    l.append(pos)

data["p"] = l
pp = 0
stocks = 0
stocks1 = 0
for i in range(1,len(data)):
    row = data.iloc[i]
    row1 = data.iloc[i-1]
    if row1.p == 0 and row.p == 1:
        stocks = cash / row.Price
        cash = 0
        stocks1 = 0
    elif row1.p == 1 and row.p == 0:
        cash = stocks * row.Price
        stocks = 0
        stocks1 = 0
    elif row1.p == 0 and row.p == -1:
        # shortina
        stocks1 = cash / row.Price
        cash = 2 * cash
        stocks = 0
    elif row1.p == -1 and row.p == 0:
        money = stocks1 * row.Price
        stocks1 = 0
        cash = cash - money
        stocks = 0
    elif row1.p == -1 and row.p == 1:
        money = stocks1 * row.Price
        cash = cash - money
        stocks = cash / row.Price 
        stocks1 = 0
        cash = 0
    elif row1.p == 1 and row.p == -1:
        cash = stocks * 2 * row.Price
        stocks1 = stocks
        stocks = 0

print(cash)
print(stocks)
print(stocks1)

    
    

# for i in range(len(data)):
#     print(data.iloc[i])
# print(data[data["t"]==1])
# print(data[data["t"]==-1])
# print(max(data["t"]))
# print(min(data["t"]))