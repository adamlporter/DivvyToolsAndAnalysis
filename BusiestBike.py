#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 11 06:00:52 2019

@author: adam
"""

import pandas as pd

raw = pd.read_csv('/media/adam/Data/DataSets/Divvy_Trips_2018_Q3.csv')

raw['start_time'] = pd.to_datetime(raw['start_time'])
raw['end_time'] = pd.to_datetime(raw['end_time'])
raw = raw.assign(doy = raw.start_time.dt.strftime('%j'))
# convert strings to date/time
# add column to table of day of year (doy)
                                                  
day_usage = raw['doy'].value_counts() # what day had the highest usage?

day_use_df = day_usage.to_frame() # convert seriest to df
day_use_df['day'] = day_use_df.index # add the index values to the df

sel_rows = raw[raw['doy'] == '209'] # get the rows for the highest use day

busy_bike = sel_rows['bikeid'].value_counts() # what is the busiest bike on that day?
busy_bike = busy_bike.to_frame()
busy_bike = busy_bike.rename(index = str, columns={'bikeid':'n_rides'})
busy_bike['bikeid'] = busy_bike.index

bike_num = busy_bike[busy_bike['n_rides']==busy_bike['n_rides'].max()]['bikeid']


