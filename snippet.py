# Define ticker for EUR/USD
ticker = "EURUSD=X"

# Define time range
end_date = datetime.today().strftime("%Y-%m-%d")
start_date = (datetime.today() - timedelta(days=7)).strftime("%Y-%m-%d")

# Fetch 5-minute data
df = yf.download(ticker, start=start_date, end=end_date, interval="5m")

# Drop rows with NaN values (if any)
df.dropna(inplace=True)



ind_random = vbt.IndicatorFactory(
    class_name = "Random",
    short_name = "rand",
    input_names = ["close"],
    output_names = ["value"]
    ).from_apply_func(
        random_pf
        )



def ema_crossover(close, ema1_period=5, ema2_period=8, ema3_period=13):
    close = close.flatten()

    ema1 = talib.EMA(close, timeperiod=ema1_period)
    ema2 = talib.EMA(close, timeperiod=ema2_period)
    ema3 = talib.EMA(close, timeperiod=ema3_period)

    macd, macd_signal, macd_hist = talib.MACD(close, fastperiod=12, slowperiod=26, signalperiod=9)

    value = [0] * len(close)
    trade_open = 0
    for n in range(len(close)):
        try:
            if ema1[n] < ema3[n] and ema1[n] < ema2[n]:
                value[n] = -100
                trade_open = -1
            elif ema1[n] > ema3[n] and ema1[n] > ema2[n]:
                value[n] = 100
                trade_open = 1

            else:
                value[n] = 0

        except:
            value[n] = 0

    return value