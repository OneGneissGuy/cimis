try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

with open("README.md") as readme_file:
    readme = readme_file.read()


with open("LICENSE") as license_file:
    license = license_file.read()

setup(name='cimis',
      description='Python package to query DWR CIMIS WSN data',
      author='John Franco Saraceno',
      author_email='saraceno@usgs.gov',
      url='https://github.com/OneGneissGuy/cimis',
      version='1.0',
      packages=['cimis'],
      install_requires=['numpy', 'pandas', 'urllib2'],
      license=license,
      )
