# -*- coding: utf-8 -*-
"""
cimis_example.py
:DESCRIPTION: Example script to collect data from CIMIS using cimis module
This script reports cummulative precipitation, if available,
 for all CIMIS stations

:REQUIRES:datetime, json, pandas, urllib2 modules and cimis.py
app_key from CIMIS
See http://et.water.ca.gov/Home/Faq for more information

:TODO:
1) add support to select specific parameters
2) when querying daily data, round convert now to yesterday
3) deal with return of no data when the start data covers a period when the station was down(?)
-keep varyuing the start data until data is returned
4) write output to a csv/xlsx file
:AUTHOR: John Franco Saraceno
:ORGANIZATION: U.S. Geological Survey, United States Department of Interior
:CONTACT: saraceno@usgs.gov
:VERSION: 0.1
Thu Nov 03 14:48:34 2016
"""
import datetime
import dateutil
from cimis import run_cimis, retrieve_cimis_station_info, write_output_file


def main():
    appKey = 'acac78e2-860f-4194-b27c-ebc296745833'  # cimis appKey
    # list of CIMIS station ID's from which to query data
    sites = [140]  # uncomment to query single site
    sites = [str(i) for i in sites]  # convert list of ints to strings
    ItemInterval = 'hourly'
    today = datetime.datetime.now()
    one_month_ago = today - dateutil.relativedelta.relativedelta(months=1)
    today_str = today.strftime("%Y-%m-%d")
    one_month_ago_str = one_month_ago.strftime("%Y-%m-%d")
    # start date fomat in YYYY-MM-DD
    start = one_month_ago_str
    # end date fomat in YYYY-MM-DD
    # e.g. pull all data from start until today
    end = today_str
    # pull daily data; other options are 'hourly' and 'default'
    # edit convert_data_items function to customize list of queried parameters
    station_info = retrieve_cimis_station_info()
    pulled_site_names = [station_info[x] for x in sites]
    # retrieve the data for each station and place into a list of dataframes
    df = run_cimis(appKey, sites, start, end, ItemInterval)
    return pulled_site_names, df


if __name__ == "__main__":
    xls_path = 'CIMIS_query_example.xlsx'
    site_names, cimis_data = main()
    write_output_file(xls_path, cimis_data, site_names)

