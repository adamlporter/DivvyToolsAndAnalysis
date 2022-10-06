# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import pandas as pd

df = pd.read_csv('/media/adam/Data/DataSets/Divvy_Trips_2018_Q3.csv')



totalTrips = len(df)

df.groupby('gender')[int(['tripduration'[:-2])]].mean()
df.groupby('gender')['birthyear'].mean()

df['tripduration'] = df['tripduration'].astype('float64') # won't work with strings with commas
df.apply(pd.to_numeric, errors='ignore')

df.groupby('from_station_id')['trip_id'].count() # count number of trips from a given station

 def conv_to_int(valString):
    try:
        return(int(valString[:-2].replace(',','')))
    except:
        return(0)

temp_tripdur = df['tripduration'] # pull out a single column
temp_trip_list = [] # create a blank list
for i in temp_tripdur: #iterate the column
    temp_trip_list.append(conv_to_int(i)) #add values to new list   
df['tripduration'] = temp_trip_list #replace initial values with new values

    
df = pd.read_csv('/media/adam/Data/DataSets/Divvy_Test_trips.csv',parse_dates=[1,2],thousands = ',')
df.groupby('gender')['trip_id'].count()
df.groupby('gender')['tripduration'].mean()/60

stations = pd.read_csv('/media/adam/Data/DataSets/Divvy_Stations_2013.csv',parse_dates=[6])

data = df.merge(stations,left_on = 'from_station_id',right_on='id')

import matplotlib.pyplot as plt
plt.scatter(1,1)



stations = pd.read_csv('/media/adam/Data/DataSets/Divvy_Stations_2013.csv',parse_dates=[6])
plt.scatter(stations['latitude'],stations['longitude'])

# =====
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import pandas as pd

stations = pd.read_csv('/media/adam/Data/DataSets/Divvy_Stations_2013.csv',parse_dates=[6])


fig = plt.figure(figsize=(4, 8))
m = Basemap(projection='lcc', resolution='h', 
            lat_0=41.87, lon_0=-87.64,
            width=1.25E4, height=2.5E4)
m.drawcoastlines()
x,y = m(-87.64,41.87)
plt.plot(x,y,'ok',markersize = 2)
plt.text(x,y,'Union Station',fontsize=8)
lat = stations['latitude'].values
lon = stations['longitude'].values
m.scatter(lon,lat,latlon=True,s=2)

# ====================================
# second in a day
# input a hour/min/sec and this will return second from midnight

def sec_offset(h,m,s):
    return(h*3600  + m * 60 + s)
    
    