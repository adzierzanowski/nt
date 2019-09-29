'''
setup.py allows to install this package with pip
$ pip3 install . [--upgrade]
'''

from setuptools import setup
from src.nt.meta import __version__, __progname__

with open('README.md', 'r') as f:
  long_desc = f.read()

setup(
  name=__progname__,
  version=__version__,
  description='todo list',
  long_description=long_desc,
  long_description_content_type='text/markdown',
  url='https://github.com/adzierzanowski/nt',
  author='Aleksander Dzierżanowski',
  author_email='a.dzierzanowski1@gmail.com',
  license='MIT',
  packages=['nt'],
  package_dir={'': 'src'},
  include_package_data=True,
  install_requires=['afmt'],
  scripts=['bin/nt'],
  zip_safe=False,
  python_requires='>=3.6',
  classifiers=[
    'Development Status :: 5 - Production/Stable',
    'Environment :: Console',
    'Intended Audience :: End Users/Desktop',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Topic :: Office/Business :: Scheduling',
    'Topic :: Terminals',
    'Topic :: Utilities'
  ]
)
