'''
setup.py allows to install this package with pip
$ pip3 install . [--upgrade]
'''

from setuptools import setup
from src.nt.meta import __version__, __progname__

setup(
  name=__progname__,
  version=__version__,
  description='todo list',
  url='https://github.com/adzierzanowski/nt',
  author='Aleksander Dzierżanowski',
  author_email='a.dzierzanowski1@gmail.com',
  license='MIT',
  packages=['nt'],
  package_dir={'': 'src'},
  include_package_data=True,
  install_requires=[],
  scripts=['bin/nt'],
  zip_safe=False
)
