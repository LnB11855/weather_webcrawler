from wwo_hist import retrieve_hist_data
frequency = 24
start_date = '07-DEC-2019'
end_date = '06-DEC-2020'
api_key = ''
location_list = ['aruba']
location_list=final.RegionName.unique()
for i in range(len(location_list)):
    try:
        location=[location_list[i]]
        hist_weather_data = retrieve_hist_data(api_key,
                                location,
                                start_date,
                                end_date,
                                frequency,
                                location_label = False,
                                export_csv = True,
                                store_df = True)
    except:
        print(location)
