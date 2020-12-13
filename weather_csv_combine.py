import os
import pandas as pd
import numpy as np
def get_weather(file_path='D:/COVID_19/weather_data',download=True):
    names=[]
    combined=pd.DataFrame([])
    flag=False
    cols=['date', 'maxtempC', 'mintempC', 'totalSnow_cm', 'sunHour', 'uvIndex',
           'moon_illumination', 'moonrise', 'moonset', 'sunrise', 'sunset',
           'DewPointC', 'FeelsLikeC', 'HeatIndexC', 'WindChillC', 'WindGustKmph',
           'cloudcover', 'humidity', 'precipMM', 'pressure', 'tempC', 'visibility',
           'winddirDegree', 'windspeedKmph', 'location']
    sameCols=['date', 'maxtempC', 'mintempC', 'sunHour', 'uvIndex',
           'moon_illumination', 'location']
    diffCols=[
           'DewPointC', 'FeelsLikeC', 'HeatIndexC', 'WindChillC', 'WindGustKmph',
           'cloudcover', 'humidity', 'pressure', 'tempC',
           'winddirDegree', 'windspeedKmph']
    try:
        for info in os.listdir(file_path):
            domain = os.path.abspath(file_path)
            names.append(info.split('.')[0])
            info = os.path.join(domain,info)
            data = pd.read_csv(info)
            data['date_time'] = pd.to_datetime(data.date_time).dt.date
            data = data.rename(columns={'date_time': 'date'})
            data = data[sameCols + diffCols]
            # for diffCols, 1. get the diff values between max and min 2. get the average
            data_agg = data.groupby('date')[diffCols].agg([np.ptp, np.mean])
            data = data.join(data_agg, on='date')
            data = data.drop(diffCols, axis=1)
            data = data.drop_duplicates()
            combined=pd.concat([combined,data],axis=0)
    except:
        print('weather file load error')
    final_weather_csv=combined.reset_index(drop=True)
    if download:
        final_weather_csv.to_csv('combined_weather.csv',index=False)
    return final_weather_csv



