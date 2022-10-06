#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 11 19:11:23 2019

@author: adam
"""

import numpy as np
import pandas as pd

def bar_freq_count(series_data):
    import matplotlib.pyplot as plt
    # this will take a frequency count series and sort it by the index
    # then present it in a bar chart
    # https://pythonspot.com/matplotlib-bar-chart/
    
    series_data.sort_index(inplace = True)
    bar_heights = series_data.tolist()
    y_pos = np.arange(len(bar_heights))
    plt.ylabel('N rides')
    plt.xlabel(series_data.name)
    plt.title('divvy bike frequency usage by ')
    plt.bar(y_pos,bar_heights,align = 'center')

workDir = '/home/alp/Google Drive/Python/DataSets/Data_Divvy/'
raw4 = pd.read_csv(workDir + 'Divvy_Trips_2018_Q4.csv',parse_dates=['start_time','end_time']

# convert str columns to specific data types
raw['start_time'] = pd.to_datetime(raw['start_time'])
raw['end_time'] = pd.to_datetime(raw['end_time'])
raw['tripduration'] = raw['tripduration'].str.replace(',','').astype(float)

# add doy (day of year) column
raw = raw.assign(doy = raw.start_time.dt.strftime('%j'))
# add month column
raw = raw.assign(month = raw.start_time.dt.strftime('%m'))
# create new hour column
raw = raw.assign(hour = raw.start_time.dt.strftime('%H'))
# create new hour column
raw = raw.assign(dow = raw.start_time.dt.strftime('%w'))
 # create new DOW column with 0 - 6 values
raw = raw.assign(tripdur_min = raw['tripduration']/60)


use_by_date = raw['doy'].value_counts() # frequency counts
#use_by_date.sort_index(inplace = True)

bar_freq_count(use_by_date)
bar_freq_count(raw['hour'].value_counts())

# pivot table analysis
# by DOW - average trip length and number
dow_table = pd.pivot_table(raw,index = 'dow',values = 'tripduration',aggfunc=[np.mean,len])

# by hour in day 
hour_table = pd.pivot_table(raw,index = 'hour',values = 'tripduration',aggfunc=[np.mean,len])
