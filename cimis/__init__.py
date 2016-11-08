# -*- coding: utf-8 -*-
"""
cimis module
:DESCRIPTION: script to interact with DWR CIMIS Weather Station Network (WSN)
using Restful API
see http://et.water.ca.gov/Rest/Index for more information on API

This script supports pulling hourly or daily data by station number
station list is available here: http://www.cimis.water.ca.gov/Stations.aspx

:REQUIRES:json, pandas, urllib2

:TODO:
:AUTHOR: John Franco Saraceno
:ORGANIZATION: U.S. Geological Survey, United States Department of Interior
:CONTACT: saraceno@usgs.gov
:VERSION: 0.1
Thu Nov 03 14:48:34 2016
"""
# =============================================================================
# IMPORT STATEMENTS
# =============================================================================
import json
import pandas as pd
import urllib2


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
        print "There was an HTTPError when queriying CIMIS for station \
        information. Station info not available"


def retrieve_cimis_data(url, target):
    try:
        content = urllib2.urlopen(url).read()
        print 'Retrieving data for station #{}'.format(target)
        return json.loads(content)
    except urllib2.HTTPError:
        print 'Could not resolve the http request for station \
        #{}'.format(target)
    except urllib2.URLError:
        print 'Could not access the CIMIS database.Verify that you have an\
        active internet connection and try again.'


def parse_cimis_data(records, target, Iteminterval):
    try:
        dates = []
        hours = []
        frames = []
        for i, day in enumerate(records):
            dates.append(day['Date'])
            hours.append(int(day.get('Hour','0000'))/100)
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
        if Iteminterval is ('daily'  or 'default'):
            dataframe.index = pd.to_datetime(dates)
        elif Iteminterval is 'hourly':
            dataframe.index = (pd.to_datetime(dates) +
                               pd.to_timedelta(hours, unit='h'))
        print 'Parsing data from station #{}'.format(target)
        return dataframe
    except ValueError:
        #        pass
        print 'No data was found for this period. Station {} \
        may be inactive.'.format(target)


def convert_data_items(ItemInterval):
    # by default, grab all of the available paramters for each option
    # edit these lists for a custom query of parameters
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
        dataItems_list = ['day-asce-eto',
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


def report_precip(dataframe, target, station_info,):
        field = 'DayPrecip'
        if field in dataframe.columns:
            if str(target) in station_info.keys():
                print 'Cummulative precipitation at {0} for this \
                period was {1:.2f} inches'.format(station_info[str(target)],
                                                  dataframe[field].sum()/25.4)


def cimis_to_dataframe(appKey, station, start, end, dataItems, Iteminterval):
    url = ('http://et.water.ca.gov/api/data?appKey=' + appKey + '&targets='
            + str(station) + '&startDate=' + start + '&endDate=' + end +
            '&dataItems=' + dataItems +'&unitOfMeasure=M')
    #    url = ('http://et.water.ca.gov/api/data?appKey='+appKey+'&targets=140&startDate=2010-01-01&endDate=2010-02-07&dataItems=hly-air-tmp,hly-dew-pnt,hly-eto,hly-net-rad,hly-asce-eto,hly-asce-etr,hly-precip,hly-rel-hum,hly-res-wind,hly-soil-tmp,hly-sol-rad,hly-vap-pres,hly-wind-dir,hly-wind-spd&unitOfMeasure=M')
    # data = retrieve_cimis_data(url, target)
    #    print url
    data = retrieve_cimis_data(url, station)
    try:
        dataframe = parse_cimis_data(data['Data']['Providers'][0]['Records'],
                                     station, Iteminterval)
        return dataframe
    except (TypeError, AttributeError):
        print 'No data to parse'


def run_cimis(appKey, sites, start, end, Iteminterval):
    cimis_data = []
    dataItems = convert_data_items(Iteminterval)
    station_info = retrieve_cimis_station_info(verbose=False)
    for target in sites:
        dataframe = cimis_to_dataframe(appKey, target, start, end, dataItems,
                                       Iteminterval)
        if isinstance(dataframe, pd.DataFrame):
            if dataframe is not None:
                report_precip(dataframe, target, station_info)
                cimis_data.append(dataframe)
    return cimis_data
