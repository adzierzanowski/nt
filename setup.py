from setuptools import setup
from src.nt.meta import PROGNAME, VERSION, DESC

setup(
  name=PROGNAME,
  version=VERSION,
  description=DESC,
  url='',
  author='Aleksander Dzierżanowski',
  author_email='a.dzierzanowski1@gmail.com',
  license='MIT',
  packages=['nt'],
  package_dir={'': 'src'},
  include_package_data=True,
  install_requires=[''],
  scripts=['bin/nt'],
  zip_safe=False
)
