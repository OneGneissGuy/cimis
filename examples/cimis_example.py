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
        dataframe = cimis_to_dataframe(app_key, target, start, end, dataItems)
        if isinstance(dataframe, pd.DataFrame):
            if dataframe is not None:
                report_precip(dataframe, target, station_info,
                              field='DayPrecip')
                cimis_data.append(dataframe)
    return cimis_data

if __name__ == "__main__":
    app_key = 'acac78e2-860f-4194-b27c-ebc296745833'
    sites = list(np.arange(2, 252, 1))
    start = '2016-10-01'
    # end = '2015-10-1'
    # yesterday
    end = datetime.datetime.now().strftime("%Y-%m-%d")
    Iteminterval = 'daily'

    cimis_data = main(app_key, sites, start, end, Iteminterval)
