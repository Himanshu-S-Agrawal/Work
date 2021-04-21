# -*- coding: utf-8 -*-
"""
Created on Thu Oct 22 19:47:26 2020
efficient frontier
@author: Himanshu
"""
import pandas as pd
from pandas_datareader import data as wb
import matplotlib.pyplot as plt
import scipy.optimize as sco
import numpy as np

symbols = ['AAPL','MSFT','DB','GLD']
noa = len(symbols)

data = pd.DataFrame()
for sym in symbols:
    data[sym] = wb.DataReader(sym, data_source = 'yahoo', start ='2012-1-1')['Adj Close']
    
rets = np.log(data / data.shift(1))
#weights = np.random.random(noa)
prets = []
pvols = []
for p in range(2500):
    weights = np.random.random(noa)
    weights /= np.sum(weights)
    prets.append(np.sum(rets.mean()*weights)*252)
    pvols.append(np.sqrt(np.dot(weights.T,np.dot(rets.cov()*252,weights))))
  
prets = np.array(prets)
pvols = np.array(pvols)

#plt.figure(figsize=(8,4))
#plt.scatter(pvols,prets, c=prets/pvols, marker='o')
#plt.colorbar(label='sharpe ratio')

def statis(weights):
    weights = np.array(weights)
    pret = []
    pvol = []
    pret = np.sum(rets.mean()*weights)*252
    pvol = np.sqrt(np.dot(weights.T,np.dot(rets.cov()*252,weights)))
    return np.array([pret, pvol, pret/pvol])
    
def min_func_port(weights):
    return statis(weights)[1]

trets = np.linspace(0.0,0.25,50)
tvols = []
bnds = tuple((0,1) for x in weights)
for tret in trets:
    cons = ({'type':'eq','fun': lambda x: statis(x)[0]-tret},
             {'type':'eq', 'fun': lambda x: np.sum(x)-1})
    res = sco.minimize(min_func_port, noa*[1./noa,], method = 'SLSQP', bounds = bnds, constraints = cons)
    tvols.append(res['fun'])
    
tvols = np.array(tvols)
    
plt.figure(figsize=(8,5))
plt.scatter(pvols,prets, c=prets/pvols, marker='o')
plt.scatter(tvols, trets, c=trets/tvols, marker='x')
plt.colorbar(label='sharpe ratio')

    
    
