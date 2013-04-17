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
'''The dataObjects module contains classes pertaining to creating objects which
can be sent to the iPhone or Apples' web server which contain various types of
data to be displayed to the user.

'''
from pysiriproxy.objects.baseObject import SiriObject


class _Location(SiriObject):
    '''The _Location class provides the ability to create a
    :class:`.SiriObject` which contains a specific map location to be
    displayed to the user.

    '''

    def __init__(self, label=None, street=None, city=None, stateCode=None,
                 countryCode=None, postalCode=None, latitude=None,
                 longitude=None):
        '''
        * label -- The label for the location
        * street -- The street for the location
        * city -- The city of the location
        * stateCode -- The state code for the location
        * countryCode -- The country code for the location
        * postalCode -- The postal code for the location
        * latitude -- The latitude for the location
        * longitude -- The longitude for the location

        '''
        SiriObject.__init__(self, "Location", "com.apple.ace.system")

        names = ["label", "street", "city", "stateCode", "countryCode",
                 "postalCode", "latitude", "longitude"]

        # Set all of the arguments so long as their values are not None
        self.setNonNoneArguments(names, locals())


class _Answer(SiriObject):
    '''The _Answer class creates an object which is Siri's answer to
    a user's question.

    '''

    def __init__(self, title="", lines=None):
        '''
        * title -- The title for the answer
        * lines -- The lines of text for the answer

        '''
        SiriObject.__init__(self, "Object", "com.apple.ace.answer")
        self.title = title
        self.lines = [] if lines is None else lines


class _AnswerLine(SiriObject):
    '''The _AnswerLine creates a single line for Siri's answer to a
    user's question.

    '''

    def __init__(self, text="", image=""):
        '''
        * text -- The text to display
        * image -- The image to display

        '''
        SiriObject.__init__(self, "ObjectLine", "com.apple.ace.answer")
        self.text = text
        self.image = image


class _MapItem(SiriObject):
    '''The _MapItem creates an object that displayed to the user as a
    map item.

    '''
    def __init__(self, label=None, location=None, detailType="BUSINESS_ITEM"):
        '''
        * label -- The label for the map item
        * location -- The :class:`._Location` object for the map item
        * detailType -- The detail type for this map item

        '''
        SiriObject.__init__(self, "MapItem", "com.apple.ace.localsearch")

        self.detailType = detailType

        names = ["label", "location"]

        # Set all of the arguments so long as their values are not None
        self.setNonNoneArguments(names, locals())


class _CurrentLocation(_MapItem):
    '''The _CurrentLocation class creates an object that displays the user's
    current location as a map item.

    '''
    __DetailType = 'CURRENT_LOCATION'
    
    def __init__(self, label=None):
        '''
        * label -- The label for this map item

        '''
        _MapItem.__init__(self, label=label, detailType=self.__DetailType)


class DataObjects:
    '''The DataObjects class provides definitions of various types of objects
    to display data to the Siri user.

    This class also provides a factory method for creating objects of specific
    types.

    '''
    Location = "Location"
    '''The object type corresponding to a map location.'''

    Answer = "Answer"
    '''The object type corresponding to Siri's answer to a user's question.'''

    AnswerLine = "AnswerLine"
    '''The object type corresponding to a single answer line.'''

    MapItem = "MapItem"
    '''The object type corresponding to creating an item on a map.'''

    CurrentLocation = "CurrentLocation"
    '''The object type corresponding to creating an item on a map corresponding
    to the iPhone's current location.

    '''

    __TypeMap = {
        Location: _Location,
        Answer: _Answer,
        AnswerLine: _AnswerLine,
        MapItem: _MapItem,
        CurrentLocation: _CurrentLocation,
        }

    @classmethod
    def create(cls, objectType, *args, **kwargs):
        '''Create a DataObject of the given type.

        * dataObject -- The type of DataObject to create
        * args -- The arguments
        * kwargs -- The keyword arguments

        '''
        dataObject = None

        # Create the button object if it is found
        objectClass = DataObjects.__TypeMap.get(objectType)
        if objectClass is not None:
            dataObject = objectClass(*args, **kwargs)

        return dataObject
