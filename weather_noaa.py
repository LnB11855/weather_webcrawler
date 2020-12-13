import requests
import datetime
import numpy as np
import pandas as pd
import os
import sys


def get_temp(locationid, begin_date, end_date,mytoken):
    token = {'token': mytoken}

    # passing as string instead of dict because NOAA API does not like percent encoding
    params = 'datasetid=GHCND' + '&locationid=' + str(locationid) + '&startdate=' + str(begin_date) + '&enddate=' + str(
        end_date) +'&limit=1000' + '&units=standard'+'&datacategoryid=TEMP'

    base_url = 'https://www.ncdc.noaa.gov/cdo-web/api/v2/data'

    r = requests.get(base_url, params=params, headers=token)
    print("Request status code: " + str(r.status_code))

    try:
        # results comes in json form. Convert to dataframe
        df = pd.DataFrame.from_dict(r.json()['results'])
        print("Successfully retrieved " + str(len(df['station'].unique())) + " stations")
        dates = pd.to_datetime(df['date'])
        print("Last date retrieved: " + str(dates.iloc[-1]))

        # if df.count().max() == 1000:
        #     print('WARNING: Maximum data limit was reached (limit = 1000)')
        #     print('Consider breaking your request into smaller pieces')

        # return df[df.datatype=='TAVG'].value.values.mean()
        return df[df.datatype=='TAVG'].value.values.mean(),df[df.datatype=='TMAX'].value.values.mean(),df[df.datatype=='TMIN'].value.values.mean()

    # Catch all exceptions for a bad request or missing data
    except:
        print("Error converting weather data to dataframe. Missing data?")
        return np.nan,np.nan,np.nan


def get_region_info(mytoken):
    token = {'token': mytoken}

    # passing as string instead of dict because NOAA API does not like percent encoding

    region = 'locationcategoryid=ST' + '&units=standard' + '&limit=1000'
    base_url = 'https://www.ncdc.noaa.gov/cdo-web/api/v2/locations'
    r = requests.get(base_url, headers=token, params=region)
    print("Request status code: " + str(r.status_code))

    try:
        # results comes in json form. Convert to dataframe
        df = pd.DataFrame.from_dict(r.json()['results'])
        print("Successfully retrieved " + str(len(df['id'].unique())) + " stations")

        if df.count().max() >= 1000:
            print('WARNING: Maximum data limit was reached (limit = 1000)')
            print('Consider breaking your request into smaller pieces')

        return df[['name','id']]
    # Catch all exceptions for a bad request or missing data
    except:
        print("Error converting station data to dataframe. Missing data?")

def add_temp(region_name,df_locations,date,window):
    if region_name in df_locations.name.values:
        begin_date = (date-datetime.timedelta(days=window)).strftime("%Y-%m-%d")
        end_date =date.strftime("%Y-%m-%d")
        locationid=df_locations[df_locations.name==region_name].id.values[0]
        temp = get_temp(locationid, begin_date, end_date, mytoken)
        return temp
    else:
        print("Region not in record")
        return np.nan


if __name__ == '__main__':

    # If running script directly from command line, just retrieve this day last year's weather
    # This can be modified to replace 'lastyear' with any date with the format 'YYYY-mm-dd'

    # Put your API token from NOAA here
    mytoken = 'kgumxzGkOrloppitYAKgwXQUGyKWOvvx'

    if mytoken == '':
        sys.exit('Missing API token. Open get_weather_noaa and provide your unique token!')
    token = {'token': mytoken}

    # passing as string instead of dict because NOAA API does not like percent encoding

    region = 'locationcategoryid=COUNTRY' + '&units=standard' + '&limit=1000'
    base_url = 'https://www.ncdc.noaa.gov/cdo-web/api/v2/locations'
    r = requests.get(base_url, headers=token, params=region)
    print("Request status code: " + str(r.status_code))


    print("Request status code: " + str(r.status_code))
    com_url="https: // www.ncdc.noaa.gov / cdo - web / api / v2 / locationcategories?startdate = 1970 - 01 - 01"
    # Location key for the region you are interested in (can be found on NOAA or requested as a different API as well)
    # locationid = 'FIPS:38'  # location id for North Dakota
    lastyear = datetime.datetime.now() - datetime.timedelta(days=365)

    df_locations = get_region_info(mytoken)

    temp_state_list=[]
    for i in range(26,51):
        region_name=df_locations.loc[i,'name']
        locationid=df_locations.loc[i,'id']
        for j in range(365):
            begin_date=(lastyear+datetime.timedelta(days=j)).strftime("%Y-%m-%d")
            end_date=begin_date
            temp_aver, temp_max, temp_min = get_temp(locationid, begin_date, end_date, mytoken)
            temp_state_list.append([region_name,begin_date, temp_aver, temp_max, temp_min])

    temp_df=pd.DataFrame(temp_state_list)
    temp_df.to_csv("state_weather2.csv")




    # begin_date = lastyear.strftime("%Y-%m-%d")
    # end_date = lastyear.strftime("%Y-%m-%d")
    # temp_aver,temp_max,temp_min = get_temp(locationid, begin_date, end_date, mytoken)
    #
    # date=datetime.datetime.now()
    # window=2
    #
    # final['temp'] = final.RegionName.apply(lambda RegionName: add_temp(RegionName,df_locations,date,window))
    #

