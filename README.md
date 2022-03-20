# crypto-bot
 Automated Cryptocurrency Trading Bot writtin in python using public libraries such as binance, ccxt, pandas, numpy, mplfinance, matplotlib

## Logging into NDAX exchange
Using ccxt library to access NDAX exchange.
```
import ccxt

exchange = ccxt.ndax({
   'apiKey': API_KEY,
   'secret': API_SECRET,
   'uid': "123456",   
   'login' : LOGIN,
   'password' : PASSWORD,
   'twofa': "123456",
})
```
## Fetching Historical OHLC (Open High Low Close) Data
Using python-binance library fetch historical OHLC data.
```
from binance.client import Client

client = Client()
historical = client.get_historical_klines('BTCUSDT', client.KLINE_INTERVAL_1DAY, '1-Oct-2021')
```
## Data Cleaning for Candlestick Graph
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
## Plotting Candlestick Graph with closing time
The lines in the graph represent the moving averages.

## Calculating Moving Averages Using DataFrame
To read more about moving averages, visit (https://www.investopedia.com/terms/m/movingaverage.asp)
```
#calculate the moving average for 10 and 15 days
df['mav10'] = df['Close'].rolling(10).mean()
df['mav15'] = df['Close'].rolling(15).mean()
#remove any NaN values from the table
df = df.dropna()
#create a new DataFrame with index 'Close Time' and columns 'Close', 'mav10', 'mav15'
df = df[['Close', 'mav10', 'mav15']]
```

## Buy and Sell Algorithm
Using moving average algorithm to decide buy and sell.
```
#if true, then you can buy, if false, you can sell
tradeBoolean = True
#calculate purchase amount by dividing your current balance with the current crypto price
purchaseAmount = '{0:.3g}'.format(availableCad / askPrice)

if df.mav10.iloc[len(df)-1] > df.mav15.iloc[len(df)-1] and df.mav10.iloc[len(df)-2] < df.mav15.iloc[len(df)-2] and tradeBoolean == True:
    #buy on exchange
    exchange.id, exchange.create_market_buy_order(exchangeCryptoName, purchaseAmount)
if df.mav10.iloc[len(df)-1] < df.mav15.iloc[len(df)-1] and df.mav10.iloc[len(df)-2] > df.mav15.iloc[len(df)-2] and tradeBoolean == False:
    #sell on exchange
    exchange.id, exchange.create_market_sell_order(exchangeCryptoName, availableCrypto)
```

## Plotting Candlestick Graph with closing time
The lines in the graph represent the moving averages.
The up arrows represent buy indicators, the down arrows represent sell indicators.

## Automate Crypto Bot
Using schedule and time libraries to automate cryto bot
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

