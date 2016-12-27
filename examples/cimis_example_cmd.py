# -*- coding: utf-8 -*-
"""
cimis_example_cmd.py
:DESCRIPTION: Example command line script to collect data from CIMIS using
cimis module

USAGE:

cimis_example_cmd.py <sites> <outfile> <appkey> -i hourly -b 2016-10-01 -e 2016-11-01

example: cimis_example_cmd.py 140 outfile.xlsx appkey -i hourly -b 2016-10-01 -e 2016-11-01

REQUIRED postional args are:

sites, a space delimited station list, e.g. 140 220 300

outfile, name of output xlsx file, e.g. outfile.xlsx

appKey, your custom cimis appkey, e.g. acac78e2-817f-4194-e27c-eac296745833

OPTIONS are:

-i, --data_interval [hourly]. Sample interfval,options are hourly, daily or default.Default is daily.

-b, --begin [YYYY-MM-DD]. Begin date, e.g. 2016-10-01. Default is one month ago.

-e, --end [YYYY-MM-DD].End data, e.g. 2016-11-01. Default is today.


:REQUIRES:datetime, json, pandas, urllib2 modules and cimis.py
app_key from CIMIS
See http://et.water.ca.gov/Home/Faq for more information

:AUTHOR: John Franco Saraceno
:ORGANIZATION: U.S. Geological Survey, United States Department of Interior
:CONTACT: saraceno@usgs.gov

:VERSION: 0.1
Thu Nov 03 14:48:34 2016
"""
# =============================================================================
# IMPORT STATEMENTS
# =============================================================================
import argparse
import datetime
import dateutil
from cimis import run_cimis, retrieve_cimis_station_info, write_output_file

# =============================================================================
# METHODS
# =============================================================================

# =============================================================================
# MAIN METHOD AND TESTING AREA
# =============================================================================


def arg_parser():
#    today = datetime.datetime.now().strftime("%Y-%m-%d") # string

    today = datetime.datetime.now()
    one_month_ago = today - dateutil.relativedelta.relativedelta(months=1)
    today_str = today.strftime("%Y-%m-%d")
    one_month_ago_str = one_month_ago.strftime("%Y-%m-%d")
    parser = argparse.ArgumentParser(description='CIMIS DATA QUERY SCRIPT')
    parser.add_argument('sites', type=int, nargs='+',
                        help='Space delimited sites number(s)',)
    parser.add_argument('outfile', type=str,
                        help='Output filename')
    parser.add_argument('appKey', type=str,
                        help='personal app key from CIMIS',)
    parser.add_argument('-i', '--data_interval', type=str,
                        help='data interval: options are daily or hourly',
                        required=False, default='daily')
    parser.add_argument('-b', '--start', type=str, default=one_month_ago_str,
                        help='start date of format YYYY-MM-DD; default is start of 2016 WY',
                        required=False)
    parser.add_argument('-e', '--end', type=str,
                        help='end date, default is todays date',
                        required=False,
                        default=today_str)
    args = parser.parse_args()
    return dict(vars(args).items())


def main(**kwargs):

    # list of CIMIS station ID's from which to query data

    sites = kwargs.get('sites')#, list([140]))
    # JFS appKey by default
    appKey = kwargs.get('appKey')#,'acac78e2-860f-4194-b27c-ebc296745833')

    # pull daily data; other options are 'hourly' and 'default'
    data_interval = kwargs.get('data_interval', 'daily')
    today = datetime.datetime.now()
    one_month_ago = today - dateutil.relativedelta.relativedelta(months=1)
    today_str = today.strftime("%Y-%m-%d")
    one_month_ago_str = one_month_ago.strftime("%Y-%m-%d")

    # start date fomat in YYYY-MM-DD
    start = kwargs.get('start', one_month_ago_str)
    if start is None:
        start = one_month_ago_str
    end = kwargs.get('end', today_str)
    if end is None:
        end = today_str
    """Defaults"""
    #    appKey = ''  # JFS appKey
        # sites = [140]  # uncomment to query single site
    #    data_interval = 'daily'
        # start date fomat in YYYY-MM-DD
    #    start = '2016-10-01'
        # end date fomat in YYYY-MM-DD
        # e.g. pull all data from start until today
    #    end = datetime.datetime.now().strftime("%Y-%m-%d")
    """End defaults"""
    sites = [str(i) for i in sites]  # convert list of ints to strings
    station_info = retrieve_cimis_station_info()
    pulled_site_names = [station_info[x] for x in sites]

    # retrieve the data for each station and place into a list of dataframes
    df = run_cimis(appKey, sites, start, end, data_interval)
    return pulled_site_names, df


if __name__ == "__main__":
    kw_args = arg_parser()
    site_names, cimis_data = main(**kw_args)
    xls_path = kw_args.get('outfile','CIMIS_cmd_line_query.xlsx')
    write_output_file(xls_path, cimis_data, site_names)
