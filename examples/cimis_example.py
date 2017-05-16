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

from cimis import run_query, write_output_file


if __name__ == "__main__":
    xls_path = 'Fresno_state_precip_09012013.xlsx'
    appKey = 'acac78e2-860f-4194-b27c-ebc296745833'  # cimis appKey
    sites = [80]  #  query single site
    interval='daily' #options are:    daily, 
    start = '10-01-2016'
    end = '03-01-2017'
    site_names, cimis_data = run_query(appKey, sites, interval)
    #write data to excel file
    write_output_file(xls_path, cimis_data, site_names)

