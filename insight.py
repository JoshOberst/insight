import yfinance as yf
from yahoofinancials import YahooFinancials
import pandas as pd
import datetime as dt
from pathlib import Path
import numpy as np
from pypfopt import expected_returns

#Imputs
startDay = dt.datetime(2018,12,31)
stockList = ['AAPL','TSLA','SPY','GME','BB']
benchList = ['^IXIC'] #This can be changed to suit needs. ONLY 1 STOCK 
oneYearTBill = 0.01026 

#Getting Data
data = yf.download(stockList+benchList,startDay).get("Adj Close")

#Getting Log Returns
returns = np.log(data.copy()).diff().dropna()

#Spliting out the benchmark
assets = returns.loc[:, returns.columns != benchList[0]]
benchmark = returns.loc[:, returns.columns == benchList[0]]

#Calculating Expected returns and the Cov Matrix
eR = expected_returns.capm_return(assets,market_prices = benchmark, returns_data = True, risk_free_rate = oneYearTBill/100,frequency = 252)
covMatrix = assets.cov()*252

#Printing to csv
filepath1 = Path('insight/matrix.csv')  
filepath1.parent.mkdir(parents=True, exist_ok=True)
filepath2 = Path('insight/er.csv')  
filepath2.parent.mkdir(parents=True, exist_ok=True)
covMatrix.to_csv(filepath1)
eR.to_csv(filepath2)
print(eR)
print(covMatrix)
