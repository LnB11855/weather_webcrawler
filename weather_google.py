##### Get yearly CSVs for average precipitation, temperature, and wind speed per US state from 1980-2019.
### Author: Matthew Walter, mswalter@udel.edu


# Import and authorize Earth Engine
# Google Earth Engine API is required to obtain climate data by state and country from raster data
import ee
import folium

# ee.Authenticate()
ee.Initialize()

### Using Google Earth Engine API, download CSVs of Climate data to Drive

# Bring in states feature collection
fc = ee.FeatureCollection('TIGER/2018/States')
geom = fc.geometry()


### Function to get the yearly average precipitation in each state boundary

# CSVs will upload to Google Drive through Google Earth Engine servers


def getPrecip(start, end, name):
    # Precip data

    # Bring in data
    img = ee.ImageCollection('ECMWF/ERA5/MONTHLY')

    # Filter date
    precipsum = img.filterDate(start, end)
    precipsum = precipsum.sum()
    precipsum = precipsum.select('total_precipitation')

    # Convert to double
    img = ee.Image.toDouble(precipsum)

    # Get sum of precipitation in each region
    precipav = precipsum.reduceRegions(**{
        'reducer': ee.Reducer.mean(),
        'collection': fc,
        'scale': 10000
    })

    # Export table to csv in drive
    task_config = {
        'fileFormat': 'csv',
        'folder': 'precip_by_state'
    }

    task = ee.batch.Export.table(precipav, name, task_config)
    task.start()
    task.status()

    return precipsum


# Run Function to get precipitation Sum for each State
i = 1980
while i <= 2019:
    start = '%s-01-01' % (i)
    end = '%s-12-31' % (i)
    name = 'Precip%s_avg_byState' % (i)
    precip = getPrecip(start, end, name)
    i += 1


### Function to get the yearly average temperature in each state boundary


def getTemp(start, end, name):
    # Bring in data
    img = ee.ImageCollection("ECMWF/ERA5/MONTHLY")

    # Filter date
    tempsum = img.filterDate(start, end)
    tempsum = tempsum.mean()
    tempsum = tempsum.select('mean_2m_air_temperature')

    # Get sum of precipitation in each region
    tempav = tempsum.reduceRegions(**{
        'reducer': ee.Reducer.mean(),
        'collection': fc,
        'scale': 10000
    })

    # Export table to csv in drive
    task_config = {
        'fileFormat': 'csv',
        'folder': 'temp_by_state'
    }

    task = ee.batch.Export.table(tempav, name, task_config)
    task.start()
    task.status()

    return tempsum


# Run Function to get precipitation Sum for each State
i = 1980
while i <= 2019:
    start = '%s-01-01' % (i)
    end = '%s-12-31' % (i)
    name = 'Temp%s_avg_byState' % (i)
    temp = getTemp(start, end, name)
    i += 1


### Function to get the yearly average wind speed (m/s) in each country boundary

def getWind(start, end, name):
    # Bring in data
    img = ee.ImageCollection('IDAHO_EPSCOR/TERRACLIMATE')
    # Filter date
    windsum = img.filterDate(start, end)
    windsum = windsum.mean()
    windsum = windsum.select('vs')

    # Get sum of precipitation in each region
    windav = windsum.reduceRegions(**{
        'reducer': ee.Reducer.mean(),
        'collection': fc,
        'scale': 10000
    })

    # Export table to csv in drive
    task_config = {
        'fileFormat': 'csv',
        'folder': 'wind_by_state'
    }

    task = ee.batch.Export.table(windav, name, task_config)
    task.start()
    task.status()

    return windsum


# Run Function to get wind avg for each Country
i = 1980
while i <= 2018:
    start = '%s-01-01' % (i)
    end = '%s-12-31' % (i)
    name = 'Wind%s_avg_byState' % (i)
    wind = getWind(start, end, name)
    i += 1
