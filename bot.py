
from config import API_KEY, API_SECRET , LOGIN, PASSWORD
from binance.client import Client
from operator import truediv
import matplotlib.pyplot as plt 
import mplfinance as mpf
import pandas as pd
import schedule
import ccxt
import json
 
tradeBoolean = True

def fetchData():
    #if true, then you can buy, if false, you can sell
    exchangeCryptoName = 'MANA/CAD'
    cryptoName = 'MANA'
    binanceCryptoName = 'BTCUSDT'

    #accessing ndax account through ccxt library 
    exchange = ccxt.ndax({
        'apiKey': API_KEY,
        'secret': API_SECRET,
        'uid': "237456",   
        'login' : LOGIN,
        'password' : PASSWORD,
        'twofa': "440367",
    })

    #fetching balance
    balance = exchange.fetch_balance()
    ticker = exchange.fetch_ticker(exchangeCryptoName)
    #formatting json response
    json.dumps(balance, sort_keys=True, indent=4)
    json.dumps(ticker, sort_keys=True, indent=4)

    askPrice = ticker['ask']
    availableCad = balance['CAD'].get('free')
    availableCrypto = balance[cryptoName].get('free')
    #calculating max purchase amount by dividing my available CAD with the current crypto price
    purchaseAmount = '{0:.3g}'.format(availableCad / askPrice)

    #accessing binance client using binance library 
    client = Client()
    #fetching historical OHLCV values using binance client
    historical = client.get_historical_klines(
        binanceCryptoName, client.KLINE_INTERVAL_1DAY, '1-Jan-2019'
    )

    df = pd.DataFrame(historical)
    
    # data cleaning
    df.columns = ['Open Time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close Time', 'Quote Asset Volume', 'Number of Trades', 'TB Base Volume', 'TB Quote Volume', 'Ignore']
    dateTimeColumns = ['Open Time','Close Time']
    df['Open Time'] = pd.to_datetime(df['Open Time']/1000, unit='s')
    df['Close Time'] = pd.to_datetime(df['Close Time']/1000, unit='s')
    floatColumns = ['Open', 'High', 'Low','Close', 'Volume','Quote Asset Volume', 'TB Base Volume', 'TB Quote Volume']
    df[floatColumns]= df[floatColumns].astype('float64')
    df = df.set_index('Close Time')
    
   #plot candlestick graph with moving averages
    mpf.plot(df.tail(100),
            type='candle',style='yahoo',volume= True,
            title= binanceCryptoName + ' --- LAST 100 days',
            mav=(10,15))

    #data cleaning
    df['mav10'] = df['Close'].rolling(10).mean()
    df['mav15'] = df['Close'].rolling(15).mean()
    df = df.dropna()
    df = df[['Close','mav10', 'mav15']]

    buy = []
    sell = []

    # algorithm for buy and sell
    for i in range(len(df)):
        if df.mav10.iloc[i] > df.mav15.iloc[i] \
        and df.mav10.iloc[i-1] < df.mav15.iloc[i-1]:
            buy.append(i)
        elif df.mav10.iloc[i] < df.mav15.iloc[i] \
        and df.mav10.iloc[i-1] > df.mav15.iloc[i-1]:
            sell.append(i)

    #plotting buy and sell indicators
    plt.figure(figsize=(12,5))
    plt.plot(df['Close'], label='Price', c='blue', alpha=0.5)
    plt.plot(df['mav10'], label='mav10', c='k', alpha = 0.9)
    plt.plot(df['mav15'], label='mav15', c='magenta', alpha = 0.9)
    plt.scatter(df.iloc[buy].index,df.iloc[buy]['Close'], marker='^',color='g', s=100)
    plt.scatter(df.iloc[sell].index,df.iloc[sell]['Close'], marker='v',color='r', s=100)
    plt.legend()
    print(plt.show())

    #checking trades for today
    if df.mav10.iloc[len(df)-1] > df.mav15.iloc[len(df)-1] \
    and df.mav10.iloc[len(df)-2] < df.mav15.iloc[len(df)-2] \
    and tradeBoolean == True:
        print('buy today')  
        print(exchange.id, exchange.create_market_buy_order(exchangeCryptoName, purchaseAmount))  
    if df.mav10.iloc[len(df)-1] < df.mav15.iloc[len(df)-1] \
    and df.mav10.iloc[len(df)-2] > df.mav15.iloc[len(df)-2] \
    and tradeBoolean == False:
        print('sell today')  
        print(exchange.id, exchange.create_market_sell_order(exchangeCryptoName, availableCrypto))

#call fetchData depending on time below
schedule.every(12).hours.do(fetchData)

#continuous data fetching loop
while True:
    schedule.run_pending()
