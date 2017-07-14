from setuptools import setup, find_packages
from runnerly.dataservice import __version__


setup(name='runnerly-data',
      version=__version__,
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      entry_points="""
      [console_scripts]
      runnerly-dataservice = runnerly.dataservice.run:main
      """)
