# -*- coding: utf-8 -*-
"""
Created on Thu Nov 12 12:40:45 2020
PCA on BSE index

@author: Himanshu
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl

import quandl
from sklearn.decomposition import KernelPCA
symbols = ['BSE/BOM500820.4','BSE/BOM532215.4','BSE/BOM532977.4','BSE/BOM500034.4','BSE/BOM532978.4','BSE/BOM532454.4','BSE/BOM532281.4','BSE/BOM500180.4',
           'BSE/BOM500696.4','BSE/BOM500010.4','BSE/BOM532174.4','BSE/BOM532187.4','BSE/BOM500209.4','BSE/BOM500875.4','BSE/BOM500247.4','BSE/BOM500510.4','BSE/BOM500520.4',
           'BSE/BOM532500.4','BSE/BOM500790.4','BSE/BOM532555.4','BSE/BOM500312.4','BSE/BOM532898.4','BSE/BOM500325.4','BSE/BOM500112.4','BSE/BOM524715.4','BSE/BOM532540.4',
           'BSE/BOM500470.4','BSE/BOM532755.4','BSE/BOM500114.4','BSE/BOM532538.4']


mydata = quandl.get("BSE/SENSEX.4", authtoken="SLAD8rb9wAaHtfjw1LdY",start_date="2016-01-02", end_date="2020-11-13")


for sym in symbols:
    mydata[sym] = quandl.get(sym ,authtoken="SLAD8rb9wAaHtfjw1LdY", start_date = "2016-01-02" , end_date = "2020-11-13" )


    
mydata = mydata.dropna()
data = pd.DataFrame(mydata.pop('Close'))
mpl_dates = mpl.dates.date2num(data.index)
scale_function = lambda x: (x-x.mean())/ x.std()
pca = KernelPCA(n_components = 5).fit(mydata.apply(scale_function))
get_we = lambda x:x/x.sum()
pca_components = pca.transform(-mydata)
weights = get_we(pca.lambdas_)
data['PCA_5'] = np.dot(pca_components, weights.T)
data.apply(scale_function).plot(figsize=(8,4))
plt.figure(figsize = (8,4))
plt.scatter(data['PCA_5'], data['Close'], c=mpl_dates)
lin_reg = np.polyval(np.polyfit(data['PCA_5'], data['Close'],1),data['PCA_5'])
plt.plot(data['PCA_5'], lin_reg, 'r', lw=1)
plt.xlabel('PCA_5 INDEX')
plt.ylabel('BSE_SENSEX INDEX')
plt.colorbar(ticks=mpl.dates.DayLocator(interval=100), format=mpl.dates.DateFormatter('%d %b %y'))


    