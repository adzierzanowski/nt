'''
setup.py allows to install this package with pip
$ pip3 install . [--upgrade]
'''

from setuptools import setup
from nt.meta import __version__, __progname__

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
  include_package_data=True,
  install_requires=['afmt'],
  zip_safe=False,
  python_requires='>=3.6',
  entry_points={
    'console_scripts': [
      'nt = nt.__main__:main'
    ]
  },
  classifiers=[
    'Development Status :: 4 - Beta',
    'Environment :: Console',
    'Intended Audience :: End Users/Desktop',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Topic :: Office/Business :: Scheduling',
    'Topic :: Terminals',
    'Topic :: Utilities'
  ]
)
