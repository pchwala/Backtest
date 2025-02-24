import json
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timezone
import mplfinance as mpf
import pandas as pd
import talib
import vectorbt as vbt
from tests.test_portfolio import entries
import numpy as np


def fit_ind(close, volume, ema1_period=5, ema2_period=8, ema3_period=13, rsi_period=14):
    close = close.flatten()

    ema1 = talib.EMA(close, timeperiod=ema1_period)
    ema2 = talib.EMA(close, timeperiod=ema2_period)
    ema3 = talib.EMA(close, timeperiod=ema3_period)
    ema200 = talib.EMA(close, timeperiod=200)

    macd, macd_signal, macd_hist = talib.MACD(close, fastperiod=12, slowperiod=26, signalperiod=9)
    rsi = talib.RSI(close, rsi_period)

    value = [0] * len(close)
    trade_open = 0
    mean_volume = volume.mean()
    print(mean_volume)
    for n in range(len(close)):
        try:
            if volume[n] > 2*mean_volume and ema1[n] < ema3[n] and trade_open == 0:
                value[n] = -2
                trade_open = -2
            elif ema1[n] > ema2[n] and trade_open == -2:
                value[n] = 2
                trade_open = 0
            else:
                value[n] = 0

        except:
            value[n] = 0

    return value


def random_pf(close):
    value = [0] * len(close)
    for n in range(len(close)):
        value[n] = np.random.randint(-100, 100)

    return value

with open("us100_5m_data.json", "r") as datafile:
    raw_data = json.load(datafile)
    raw_data = raw_data['returnData']
    raw_data = raw_data['rateInfos']

# Convert JSON data to DataFrame and Series
df_data = []
us100_price = {} # Dictionary
us100_volume = []
for entry in raw_data:
    timestamp = datetime.fromtimestamp(entry["ctm"] / 1000, timezone.utc)
    open_price = entry["open"] / 100
    close_price = open_price + entry["close"] / 100
    high = open_price + entry["high"] / 100
    low = open_price + entry["low"] / 100
    volume = entry["vol"]

    df_data.append([timestamp, open_price, high, low, close_price, volume])
    us100_price[timestamp] = close_price # Store close_price in dictionary
    us100_volume.append(volume) # Store volume in a list

df = pd.DataFrame(df_data, columns=["Date", "Open", "High", "Low", "Close", "Volume"])
df.set_index("Date", inplace=True)

# Keep only last 100 candles
df = df.tail(100)

# Plot candlestick chart
#mpf.plot(df, type='candle', style='charles', volume=False, title="Candlestick Chart", ylabel="Price")
#plt.show()

# Convert dictionary to a pandas Series
us100_price = pd.Series(us100_price, name="Close Price")
us100_volume = pd.Series(us100_volume, name="Volume")
# Keep only last 1000 records
#us100_price = us100_price[-1000:]


ind_fit = vbt.IndicatorFactory(
    class_name = "3 EMA Crossover",
    short_name = "3ema",
    input_names = ["close"],
    param_names = ["volume", "ema1_period", "ema2_period", "ema3_period", "rsi_period"],
    output_names = ["value"]
    ).from_apply_func(
        fit_ind,
        ema1_period = 5,
        ema2_period = 8,
        ema3_period = 13,
        rsi_period = 14
        )

#res = ind_fit.run(us100_price, ema1_period=5, ema2_period=8, ema3_period=13)
#res = ind_random.run(us100_price)

#print(res.value.to_string())

res = ind_fit.run(us100_price, us100_volume, ema1_period=5, ema2_period=8, ema3_period=13, rsi_period=14)
entries = res.value == 1
exits = res.value == -1
short_entries = res.value == -2
short_exits = res.value == 2

pf = vbt.Portfolio.from_signals(
    us100_price,
    entries = entries,
    exits = exits,
    short_entries = short_entries,
    short_exits = short_exits
)
pf.plot().show()