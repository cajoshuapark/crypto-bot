# crypto-bot
Created a crypto bot in python using public libraries such as binance, ccxt, pandas, numpy, mplfinance, matplotlib

## Logging into NDAX exchange
```
import ccxt

ndax = ccxt.ndax({
    'apiKey': API_KEY,
    'secret': API_SECRET,
    'uid': "123456",   
    'login' : LOGIN,
    'password' : PASSWORD,
    'twofa': "123456",
})
```
## Fetching Historical OHLC (Open High Low Close) Data
```
from binance.client import Client

client = Client()
historical = client.get_historical_klines('BTCUSDT', client.KLINE_INTERVAL_1DAY, '1-Oct-2021')
```
## Data Cleaning
```
df.columns = ['Open Time', 'Open', 'High', 'Low', 'Close', 'Volume','Close Time', 'Quote Asset Volume',
  'Number of Trades', 'TB Base Volume', 'TB Quote Volume', 'Ignore']
dateTimeColumns = ['Open Time','Close Time']
df[dateTimeColumns] = pd.to_datetime(df[dateTimeColumns]/1000, unit='s')
floatColumns = ['Open', 'High', 'Low','Close', 'Volume','Quote Asset Volume', 'TB Base Volume', 'TB Quote Volume']
df[floatColumns]= df[floatColumns].astype('float64')
df = df.set_index('Close Time')
```
## Plotting Candlestick Graph with closing time
The lines in the graph represent the moving averages
