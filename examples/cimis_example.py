# -*- coding: utf-8 -*-
"""
cimis_example.py
:DESCRIPTION: Example script to collect data from CIMIS using cimis module
This script reports cummulative precipitation, if available,
 for all CIMIS stations

:REQUIRES:datetime, json, pandas, urllib2 modules and cimis.py
app_key from CIMIS
See http://et.water.ca.gov/Home/Faq for more information

:TODO: add support to select specific parameters
when querying daily data, round convert now to yesterday


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
import numpy as np
import pandas as pd

from cimis import cimis_to_dataframe
from cimis import convert_data_items
from cimis import report_precip
from cimis import retrieve_cimis_station_info

# =============================================================================
# METHODS
# =============================================================================

# =============================================================================
# MAIN METHOD AND TESTING AREA
# =============================================================================


def main(app_key, sites, start, end, Iteminterval):
    cimis_data = []
    dataItems = convert_data_items(Iteminterval)
    station_info = retrieve_cimis_station_info(verbose=False)
    for target in sites:
        dataframe = cimis_to_dataframe(app_key, target, start, end, dataItems,
                                       Iteminterval)
        if isinstance(dataframe, pd.DataFrame):
            if dataframe is not None:
                report_precip(dataframe, target, station_info)
                cimis_data.append(dataframe)
    return cimis_data

if __name__ == "__main__":
    # enter custom CIMIS user app key, available from http://wwwcimis.water.ca.gov/
    appKey = 'acac78e2-860f-4194-b27c-ebc296745833'  # JFS appKey
    # list of CIMIS station ID's from which to quuery data
    sites = list(np.arange(2, 10, 1))
    # pull daily data; other options are 'hourly' and 'default'
    # edit convert_data_items function to customize list of queried parameters
    Iteminterval = 'hourly'
    # start date fomat in YYYY-MM-DD
    start = '2016-10-01'
    # end date fomat in YYYY-MM-DD
    # e.g. pull all data from start until today
    end = datetime.datetime.now().strftime("%Y-%m-%d")
    # retrieve the data for each station and place into a list of dataframes
    cimis_data = main(appKey, sites, start, end, Iteminterval)
