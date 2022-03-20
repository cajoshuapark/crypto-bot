# crypto-bot
 Automated Cryptocurrency Trading Bot writtin in python using public libraries such as binance, ccxt, pandas, numpy, mplfinance, matplotlib

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
#adding column names
df.columns = ['Open Time', 'Open', 'High', 'Low', 'Close', 'Volume','Close Time', 'Quote Asset Volume',
  'Number of Trades', 'TB Base Volume', 'TB Quote Volume', 'Ignore']
  
#changing elements in following columns to type 'datetime'
df['Open Time'] = pd.to_datetime(df['Open Time']/1000, unit='s')
df['Close Time'] = pd.to_datetime(df['Close Time']/1000, unit='s')

#changing elements in following columns to type 'float'
floatColumns = ['Open', 'High', 'Low','Close', 'Volume','Quote Asset Volume', 'TB Base Volume', 'TB Quote Volume']
df[floatColumns]= df[floatColumns].astype('float64')

#setting index of DataFrame to 'Close Time'
df = df.set_index('Close Time')
```
## Buy and Sell Algorithm
```
for i in range(len(df)):
   if df.mav10.iloc[i] > df.mav15.iloc[i] and df.mav10.iloc[i-1] < df.mav15.iloc[i-1]:
      ndax.id, ndax.create_market_buy_order(ndaxCryptoName, purchaseAmount)
   elif df.mav10.iloc[i] < df.mav15.iloc[i] and df.mav10.iloc[i-1] > df.mav15.iloc[i-1]:
      ndax.id, ndax.create_market_sell_order(ndaxCryptoName, availableCrypto)
```

## Plotting Candlestick Graph with closing time
The lines in the graph represent the moving averages

## Plotting Candlestick Graph with closing time
The lines in the graph represent the moving averages
The up arrows represent buy indicators, the down arrows represent sell indicators

## Automate Crypto Bot
```
import schedule
import time

def fetchData():
   #trading logic

#call fetchData depending on time below
schedule.every(12).hours.do(fetchData)

#continuous data fetching loop
while True:
   schedule.run_pending()
```


