#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug 31 12:30:33 2019

@author: adam
"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

def add_lat_long(ride_data,station_data):
    from geopy import distance

    ride_data = pd.merge(ride_data,station_data[['station_id','lat','lon']],'left',left_on = 'from_station_id',right_on = 'station_id')
    ride_data = pd.merge(ride_data,station_data[['station_id','lat','lon']],'left',left_on = 'to_station_id',right_on = 'station_id')
    ride_data = ride_data.drop(columns = ['station_id_x','station_id_y'])
    ride_data = ride_data.rename(columns={'lat_x':'from_lat','lon_x':'from_lon','lat_y':'to_lat','lon_y':'to_lon'})
    #the distance f'n needs to have legit values or errors. So remove rows where the station data doesn't match the ride data
    #for station IDs / lat and long values
    ride_data = ride_data.dropna(axes = 0, subset=['from_lat','from_lon','to_lat','to_lon'])
    ride_data['distance'] = ride_data.apply(lambda row: (distance.distance((row.from_lat, row.from_lon),
                                    (row.to_lat, row.to_lon)).miles), axis='columns')

    return(ride_data)

def clean_data(ride_df):
    #convert date time fields into dt format
    #ride_df['start_time'] = pd.to_datetime(ride_df['start_time'])
    #ride_df['end_time'] = pd.to_datetime(ride_df['end_time'])
    
    # we're going to use lat, lon, so this isn't needed
    ride_df.drop(['from_station_name','to_station_name'],axis = 1, inplace = True)
         
    #convert trip duration from string to float
    ride_df['tripduration'] = ride_df['tripduration'].str.replace(',', '').astype(float)

    # subscribers gender is known, non-subscribers are not, so set gender to 'customer'
    ride_df['gender'].fillna('customer', inplace = True)
    
    return ride_df

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

def generateBaseMap(default_location=[41.87,-87.64], default_zoom_start=12):
    # default location is chicago, medium zoom
    base_map = folium.Map(location=default_location, control_scale=True, zoom_start=default_zoom_start)
    return base_map

def add_date_time(ride_df):
    #add DOW field to the datafile
    ride_df = ride_df.assign(day = ride_df.start_time.dt.strftime('%w'))
    ride_df['day'] = ride_df['day'].astype(int)
    ride_df = ride_df.assign(start_hour = ride_df.start_time.dt.strftime('%-H'))
    ride_df['start_hour'] = ride_df['start_hour'].astype(int)
    
    return ride_df


# -------------------------------------------- #

#get some data
print('loading bike data')
date_cols = ['start_time','end_time']
bike_df = pd.read_csv('/media/adam/Data/DataSets/Divvy_Trips_2018_Q3.csv',parse_dates = date_cols)

print('getting station data')
station_df = get_station_data()

#df has 1.5M records; let's sample to get a more usable number
print('sampling bike data')
sample = bike_df.sample(n=5000)

print('cleaning sample')
sample = clean_data(sample)

print('adding lat / long columns')
sample = add_lat_long(sample,station_df)

# calc the average trip duration and distance for each gender
ride_pivot = sample.pivot_table(['tripduration','distance'],'gender',aggfunc = np.mean,margins = True)
ride_pivot.reset_index(level=0,inplace=True)

# add a speed column. Need to mult by 3600 to go from miles per sec to MPH
ride_pivot['speed'] = ride_pivot['distance'] / (ride_pivot['tripduration']) *3600

# this shows that the speed for F and M is about the same 5.2 mph
# for non-subscribers ('customers') the speed is 2.1 mph
# average trip distance is shortest for M (1.3m) and about the same for F and C (1.4m)
# ave trip length is least for M (15 min), F (16 min), C (43 min)
# non-subscribers don't go very far, but do so quite slowly!

sns.barplot(x='gender',y='tripduration',data=ride_pivot)
#graph it

# gender analysis:

sample['gender'].value_counts() / len(sample) * 100
# 58% are M, 21% F, 21% C (unknown gender)

sample = add_date_time(sample)

male_rd = sample[sample['gender'] == 'Male']
female_rd = sample[sample['gender'] == 'Female']
cust_rd = sample[sample['gender'] == 'customer']
subscriber_rd = sample[sample['gender'] != 'customer']

