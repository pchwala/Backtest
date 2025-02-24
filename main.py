import yfinance as yf
import pandas as pd
import talib
from datetime import datetime, timedelta

import matplotlib.pyplot as plt

# Ensure the arrays are 1D
highs = df['High'].astype(float).values.flatten()
lows = df['Low'].astype(float).values.flatten()
closes = df['Close'].astype(float).values.flatten()

# Calculate Stochastic Oscillator
df['%K'], df['%D'] = talib.STOCH(highs, lows, closes,
                                 fastk_period=14, slowk_period=3, slowk_matype=0,
                                 slowd_period=3, slowd_matype=0)

# Plot price data
fig, axes = plt.subplots(2, 1, figsize=(12, 8), sharex=True)

# Plot EUR/USD price
axes[0].plot(df.index, df['Close'], label="EUR/USD Close Price", color='blue')
axes[0].set_title("EUR/USD Price (5-Minute Candles)")
axes[0].legend()
axes[0].grid()

# Plot Stochastic Oscillator
axes[1].plot(df.index, df['%K'], label="%K Line", color='green')
axes[1].plot(df.index, df['%D'], label="%D Line", color='red', linestyle="dashed")
axes[1].axhline(80, color='gray', linestyle="dotted")  # Overbought level
axes[1].axhline(20, color='gray', linestyle="dotted")  # Oversold level
axes[1].set_title("Stochastic Oscillator")
axes[1].legend()
axes[1].grid()

plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

#test gpg2