import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import seaborn as sns
from pandas_datareader import data as web
import warnings
warnings.filterwarnings("ignore")

prices = pd.DataFrame()
tickers = ['ITUB3.SA', 'BBDC3.SA', 'BBAS3.SA', 'SANB3.SA', '^BVSP']
for i in tickers:
    prices[i] = web.get_data_yahoo(i,'01/01/2021')['Adj Close']
    
prices.head()

prices.rename(columns ={'ITUB3.SA':'ITUB', 'BBDC3.SA':'BBDC','BBAS3.SA':'BBAS','SANB3.SA':'SANB', '^BVSP':'IBOV'},inplace = True)
prices['IBOV'] = prices['IBOV']/1000
prices.reset_index(inplace = True)


prices.dropna(subset = ['IBOV'], inplace = True)
prices.IBOV.isnull().sum()

tickers = list(prices.drop(['Date'], axis = 1).columns)
plt.figure(figsize=(16,6))

for i in tickers:
        plt.plot(prices['Date'], prices[i])
plt.legend(tickers)
plt.grid()
plt.title("Cotação x tempo", fontsize = 25)
plt.show()

plt.figure(figsize=(16,6))
plt.plot(prices['Date'],prices['ITUB'].rolling(window = 90).mean())
plt.plot(prices['Date'], prices['ITUB'], alpha = 0.8)
plt.plot(prices['Date'],prices['ITUB'].rolling(window = 365).mean())
plt.grid()
plt.title('Cotações diárias e médias móveis de ITUB3', fontsize = 15)
plt.legend(['Média móvel trimestral','Cotação diária','Média móvel anual'])
plt.show()

sns.heatmap(prices.corr(), annot = True)
plt.show()

returns = pd.DataFrame()
for i in tickers:
    returns[i] = prices[i].pct_change()
returns['Date'] = prices['Date']

sns.pairplot(returns)
plt.show()

returns.describe()

sns.distplot(returns['IBOV'].dropna())


return_sum = pd.DataFrame()
for ticker in tickers:
    return_sum[ticker] = (returns[ticker]+1).cumprod()
return_sum['Date'] = returns['Date']

plt.figure(figsize=(16,6))
plt.plot(return_sum['Date'], return_sum.drop(['Date'], axis = 1), alpha = 0.9)
plt.legend(tickers)
plt.title("Retorno x tempo", fontsize = 15)
plt.grid()
plt.show()

