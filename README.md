# DivvyToolsAndAnalysis

# DivvyToolsAndAnalysis
## This directory has a bunch of files related to the DIVVY bike share program in Chicago.

### Pre-2020 data
I've worked with the data from 2017-2021. The trip info files from before 2020 included the following fields:
0. trip_id
1. start_time
2. end_time
3. bikeid
4. tripduration
5. from_station_id
6. from_station_name
7. to_station_id
8. to_station_name
9. usertype
10. gender
11. birthyear

The station names and IDs are not terribly helpful in terms of mapping, etc., so in the DataMunging notebook, I documented how to merge them with station data, to end up with the following fields:

0   trip_id
1   start_time
2   end_time
3   bikeid
4   tripduration
5   from_station_id
6   from_station_name
7   to_station_id
8   to_station_name
9   usertype
10  gender
11  birthyear
12  start_lat
13  start_lng
14  end_lat
15  end_lng

### 2020-and after data

Starting in 2020, DIVVY dropped (a) trip duration, (b) bikeid, (c) gender, and (d) birthyear. Losing c and d are unfortunate, as they allow some demographic analysis of who is using the Divvy system. 
It renamed the (a) station fields, (b) the time fields, and (c) usertype became "member_casual".
It started recording (a) the sort of bike used ('ridable_type') and (b) lat/long itself. 

0   ride_id
1   rideable_type
2   started_at
3   ended_at
4   start_station_name
5   start_station_id
6   end_station_name
7   end_station_id
8   start_lat
9   start_lng
10  end_lat
11  end_lng
12  member_casual
