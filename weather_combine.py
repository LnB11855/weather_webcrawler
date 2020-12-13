import requests
import datetime
import numpy as np
import pandas as pd
import os
import sys
import seaborn as sns
from matplotlib import pyplot as plt
weather1=pd.read_csv('state_weather.csv')
weather2=pd.read_csv('state_weather2.csv')
weather1=weather1.loc[0:9489,['0','1','2','3','4']]
weather2=weather2[['0','1','2','3','4']]
weather=pd.concat([weather1,weather2])
weather['1']=weather1['1'].astype('datetime64[ns]')
weather.columns=['State','Date','TAVG','TMAX','TMIN']
weather[['State','Date','TAVG']].groupby('State')['TAVG'].plot(legend=True)

sns.lineplot(x='Date',y='TAVG',hue='State',data=weather)
plt.show()
sns.lineplot(x='Date',y='TMAX',hue='State',data=weather)
plt.show()
sns.lineplot(x='Date',y='TMIN',hue='State',data=weather)
plt.show()

weather.to_csv("weather_one_year.csv")