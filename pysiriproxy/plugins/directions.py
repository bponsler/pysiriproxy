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
'''The directions module contains classes for creating decorators that allow
functions to match objects that were recieved from a specific source (e.g.,
from the iPhone).

'''
from pysiriproxy.constants import Directions

from pyamp.patterns import listProperty


# Define the property name used to store the directions for a function
_DIRECTIONS_PROP = "Directions"


def _addDirection(direction):
    '''Create a function decorator which adds the given direction to
    the directions property for the function.

    * direction -- The direction

    '''
    return listProperty(_DIRECTIONS_PROP, direction)


def getDirections(function):
    '''Get the list of directions for the given function.

    * function -- The function

    '''
    return getattr(function, _DIRECTIONS_PROP, [])


def isDirectionFilter(function):
    '''Determine if the given function is a directions filter.

    * function -- The function

    '''
    directions = getDirections(function)
    return directions is not None and len(directions) > 0


def directionsMatch(function, direction):
    '''Determine if the given direction is found in the list
    of directions for this function.

    * function -- The function
    * direction -- The given direction

    '''
    directions = getDirections(function)
    return directions is None or len(directions) == 0 \
        or direction in directions


# Define all of the direction decorators
From_iPhone = _addDirection(Directions.From_iPhone)
'''The From_iPhone property is a decorator which can be used to allow
functions to match objects that are received from the iPhone.

'''

From_Server = _addDirection(Directions.From_Server)
'''The From_Server property is a decorator which can be used to allow
functions to match objects that are received from Apple's web server.

'''
