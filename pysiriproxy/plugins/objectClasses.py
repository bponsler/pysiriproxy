# Copyright (C) 2012 Brett Ponsler, Pete Lamonica
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
'''The objectClasses module contains functions and attributes which are
used to create object class filters for plugins.

An object class filter is a plugin function which will be notified in the
event that pysiriproxy receives an object of a specific type (or class).

'''
import sys
from pysiriproxy.constants import ClassNames

from pyamp.patterns import listProperty


# The property name used to store the list of classes which is used to
# identify the object classes that a decorator function filters
_CLASSES_PROP = "Classes"


def createClassFilter(className):
    '''Create a function decorator which is used to filter received objects
    to find objects with the given class name.

    * className -- The class name used to filter received objects

    '''
    return listProperty(_CLASSES_PROP, className)


def isObjectClassFilter(function):
    '''Determine if the given function is an object class filter function.

    * function -- The function

    '''
    objectClasses = getObjectClasses(function)
    return objectClasses is not None and len(objectClasses) > 0


def getObjectClasses(function):
    '''Get the list of object classes that this filter function
    supports.

    * function -- The filter function

    '''
    return getattr(function, _CLASSES_PROP, [])


def objectClassesMatch(function, objectClass):
    '''Determine if the given object class is found in the list
    of object classes for this function.

    * function -- The function
    * objectClass -- The given object classes

    '''
    objectClasses = getObjectClasses(function)
    return objectClasses is None or len(objectClasses) == 0 or \
        objectClass in objectClasses


# Grab a reference to the current module object so we can add
# attributes to it
thisModule = sys.modules[__name__]

# Create class filter decorators for all of the known class names
for className in ClassNames.get():
    classFilter = createClassFilter(className)
    setattr(thisModule, className, classFilter)
