
# coding: utf-8

# # Assignment 2
# 
# Before working on this assignment please read these instructions fully. In the submission area, you will notice that you can click the link to **Preview the Grading** for each step of the assignment. This is the criteria that will be used for peer grading. Please familiarize yourself with the criteria before beginning the assignment.
# 
# An NOAA dataset has been stored in the file `data/C2A2_data/BinnedCsvs_d400/fb441e62df2d58994928907a91895ec62c2c42e6cd075c2700843b89.csv`. This is the dataset to use for this assignment. Note: The data for this assignment comes from a subset of The National Centers for Environmental Information (NCEI) [Daily Global Historical Climatology Network](https://www1.ncdc.noaa.gov/pub/data/ghcn/daily/readme.txt) (GHCN-Daily). The GHCN-Daily is comprised of daily climate records from thousands of land surface stations across the globe.
# 
# Each row in the assignment datafile corresponds to a single observation.
# 
# The following variables are provided to you:
# 
# * **id** : station identification code
# * **date** : date in YYYY-MM-DD format (e.g. 2012-01-24 = January 24, 2012)
# * **element** : indicator of element type
#     * TMAX : Maximum temperature (tenths of degrees C)
#     * TMIN : Minimum temperature (tenths of degrees C)
# * **value** : data value for element (tenths of degrees C)
# 
# For this assignment, you must:
# 
# 1. Read the documentation and familiarize yourself with the dataset, then write some python code which returns a line graph of the record high and record low temperatures by day of the year over the period 2005-2014. The area between the record high and record low temperatures for each day should be shaded.
# 2. Overlay a scatter of the 2015 data for any points (highs and lows) for which the ten year record (2005-2014) record high or record low was broken in 2015.
# 3. Watch out for leap days (i.e. February 29th), it is reasonable to remove these points from the dataset for the purpose of this visualization.
# 4. Make the visual nice! Leverage principles from the first module in this course when developing your solution. Consider issues such as legends, labels, and chart junk.
# 
# The data you have been given is near **Ann Arbor, Michigan, United States**, and the stations the data comes from are shown on the map below.

# In[22]:

import matplotlib.pyplot as plt
#import mplleaflet
import pandas as pd
import numpy as np

#cleaning data
df1 = pd.read_csv('data/C2A2_data/BinnedCsvs_d400/fb441e62df2d58994928907a91895ec62c2c42e6cd075c2700843b89.csv')
df1['Date'] = pd.DatetimeIndex(df1['Date'])
df1 = df1[~((df1.Date.dt.month == 2) & (df1.Date.dt.day == 29))]
df1['Data_Value'] = df1['Data_Value']/10
df1['month'] = df1['Date'].dt.month
df1['Day'] = df1['Date'].dt.day
df1 = df1.sort_values(['month', 'Day'], ascending=[True, True])
df4 = df1.loc[ df1['Date'].dt.year > 2014 ]
df1 = df1.loc[ df1['Date'].dt.year < 2015 ]

#creating record temperatures dataframe
df5 = df4[df4['Element'] == 'TMAX']
df5 = df4.groupby(['month','Day'], as_index=False)['Data_Value'].max()
df5['day-month'] = df5['Day'].map(str)+'-'+df5['month'].map(str)
df6 = df4[df4['Element'] == 'TMIN']
df6 = df4.groupby(['month','Day'], as_index=False)['Data_Value'].min()
df6['day-month'] = df6['Day'].map(str)+'-'+df6['month'].map(str)
df2 = df1.groupby(['month','Day'], as_index=False)['Data_Value'].max()
df2['day-month'] = df2['Day'].map(str)+'-'+df2['month'].map(str)
df3 = df1.groupby(['month','Day'], as_index=False)['Data_Value'].min()
df5['Diff'] = df5['Data_Value']-df2['Data_Value']
df5 = df5[df5['Diff'] > 0]
df6['Diff'] = df6['Data_Value']-df3['Data_Value']
df6 = df6[df6['Diff'] < 0]
frame = [df5,df6]
df7 = pd.concat(frame)
df7 = df7.sort_values(['month', 'Day'], ascending=[True, True])
df7 = df7.rename(columns = {'Data_Value':'2015Data_Value'})
df8 = df2.merge(df7, how = 'outer', left_on ='day-month', right_on ='day-month')

#creating plot lists
Record_High_temperatures = df2['Data_Value']
Record_Low_temperatures = df3['Data_Value']
Record_temperatures = df8['2015Data_Value']

#plotting code
fig, axs = plt.subplots(figsize = (16,8))

plt.plot(Record_High_temperatures,'-b',Record_Low_temperatures,'-r')
plt.plot(Record_temperatures,'og')
axs.set_xlim(0,len(Record_High_temperatures))

plt.gca().fill_between(range(len(Record_High_temperatures)), 
                       Record_High_temperatures, Record_Low_temperatures, 
                       facecolor='Grey', 
                       alpha=0.25)
plt.legend(['Record High Temperatures(Period 2005-14)', 'Record Low Temperatures(Period 2005-14)', '2015 Record Temperatures'])
axs.set_xlabel('Dates(total 365 days for a year)')
axs.set_ylabel('Temperature(in degree centigrade)')
axs.set_title('Temperature record for a region')

plt.show()


# ### 
