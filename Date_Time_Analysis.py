#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 23 17:17:52 2019

@author: adam
"""

import pandas as pd
import matplotlib.pyplot as plt

q3 = pd.read_csv('/media/adam/Data/DataSets/Divvy_Trips_2018_Q3.csv')

q3['start_time'] = pd.to_datetime(q3['start_time'])
# convert to datetime format
q3 = q3.assign(month = q3.start_time.dt.strftime('%m'))
# create new month column
q3 = q3.assign(hour = q3.start_time.dt.strftime('%H'))
# create new hour column
q3 = q3.assign(dow = q3.start_time.dt.strftime('%a'))
 # create new DOW column
 
 dowCount = q3['dow'].value_counts()
 monthCount = q3['month'].value_counts()
 
 hourCount =  q3['hour'].value_counts()
 hourCount.sort_index(inplace=True)
 plt.plot(hourCount)
 plt.xlabel('Hour')
 plt.ylabel('N rides')
 plt.title('Rides starting at hour of the day')
 
 stationCount = q3['from_station_id'].value_counts()
 stationCount.sort_values(inplace=True,ascending=False)
 #what are the post popular stations?
 
topStations = stationCount.head(19)
top20=stationCount.index[0:20]
top20df = pd.DataFrame(top20) 
top20df = to20df.rename(columns={0:'id'})
top20df = pd.merge(to20df,stations[['id','latitude','longitude']],on='id')

from pandas import DataFrame
import pandas as pd
import json
import requests

# get up-to-date information about Divvy Bike stations
url = 'http://divvybikes.com/stations/json'
resp = requests.get(url)

data = json.loads(resp.text)
stations_metadata = data['stationBeanList']
stations_dataFrame = DataFrame(stations_metadata)

