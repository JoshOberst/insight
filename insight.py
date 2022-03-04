import yfinance as yf
from yahoofinancials import YahooFinancials
import pandas as pd
import datetime as dt

startDay = dt.datetime(2022,1,31)
stockList = ['SPY','AAPL','TSLA']

def getReturns(dataStore):
    global startDay
    lastDay = startDay
    returns = dataStore.copy().transpose()
    for tick in dataStore:
        for day in dataStore.get(tick).index:
            if day != startDay: 
                today = dataStore.get(tick).get(day)
                yesterday = dataStore.get(tick).get(lastDay)
                returns[day][tick] = (today - yesterday)/yesterday
            else:
                returns[day][tick] = 0
            lastDay = day
    return(returns)

data = yf.download(stockList,startDay).get("Adj Close")

returns = getReturns(data).transpose()
covMatrix = returns.reset_index(drop=True).cov()



