### 0. Imports and params

import numpy as np
import pandas as pd
import quandl
import yfinance as yf
import os
import matplotlib.pyplot as plt

hist_years = 20
bronze = './data/bronze/stock-prices/'
silver = './data/silver/stock-prices/'
gold = './data/gold/portfolio-optimization/'
ticker = ['AAPL','MSFT','AMZN','TSLA','GOOGL','GOOG','NVDA','BRK-B','META','UNH','^GSPC']
start = (pd.to_datetime('today').normalize()+pd.DateOffset(years=-hist_years)).strftime('%Y-%m-%d')
end = pd.to_datetime('today').normalize().strftime('%Y-%m-%d')
print('Historical data loaded: {} - {}'.format(start, end))

if not os.path.exists(bronze+end+'/'):
    os.makedirs(bronze+end+'/')
if not os.path.exists(silver):
    os.makedirs(silver)
if not os.path.exists(gold):
    os.makedirs(gold)

### 1. Bronze Layer

# Data extraction
for i in ticker:
    brz_data = yf.download(i, start=start, end=end)
    brz_data['Ticker']=i
    brz_data.to_csv(bronze+end+'/'+i+'.csv')

### 2. Silver Layer

slv_data = pd.DataFrame()
for i in ticker:
    df = pd.read_csv(bronze+end+'/'+i+'.csv')
    slv_data = pd.concat([slv_data, df])
slv_data.to_csv(silver+'stock_prices.csv',index=False)