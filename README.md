cimis : Query CA DWR CIMIS Weather Station Network (WSN)for meterological data
=============================================================

cimis is a python project which allows communication with the CIMIS WSN api.

The main features include routine automatic collecting of data from stations 
and returns data as a dataframe or in the instance of several stations,
a list of dataframes.
CIMIS station info can be queried and returned as a dictionary of dictionaries.

see http://et.water.ca.gov/Rest/Index for more information on API


Requirements:
-------------
datetime
json
numpy
pandas
urllib2

:::python
#Example: Retrieve data from Twitchell Island

	import datetime
	import numpy as np
	from cimis import run_cimis,retrieve_cimis_station_info

	def main():
		appKey = ''  # Unique user appKey 
		# list of CIMIS station ID's from which to query data
		sites = [140]
		# pull daily data; other options are 'hourly' and 'default'
		# edit convert_data_items function to customize list of queried parameters
		Iteminterval = 'daily'
		# start date fomat in YYYY-MM-DD
		start = '2016-10-01'
		# end date fomat in YYYY-MM-DD
		# e.g. pull all data from start until today
		end = datetime.datetime.now().strftime("%Y-%m-%d")
		# retrieve the data for each station and place into a list of dataframes
		return run_cimis(appKey, sites, start, end, Iteminterval)

	if __name__ == "__main__":
		station_info = retrieve_cimis_station_info(verbose=True)
		cimis_data = main()


--------


Features:
--------

Installation
------------

Or you can get the source code from bitbucket
https://bitbucket.org/geofranco/cimis

::

	$ git clone https://geofranco@bitbucket.org/geofranco/cimis.git
	$ cd cimis
	$ python setup.py install



