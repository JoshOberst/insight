import yfinance as yf
from yahoofinancials import YahooFinancials
import pandas as pd
import datetime as dt
from pathlib import Path
import numpy as np
from pypfopt import expected_returns


startDay = dt.datetime(2018,12,31)
stockList = ['AAPL','TSLA','SPY']
benchList = ['^IXIC'] #This can be changed to suit needs. ONLY 1 STOCK 


data = yf.download(stockList+benchList,startDay).get("Adj Close")
returns = np.log(data.copy()).diff().dropna() #log returns

assets = returns.loc[:, returns.columns != benchList[0]]
benchmark = returns.loc[:, returns.columns == benchList[0]]

eR = expected_returns.capm_return(assets,market_prices = benchmark, returns_data = True, risk_free_rate = 0.07/100,frequency = 252)
print(eR)

covMatrix = assets.cov()*252
print(covMatrix)

filepath1 = Path('insight/matrix.csv')  
filepath1.parent.mkdir(parents=True, exist_ok=True)

filepath2 = Path('insight/er.csv')  
filepath2.parent.mkdir(parents=True, exist_ok=True)

covMatrix.to_csv(filepath1)
eR.to_csv(filepath2)
