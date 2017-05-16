# -*- coding: utf-8 -*-
"""
cimis_example.py
:DESCRIPTION: Example script to collect data from CIMIS using cimis module
This script reports cummulative precipitation, if available,
 for all CIMIS stations

:REQUIRES: pandas, urllib2, cimis.py
app_key from CIMIS
See http://et.water.ca.gov/Home/Faq for more information

:AUTHOR: John Franco Saraceno
:ORGANIZATION: U.S. Geological Survey, United States Department of Interior
:CONTACT: saraceno@usgs.gov
:VERSION: 0.1
Thu Nov 03 14:48:34 2016
"""

from cimis import run_query, write_output_file#, report_precip


if __name__ == "__main__":
    #name of file to push data
    xls_path = 'Fresno_state_precip_09012013.xlsx'
    #setup parameters for query    
    appKey = 'acac78e2-860f-4194-b27c-ebc296745833'  # cimis unique appKey
    sites = [80]  #query single site or multiple
    interval ='daily' #options are:    default, daily, hourly
    start = '10-01-2014' #self-explanatory
    end = '03-01-2017' #self-explanatory
    #get the data as a list of data frames; one dataframe for each site
    site_names, cimis_data = run_query(appKey, sites, interval,
                                       start=start, end=end)
    #work with the first dataset in the list
    params = cimis_data[0].columns.tolist()
    #summarize the data    
    param = 'DayEto'
    et = cimis_data[0][param]
    print('{} stats for the period: {}'.format( param, et.describe()))
    et.plot(marker='o', label=et.name, legend=True)

    param = 'DayPrecip'
    data = cimis_data[0][param]
    precip_cummul = data.sum()
    print('Cummulative precip for the period: {} inches'.format(precip_cummul/25.4))

    #visualize the data
    data.plot(marker='o', label=data.name, legend=True)
    #apply some time series analysis
    
    #write data to excel file
    write_output_file(xls_path, cimis_data, site_names)

