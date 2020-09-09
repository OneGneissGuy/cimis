# cimis : A python package to query the California Department of Water Resources CIMIS Weather Station Network (WSN) for meteorological data


`cimis` is a python wrapper for communication with the CIMIS WSN API.
Queried station data is returned as a pandas dataframe timeseries (or a list of dataframes in the case that multiple stations were queried). 
CIMIS station info is returned as a dictionary.

See http://et.water.ca.gov/Rest/Index for more information on the CIMIS API.

See examples/cimis_example.py for usage

Requirements:
--------------
### 1. CIMIS user account and appKey ###
### 2. python dependencies: ###

* datetime
* json
* numpy
* pandas
* urllib2

Example: Retrieve water year 2016 daily data from Twitchell Island, station 140
-------------------------------------------------------------------------------
```python

	import datetime
	from cimis import run_cimis, retrieve_cimis_station_info, write_output_file

	def main():
		appKey = ''  # cimis appKey
		# list of CIMIS station ID's from which to query data
		sites = [140]  # uncomment to query single site
		sites = [str(i) for i in sites]  # convert list of ints to strings
		ItemInterval = 'daily'
		# start date fomat in YYYY-MM-DD
		start = '2016-10-01'
		# end date fomat in YYYY-MM-DD
		# e.g. pull all data from start until today
		end = datetime.datetime.now().strftime("%Y-%m-%d")
		# pull daily data; other options are 'hourly' and 'default'
		# edit convert_data_items function to customize list of queried parameters
		station_info = retrieve_cimis_station_info()
		pulled_site_names = [station_info[x] for x in sites]
		# retrieve the data for each station and place into a list of dataframes
		df = run_cimis(appKey, sites, start, end, ItemInterval)
		return pulled_site_names, df


	if __name__ == "__main__":
		xls_path = 'CIMIS_query_example_daily.xlsx'
		site_names, cimis_data = main()
		write_output_file(xls_path, cimis_data, site_names)
```


Installation:
------------

Or you can get the full source code
https://github.com/OneGneissGuy/cimis

::

	$ git clone https://github.com/OneGneissGuy/cimis.git
	$ cd cimis
	$ python setup.py install


Disclaimer:
----------

This software is preliminary or provisional and is subject to revision. It is being provided to meet the need for timely
best science. The software has not received final approval by the U.S. Geological Survey (USGS). No warranty, expressed
or implied, is made by the USGS or the U.S. Government as to the functionality of the software and related material nor
shall the fact of release constitute any such warranty. The software is provided on the condition that neither the USGS
nor the U.S. Government shall be held liable for any damages resulting from the authorized or unauthorized use of the
software.

The USGS provides no warranty, expressed or implied, as to the correctness of the furnished software or the suitability
for any purpose. The software has been tested, but as with any complex software, there could be undetected errors. Users
who find errors are requested to report them to the USGS.

References to non-USGS products, trade names, and (or) services are provided for information purposes only and do not
constitute endorsement or warranty, express or implied, by the USGS, U.S. Department of Interior, or U.S. Government, as
to their suitability, content, usefulness, functioning, completeness, or accuracy.

Although this program has been used by the USGS, no warranty, expressed or implied, is made by the USGS or the United
States Government as to the accuracy and functioning of the program and related program material nor shall the fact of
distribution constitute any such warranty, and no responsibility is assumed by the USGS in connection therewith.

This software is provided "AS IS."


Author(s):
------
John Franco Saraceno, <jfsaraceno@gmail.com>

More information:
-----------------
* Python: https://www.python.org/
* pytest: http://pytest.org/latest/
* Sphinx: http://sphinx-doc.org/
* public domain: https://en.wikipedia.org/wiki/Public_domain
* CC0 1.0: http://creativecommons.org/publicdomain/zero/1.0/
* U.S. Geological Survey: https://www.usgs.gov/
* USGS: https://www.usgs.gov/
* U.S. Geological Survey (USGS): https://www.usgs.gov/
* United States Department of Interior: https://www.doi.gov/
* official USGS copyright policy: http://www.usgs.gov/visual-id/credit_usgs.html#copyright/
* U.S. Geological Survey (USGS) Software User Rights Notice: http://water.usgs.gov/software/help/notice/
* Python's download page: https://www.python.org/downloads/
* git: https://git-scm.com/
* Distutils: https://docs.python.org/3/library/distutils.html
* Installing Python Modules: https://docs.python.org/3.5/install/
* How Installation Works: https://docs.python.org/3.5/install/#how-installation-works