#create a new df with the percent of rides for each gender on a given day of week
dow = pd.DataFrame({'males':male_rd['day'].value_counts() / len(male_rd) * 100, 'females':female_rd['day'].value_counts() / len(female_rd) * 100, 'customers':cust_rd['day'].value_counts() / len(cust_rd) * 100})
#dow.reset_index(level=0,inplace = True)
dow.plot(kind='bar')
plt.xlabel('Day of week (0 = Sun)')
plt.ylabel('Percent')
plt.title('Percent of rides on each day by gender')
plt.show()

#Rides per . . .
'''A groupby operation involves a combination of splitting the object, 
applying a function, and combining the results. 

First, we group by time period (day,month,hour) .
'''
import calendar
rides_per_month = sample.groupby(sample['start_time'].dt.month).count().start_time
rides_per_month.index=[calendar.month_name[x] for x in range(rides_per_month.index.min(), rides_per_month.index.max() + 1)]

rides_per_day = sample.groupby(sample['start_time'].dt.dayofweek).count().start_time
rides_per_day.index=[calendar.day_name[x] for x in range(rides_per_day.index.min(), rides_per_day.index.max() + 1)]

rides_per_hour = sample.groupby(sample['start_time'].dt.hour).count().start_time

#plots
plt.style.use('ggplot')
rides_per_day.plot(kind = 'bar',figsize = (12,7), color = 'blue',alpha = 0.5)
plt.title('Rides per day',fontsize = 20)
plt.xlabel('Day of the week',fontsize = 16)
plt.ylabel('N rides')
plt.show()

rides_per_hour.plot(kind = 'bar',figsize = (12,7), color = 'blue',alpha = 0.5)
plt.title('Rides per hour',fontsize = 20)
plt.xlabel('Hour of the day',fontsize = 16)
plt.ylabel('N rides')
plt.show()

# create a df with rides per hour per day
ride_hour_day = sample.groupby([sample['start_time'].dt.hour.rename('hour'), sample['start_time'].dt.dayofweek.rename('day')]).count().start_time

#this creates a series with a double index (0,0) 5; (0,1) 2; etc.
#the unstack function will separate these into two
ride_hour_day.unstack().plot(kind = 'barh',figsize = (16,26))
plt.legend(labels=[calendar.day_name[x] for x in range(0,7)],fontsize=16)
plt.title('Rides per hour per day in Chicago',fontsize=20)
plt.xlabel('N rides',fontsize=16)
plt.ylabel('Hour',fontsize=16);
plt.show()

# Mapping
# https://towardsdatascience.com/analysis-of-car-accidents-in-barcelona-using-pandas-matplotlib-and-folium-73384240106b
# https://www.kaggle.com/daveianhickey/how-to-folium-for-maps-heatmaps-time-data

import folium
from folium import plugins

# set up backgroup map
chicago_bike_stations = generateBaseMap()

for lat, lon, stat_id, capacity in zip(station_df.lat, station_df.lon, station_df.station_id, station_df.capacity.astype(str)):
    folium.CircleMarker(
            [lat, lon],
            radius=int(capacity) / 5,
            color='red',
            fill=True,
            popup= str(stat_id) + ' ' + str(capacity),
            fill_color='darkred',
            fill_opacity=0.6
        ).add_to(chicago_bike_stations)
    
chicago_bike_stations.save('Chicago_bike_stations.html')

# try adding the cluster plugin. For this, points are added to the plugin (stats)
# which then displays them on the map

chicago_cluster = generateBaseMap()
stats = plugins.MarkerCluster().add_to(chicago_cluster)
for lat, lon, capacity in zip(station_df.lat, station_df.lon, station_df.capacity.astype(str)):
    folium.Marker(
            location = [lat, lon],
            popup = capacity,
            icon = None
        ).add_to(stats)
chicago_cluster.save('Chicago_Cluster.html')

#heat map

# heat map with time
from folium.plugins import HeatMapWithTime
chicago_heat_time = generateBaseMap()

# Nested list that contains the lat and lon of the different bike ride starts. 
hour_list = [[] for _ in range(24)]
for lat,log,hour in zip(sample.from_lat,sample.from_lon,sample.start_time.dt.hour):
    hour_list[hour].append([lat,log]) 

# Labels indicating the hours
index = [str(i)+' Hours' for i in range(24)]

# Instantiate a heat map wiht time object for the car accidents
HeatMapWithTime(hour_list, index).add_to(chicago_heat_time)
chicago_heat_time.save('Chicago_heat_time.html')





