# -*- coding: utf-8 -*-
"""
:DESCRIPTION:this script creates a db from the CIMIS station list for later retrieval

:REQUIRES:

:TODO:

:AUTHOR: John Franco Saraceno
:ORGANIZATION: U.S. Geological Survey, United States Department of Interior
:CONTACT: saraceno@usgs.gov
:VERSION: 0.1
Sat Nov 05 16:57:12 2016
"""
# =============================================================================
# IMPORT STATEMENTS
# =============================================================================
import json
import pickle
import urllib2
# =============================================================================
# METHODS
# =============================================================================


# =============================================================================
# MAIN METHOD AND TESTING AREA
# =============================================================================

station_url = 'http://et.water.ca.gov/api/station'

content = json.loads(urllib2.urlopen(station_url).read())
stations = content['Stations']
output = open('cimis_station_master.pkl', 'wb')
pickle.dump(stations, output)
StationNbr = []
Name = []

for i in stations:
    if i['IsActive'] == "True":
        StationNbr.append(i['StationNbr'])
        Name.append(i['Name'])

station_names = dict(zip(StationNbr, Name))
output = open('cimis_station_names.pkl', 'wb')
pickle.dump(station_names, output)


