# -*- coding: utf-8 -*-
"""
cimis_example.py
:DESCRIPTION: Example script to collect data from CIMIS using cimis module
This script reports ETo and cummulative precipitation, if available,
for a queried CIMIS station

:DEPENDENCIES: matplotlib, pandas, urllib2, cimis.py

:REQUIRES app_key from CIMIS

For more information see http://et.water.ca.gov/Home/Faq and/or README.md
(https://github.com/OneGneissGuy/cimis/blob/master/README.md)

:AUTHOR: John Franco Saraceno
:ORGANIZATION: U.S. Geological Survey, United States Department of Interior
:CONTACT: saraceno@usgs.gov
:VERSION: 0.1
Thu Nov 03 14:48:34 2016
"""

from cimis import run_query, write_output_file#, report_precip
from matplotlib import pyplot as plt

if __name__ == "__main__":
    ###################USER INPUTS#########################################
    #name of output file in which to write queried data
    #setup parameters for query
    appKey = 'acac78e2-860f-4194-b27c-ebc296745833'  # cimis unique appKey
    sites = [80]  #query single site or multiple
    xls_path = 'CIMIS_query.xlsx' # TODO: make this dep on stations/query date

    interval ='daily' #options are:    default, daily, hourly
    start = '10-01-2014' #self-explanatory
    end = '03-01-2017' #self-explanatory
    param  = 'DayEto'
    param1  = 'DayPrecip'

    #get the data as a list of data frames; one dataframe for each site
    site_names, cimis_data = run_query(appKey, sites, interval,
                                       start=start, end=end)
    #write queried data to excel file
    write_output_file(xls_path, cimis_data, site_names)
    
    #plot some some data and do some analysis
    params = cimis_data[0].columns.tolist()
    error_message = "{} was not in the list of available paramters. \
        Choose a parameter from the available paramters: {} \
        and try again.".format(param, params)
    #summarize the data
    if param in params:
        data = cimis_data[0][param]
        print('{} statistics for the period:\n{}'.format(param,
              data.describe()))
        data.plot(marker='o', label=data.name, legend=True)
    else:
        print(error_message)
    
    if param in params:
        data = cimis_data[0][param1]
        # calc and display the cummul precip in inches
        precip_cummul = data.sum()
        print('Cummulative precipitation for the period: {:.2f} inches'.format(precip_cummul/25.4))
        #visualize the data
        plt.figure()
        data.plot(marker='o', label=data.name, legend=True,)
        #apply some time series analysis
    else:
        print(error_message)
