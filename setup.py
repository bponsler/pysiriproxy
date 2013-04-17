#!/usr/bin/python
# Copyright (C) 2012 Brett Ponsler
# This file is part of pysiriproxy.
#
# pysiriproxy is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# pysiriproxy is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with pysiriproxy.  If not, see <http://www.gnu.org/licenses/>.
from sys import stderr
from os import environ
from os import listdir
from os.path import join, isfile
from setuptools import setup


# The list of external python modules that are required
_REQUIRED_MODULES = ["CFPropertyList", "zlib"]


def checkForModule(moduleName):
    '''Check that the given Python module name is installed and accessible. If
    it is not accessible, then exit

    * moduleName -- The module name that must be installed

    '''
    try:
        __import__(moduleName, globals(), locals(), [], -1)
    except ImportError, e:
        print >> stderr, e
        print >> stderr, "Error: pysiriproxy requires module [%s]" % moduleName
        print >> stderr, "Please install [%s] and try again!" % moduleName
        exit(1)


# Check for all the required modules
for moduleName in _REQUIRED_MODULES:
    checkForModule(moduleName)


setup(name='pysiriproxy',
      version='0.0.8',
      description='Python implementation of SiriProxy.',
      author='Brett Ponsler',
      author_email='ponsler@gmail.com',
      url='https://code.google.com/p/pysiriproxy/',
      packages=['pysiriproxy', 'pysiriproxy.connections',
                'pysiriproxy.objects', 'pysiriproxy.options',
                'pysiriproxy.plugins', 'pysiriproxy.testing'],
      include_package_data=True,
      license='GNU GPL v3',
      install_requires=[
        "biplist>=0.5",
        "twisted==12.1.0",
        "pyamp>=1.2",
        ],
      )
