import yfinance as yf
from yahoofinancials import YahooFinancials
import pandas as pd
import datetime as dt
from pathlib import Path 


startDay = dt.datetime(2018,12,31)
stockList = ['AAPL','TSLA','DKNG','BB','GME','WISH','PARA','META']

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
eR = (returns.copy().sum())/returns.size #daily

filepath1 = Path('insight/matrix.csv')  
filepath1.parent.mkdir(parents=True, exist_ok=True)

filepath2 = Path('insight/er.csv')  
filepath2.parent.mkdir(parents=True, exist_ok=True)

covMatrix.to_csv(filepath1)
eR.to_csv(filepath2)

print(covMatrix)
print(eR)

