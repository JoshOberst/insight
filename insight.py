import yfinance as yf
from yahoofinancials import YahooFinancials
import pandas as pd
import datetime as dt
from pathlib import Path
import numpy as np


startDay = dt.datetime(2018,12,31)
stockList = []


data = yf.download(stockList,startDay).get("Adj Close")
returns = np.log(data.copy()).diff().dropna() #log returns



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
