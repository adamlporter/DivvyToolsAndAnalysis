#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov  7 09:09:36 2020

@author: adam

data from Divvy: https://www.divvybikes.com/system-data
    https://divvy-tripdata.s3.amazonaws.com/index.html
"""


import glob
import pandas as pd
#import numpy as np
#import seaborn as sns
from datetime import datetime

def get_station_data():
    import urllib.request
    import json
    
    stat_info = 'https://gbfs.divvybikes.com/gbfs/en/station_information.json'
    stat_status = 'https://gbfs.divvybikes.com/gbfs/en/station_status.json'
    
    url = urllib.request.urlopen(stat_info)
    data = json.loads(url.read().decode())  
    station_info_df = pd.DataFrame(data['data']['stations']).set_index('station_id')

    #clean data by a) turning index into column and making it an int (station id))
    station_info_df.reset_index(level=0,inplace=True)   
    station_info_df['station_id'] = station_info_df['station_id'].astype(int)
    
    return station_info_df

def add_lat_long(ride_data,station_data):
    from geopy import distance

    ride_data = pd.merge(ride_data,station_data[['station_id','lat','lon']],'left',left_on = 'from_station_id',right_on = 'station_id')
    ride_data = pd.merge(ride_data,station_data[['station_id','lat','lon']],'left',left_on = 'to_station_id',right_on = 'station_id')
    ride_data = ride_data.drop(columns = ['station_id_x','station_id_y'])
    ride_data = ride_data.rename(columns={'lat_x':'start_lat','lon_x':'start_lng','lat_y':'end_lat','lon_y':'end_lng'})
    #the distance f'n needs to have legit values or errors. So remove rows where the station data doesn't match the ride data
    #for station IDs / lat and long values
#    ride_data = ride_data.dropna(axes = 0, subset=['from_lat','from_lon','to_lat','to_lon'])
    ride_data = ride_data.dropna(subset=['start_lat','start_lng','end_lat','end_lng'])
#    ride_data['distance'] = ride_data.apply(lambda row: (distance.distance((row.start_lat, row.start_lng),
#                                    (row.end_lat, row.end_lng)).miles), axis='columns')
    return(ride_data)


# ===========================================

df19 = pd.DataFrame()
workd = '/media/adam/Data/GDrive/Python/DataSets/Data_Divvy/WorkFiles/'
# 2019-01-01 00:04:37
mydateparser = lambda x: datetime.strptime(x,'%Y-%m-%d %H:%M:%S')

file_names = glob.glob(workd+'*.csv')

for fname in file_names:
    print('processing',fname)
    df_temp = pd.read_csv(fname,
                          parse_dates = ['start_time','end_time'],date_parser = mydateparser)

    # subscribers gender is known, non-subscribers are not, so set gender to 'customer'
    df_temp['gender'].fillna('customer', inplace = True)

    # we're going to use lat, lon, so this isn't needed
    df_temp.drop(['from_station_name','to_station_name','usertype'],axis = 1, inplace = True)
         
    #convert trip duration from string to float
    df_temp['tripduration'] = df_temp['tripduration'].str.replace(',', '').astype(float)
 
    df19 = pd.concat([df19,df_temp])
    
print('getting station data')
station_df = get_station_data()

print('adding lat / long / distance')
df19 = add_lat_long(df19,station_df)

df20 = pd.DataFrame()
workd = '/media/adam/Data/GDrive/Python/DataSets/Data_Divvy/2020data/'
file_names = glob.glob(workd+'*.csv')

for fname in file_names:
    print('processing',fname)
    df_temp = pd.read_csv(fname,
                          parse_dates = ['started_at','ended_at'],date_parser = mydateparser)

    # subscribers gender is known, non-subscribers are not, so set gender to 'customer'
    # df_temp['gender'].fillna('customer', inplace = True)

    # we're going to use lat, lon, so this isn't needed
    df_temp.drop(['start_station_name','end_station_name'],axis = 1, inplace = True)
         
    #convert trip duration from string to float
    df_temp['tripduration'] = df_temp['ended_at'] - df_temp['started_at']
     
    df20 = pd.concat([df20,df_temp])

df19.rename(columns={'trip_id':'ride_id','start_time':'started_at',
                     'end_time':'ended_at'},inplace = True)
df19.drop(columns = ['from_station_id','to_station_id'])
df20.drop(columns = ['start_station_id','end_station_id'])


'''
# create a pivot table summarizing trip_duration and distance by gender
import numpy as np
gender_pt = df.pivot_table(['tripduration','distance'],'gender',aggfunc = np.mean,margins = True)
gender_pt.reset_index(level=0,inplace=True)

import seaborn as sns
sns.barplot(x='gender',y='tripduration',data=gender_pt)


# count of rides per month and per day
import calendar
rides_month = df.groupby(df['start_time'].dt.month).count().start_time
rides_dat = df.groupby(df['start_time'].dt.dayofweek).count().start_time


# count of rides per month AND per day (double index (1,0), (1,1), etc.)
import numpy as np
import calendar
rides_day_month = df.groupby([df['start_time'].dt.month.rename('month'),df['start_time'].dt.dayofweek.rename('day')]).count().start_time

import matplotlib.pyplot as plt
rides_day_month.unstack().plot(kind = 'bar',figsize = (26,16))
plt.legend(labels=[calendar.day_name[x] for x in range(0,7)],fontsize=16)
plt.title('Rides per day per month in Chicago',fontsize=20)
plt.ylabel('N rides',fontsize=16)
plt.xlabel('Month',fontsize=16);
plt.show()

# count the N of trips for each week of the year
rides_per_week = df.groupby(df['start_time'].dt.week.rename('week')).count().start_time
rides_per_week.plot()

dist_per_week = df.groupby(df['start_time'].dt.week.rename('week')).mean().distance
'''

