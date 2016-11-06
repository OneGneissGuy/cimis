# -*- coding: utf-8 -*-
"""
:DESCRIPTION: script to interact with DWR CIMIS Weather Station Network (WSN)
using Restful API
This script supports pulling hourly or daily data by station
station list: http://www.cimis.water.ca.gov/Stations.aspx

see http://et.water.ca.gov/Rest/Index for more information on API
:REQUIRES:json, pandas, urllib2

:TODO:Add try catch to get_cimis_data

:AUTHOR: John Franco Saraceno
:ORGANIZATION: U.S. Geological Survey, United States Department of Interior
:CONTACT: saraceno@usgs.gov
:VERSION: 0.1
Thu Nov 03 14:48:34 2016
"""
# =============================================================================
# IMPORT STATEMENTS
# =============================================================================
import datetime
import json
import numpy as np
import pandas as pd
import urllib2
# =============================================================================
# METHODS
# =============================================================================
def retrieve_cimis_station_info(verbose=False):
    StationNbr = []
    Name = []
    station_url = 'http://et.water.ca.gov/api/station'
    try:
        content = json.loads(urllib2.urlopen(station_url).read())

        stations = content['Stations']
        for i in stations:
            if i['IsActive'] == "True":
                StationNbr.append(i['StationNbr'])
                Name.append(i['Name'])
        if verbose is True:
            return stations
        else:
            return dict(zip(StationNbr, Name))
    except urllib2.HTTPError:
        print "HTTPError, Station info not available"

def retrieve_cimis_data(url, target):
    try:
        return json.loads(urllib2.urlopen(url).read())
    except urllib2.HTTPError:
        print 'Could not resolve the http request for site #{}'.format(target)
#          print 'Adjust the requested parameters or start and end dates and try again'

def parse_cimis_data(records, target):
    try:
        dates = []
        frames = []
        for i, day in enumerate(records):
            dates.append(day['Date'])
            data_values = []
            col_names = []
            for key, values in day.iteritems():
                if isinstance(values, dict):
                    data_values.append(values['Value'])
                    df = pd.DataFrame(data_values, dtype=float)
                    col_names.append(key)
            df = df.transpose()
            df.columns = col_names
            frames.append(df)

        dataframe = pd.concat(frames)
        dataframe.index = pd.to_datetime(dates)
        return dataframe
    except ValueError:
        pass
#        print 'Station {} may be inactive as no data was found for this period. See http://www.cimis.water.ca.gov/Stations.aspx for station status.'.format(target)

def convert_data_items(ItemInterval):
    if ItemInterval is 'daily':  # daily data
        dataItems_list = ['day-air-tmp-avg',
                         'day-air-tmp-max',
                         'day-air-tmp-min',
                         'day-dew-pnt',
                         'day-eto',
                         'day-asce-eto',
                         'day-asce-etr',
                         'day-precip']
    elif ItemInterval is 'hourly':  # hourly
        dataItems_list = ['hly-air-tmp',
                         'hly-dew-pnt',
                         'hly-eto',
                         'hly-net-rad',
                         'hly-asce-eto',
                         'hly-asce-etr',
                         'hly-precip',
                         'hly-rel-hum',
                         'hly-res-wind',
                         'hly-soil-tmp',
                         'hly-sol-rad',
                         'hly-vap-pres',
                         'hly-wind-dir',
                         'hly-wind-spd']
    elif ItemInterval is 'default':  # default CIMIS
        dataItems_list =  ['day-asce-eto',
                             'day-precip',
                             'day-sol-rad-avg',
                             'day-vap-pres-avg',
                             'day-air-tmp-max',
                             'day-air-tmp-min',
                             'day-air-tmp-avg',
                             'day-rel-hum-max',
                             'day-rel-hum-min',
                             'day-rel-hum-avg',
                             'day-dew-pnt',
                             'day-wind-spd-avg',
                             'day-wind-run',
                             'day-soil-tmp-avg']
    else:  # by default just grab daily airtemp
        dataItems_list = ['day-air-tmp-avg']
    dataItems = ','.join(dataItems_list)
    return dataItems
# =============================================================================
# MAIN METHOD AND TESTING AREA
# =============================================================================

app_key = 'acac78e2-860f-4194-b27c-ebc296745833'
sites = ['2','8','127']
sites = [2]
sites = list(np.arange(2,252,1))
start = '2016-10-01'
end = '2015-10-1'
#yesterday
end = datetime.datetime.now().strftime("%Y-%m-%d")
#-datetime.timedelta(days=1)
#end = end.strftime("%Y-%m-%d")
Iteminterval = 'daily'
dataItems = convert_data_items(Iteminterval)

cimis_data = []
station_info = retrieve_cimis_station_info(verbose=False)
for target in sites:
    url ='http://et.water.ca.gov/api/data?appKey=' + app_key + '&targets=' + str(target) + '&startDate=' + start + '&endDate=' + end + '&dataItems=' + dataItems +'&unitOfMeasure=M'
#        url = 'http://et.water.ca.gov/api/data?appKey='+app_key+'&targets=2&startDate=2010-01-01&endDate=2010-02-07&dataItems=hly-air-tmp,hly-dew-pnt,hly-eto,hly-net-rad,hly-asce-eto,hly-asce-etr,hly-precip,hly-rel-hum,hly-res-wind,hly-soil-tmp,hly-sol-rad,hly-vap-pres,hly-wind-dir,hly-wind-spd&unitOfMeasure=M'
#    data = retrieve_cimis_data(url, target)
    data = retrieve_cimis_data(url, target)
    try:
        dataframe = parse_cimis_data(data['Data']['Providers'][0]['Records'], target)
        if dataframe is not None:
            cimis_data.append(dataframe)
    except (TypeError, AttributeError):
        print 'No data to parse'
#    except AttributeError:
 #   try:

 #   except NameError:
  #      print 'There was no dataframe to concatenate for site: {}'.format(target)
    field = 'DayPrecip'
    if isinstance(dataframe, pd.DataFrame):
        if field in dataframe.columns:
            if str(target) in station_info.keys():
                print 'WY 2016 total rainfall at {0}: {1:.2f} (in)'.format(station_info[str(target)], dataframe[field].sum()/25.4)
