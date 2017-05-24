# -*- coding: utf-8 -*-
"""
Created on Mon May 15 17:55:38 2017

@author: saraceno
"""
from __future__ import print_function
# -*- coding: utf-8 -*-
"""
cimis module
:DESCRIPTION: script to interact with DWR CIMIS Weather Station Network (WSN)
using Restful API
see http://et.water.ca.gov/Rest/Index for more information on API

This script supports pulling hourly or daily data by station number
station list is available here: http://www.cimis.water.ca.gov/Stations.aspx

:TODO:
1) add support to select specific parameters
2) when querying daily data, round convert now to yesterday
3) deal with return of no data when the start data covers a period when the station was down(?)
One solution would be to keep varying the start data until data is returned
4) Add ability to query station by name in addition to CIMIS number
:REQUIRES: pandas, urllib2

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

import datetime
import dateutil
import json
import pandas as pd
import urllib2

    
def write_output_file(xls_path, cimis_data, site_names):
    writer = pd.ExcelWriter(xls_path)
    for index, item in enumerate(cimis_data):
        print('Writing {} data to {}'.format(site_names[index],
                                             xls_path))
        item.to_excel(writer, sheet_name=site_names[index])
    writer.save()
    return


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
        print("There was an HTTPError when queriying CIMIS for station \
              information. Station info not available")


def retrieve_cimis_data(url, target):
    try:
        stations = retrieve_cimis_station_info()
        station = stations[str(target)]

        content = urllib2.urlopen(url).read()        
        print('Retrieving data for {}'.format(station))
        return json.loads(content)
    except urllib2.HTTPError as e:
        print("Could not resolve the http request for {}".format(station))
        error_msg = e.read()
        print(error_msg)
        if e.code == 400 and 'The report request exceeds the \
                              maximum data limit' in error_msg:
            print("Shorten the requested period of record.Try limiting \
                  the number of paramters or a maximum of 30 days for \
                  hourly data.")
    except urllib2.URLError as e:
        print(e.read())
        print('Could not access the CIMIS database.Verify that you have an \
               active internet connection and try again.')


def parse_cimis_data(records, target, Iteminterval):
    try:
        dates = []
        hours = []
        frames = []
        for i, day in enumerate(records):
            dates.append(day['Date'])
            hours.append(int(day.get('Hour', '0000'))/100)
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
        if Iteminterval == 'daily':
            dataframe.index = pd.to_datetime(dates)
        elif Iteminterval == 'default':
            dataframe.index = pd.to_datetime(dates)
        elif Iteminterval == 'hourly':
            dataframe.index = (pd.to_datetime(dates) +
                               pd.to_timedelta(hours, unit='h'))
        #print('Parsing data from station #{}'.format(target))
        return dataframe
    except ValueError:
        #        pass
        print('No data was found for this period. Station {} \
        may be inactive.'.format(target))


def convert_data_items(ItemInterval):
    # by default, grab all of the available paramters for each option
    # edit these lists for a custom query of parameters
    if ItemInterval == 'daily':  # daily data
        dataItems_list = ['day-air-tmp-avg',
                          'day-air-tmp-max',
                          'day-air-tmp-min',
                          'day-dew-pnt',
                          'day-eto',
                          'day-asce-eto',
                          'day-asce-etr',
                          'day-precip']
    elif ItemInterval == 'hourly':  # hourly
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
    elif ItemInterval == 'default':  # default CIMIS
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
                print('Cummulative precipitation at {0} for this period was \
                      {1:.2f} inches'.format(station_info[str(target)],
                                                  dataframe[field].sum()/25.4))


def cimis_to_dataframe(appKey, station, start, end, dataItems, Iteminterval):

    url = ('http://et.water.ca.gov/api/data?appKey=' + appKey + '&targets='
            + str(station) + '&startDate=' + start + '&endDate=' + end +
            '&dataItems=' + dataItems +'&unitOfMeasure=M')
    data = retrieve_cimis_data(url, station)
    try:
        dataframe = parse_cimis_data(data['Data']['Providers'][0]['Records'],
                                     station, Iteminterval)
        return dataframe
    except (TypeError, AttributeError):
        print('No data to parse')


def run_cimis(appKey, sites, start, end, Iteminterval):
    cimis_data = []
    dataItems = convert_data_items(Iteminterval)
    #station_info = retrieve_cimis_station_info(verbose=False)
    for target in sites:
        dataframe = cimis_to_dataframe(appKey, target, start, end, dataItems,
                                       Iteminterval)
        if isinstance(dataframe, pd.DataFrame):
            if dataframe is not None:
                #report_precip(dataframe, target, station_info)
                cimis_data.append(dataframe)
    return cimis_data

    
def relative_dates(months_ago=1):
    """ return a today date string and
    n months ago relative to todays date string"""
    today = datetime.datetime.now()
    one_month_ago = (today - 
                     dateutil.relativedelta.relativedelta(months=months_ago))
    today_str = today.strftime("%Y-%m-%d")
    one_month_ago_str = one_month_ago.strftime("%Y-%m-%d")

    return today_str,one_month_ago_str

    
def run_query(appKey, sites=[80], interval='daily', start='', end='',
              months_ago=1):
    # list of CIMIS station ID's from which to query data
    sites = [str(i) for i in sites]  # convert list of ints to strings
      #argument checking; TODO: find  a better way have default start and end dates
    n_months_ago = months_ago
    if not start:
    # start date fomat in YYYY-MM-DD      
        today, n_months_ago_today = relative_dates(months_ago=n_months_ago)
        start = n_months_ago_today 
    # end date fomat in YYYY-MM-DD
    # e.g. pull all data from start until today
    if not end:
        end = today
    # pull daily data; other options are 'hourly' and 'default'
    # edit convert_data_items function to customize list of queried parameters
    station_info = retrieve_cimis_station_info()
    pulled_site_names = [station_info[x] for x in sites]
    # retrieve the data for each station and place into a list of dataframes
    df = run_cimis(appKey, sites, start, end, interval)
    return pulled_site_names, df