import numpy as np
import pandas as pd
import talib
import matplotlib.pyplot as plt

# Generate sample price data (or load your price data)
np.random.seed(42)
price_data = pd.Series(np.random.randn(100).cumsum() + 100)

# Calculate MACD
macd, macd_signal, _ = talib.MACD(price_data, fastperiod=12, slowperiod=26, signalperiod=9)

# Calculate ATR
atr = talib.ATR(price_data, price_data, price_data, timeperiod=14)

# Define thresholds for signals
atr_threshold = atr.mean() + atr.std()  # Use mean + 1 std dev as a threshold

# Generate selling signals
selling_signal = (macd < macd_signal) & (atr > atr_threshold)

# Create a DataFrame to hold signals
signals_df = pd.DataFrame({
    'Price': price_data,
    'MACD': macd,
    'MACD_Signal': macd_signal,
    'ATR': atr,
    'Selling_Signal': selling_signal
})

# Plot results
plt.figure(figsize=(14, 8))
plt.plot(price_data, label='Price', color='blue')
plt.plot(macd, label='MACD', color='red')
plt.plot(macd_signal, label='MACD Signal', color='orange')
plt.plot(atr, label='ATR', color='green')
plt.scatter(signals_df.index[selling_signal], signals_df['Price'][selling_signal],
            marker='x', color='red', s=100, label='Selling Signal')
plt.title('Selling Signal based on MACD and ATR')
plt.legend()
plt.show()

# Display signals
print(signals_df[selling_signal])
