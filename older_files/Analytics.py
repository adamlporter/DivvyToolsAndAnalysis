#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 22 20:14:21 2019

@author: adam
"""

import pandas as pd
import geopy
from geopy import distance

stations = pd.read_csv('/media/adam/Data/DataSets/Divvy_Stations_2017_Q3Q4.csv')
q3 = pd.read_csv('/media/adam/Data/DataSets/Divvy_Trips_2018_Q3.csv')

# this will add lat, long to the bike use data  
q3 = pd.merge(q3,stations[['id','latitude','longitude']],'left',left_on = 'from_station_id',right_on = 'id')
q3 = pd.merge(q3,stations[['id','latitude','longitude']],'left',left_on = 'to_station_id',right_on = 'id')
q3 = q3.drop(columns = ['id_x','id_y'])
q3 = q3.rename(columns={'latitude_x':'from_lat','longitude_x':'from_long',
                        'latitude_y':'to_lat','longitude_y':'to_long'})
q3['distance']=q3.apply(lambda row: (distance.distance((row.from_lat, row.from_long),
                                    (row.to_lat, row.to_long)).miles), axis='columns')

   


tt['distance']=tt.apply(lambda row: (distance.distance((row.from_lat, row.from_long), (row.to_lat, row.to_long)).miles), axis='columns')
# calculate distance between two points in the df



tt['start_time'] = pd.to_datetime(tt['start_time'])
# convert to datetime format
tt = tt.assign(month = tt.start_time.dt.strftime('%m'))
# create new month column
tt = tt.assign(hour = tt.start_time.dt.strftime('%H'))
# create new hour column
tt = tt.assign(dow = tt.start_time.dt.strftime('%w'))
 # create new DOW column with 0 - 6 values
 
 
# this will add lat, long to the bike use data  
q3 = pd.merge(q3,stations[['id','latitude','longitude']],'left',left_on = 'from_station_id',right_on = 'id')
q3 = pd.merge(q3,stations[['id','latitude','longitude']],'left',left_on = 'to_station_id',right_on = 'id')
q3 = q3.drop(columns = ['id_x','id_y'])
q3 = q3.rename(columns={'latitude_x':'from_lat','longitude_x':'from_long',
                        'latitude_y':'to_lat','longitude_y':'to_long'})
q3['distance']=q3.apply(lambda row: (distance.distance((row.from_lat, row.from_long),
                                    (row.to_lat, row.to_long)).miles), axis='columns')

   


tt['distance']=tt.apply(lambda row: (distance.distance((row.from_lat, row.from_long), (row.to_lat, row.to_long)).miles), axis='columns')
# calculate distance between two points in the df




