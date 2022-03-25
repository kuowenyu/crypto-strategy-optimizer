import ccxt
import pandas as pd
import datetime

exchange = ccxt.binanceus()
symbol = 'ETH/USD'
timeframe = '1d'
filename = 'ETH_1d_20210510_20211031.csv'
start_date = int(datetime.datetime(2021, 5, 10).timestamp() * 1000)
end_date = int(datetime.datetime(2021, 10, 31).timestamp() * 1000)

bars = []
last_date = start_date
while True:
    if last_date >= end_date:
        break
    batch = exchange.fetch_ohlcv(symbol, timeframe=timeframe, since=last_date, limit=30)
    bars = bars + batch
    last_date = batch[-1][0]

df = pd.DataFrame(bars[:-1], columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
df.to_csv(filename)

