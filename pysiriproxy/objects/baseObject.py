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
'''The baseObject class contains the definition of the base class for
all objects that can be sent to the iPhone, or to Apple's web server.

'''
from uuid import uuid4

from pysiriproxy.constants import Keys


class SiriObject:
    '''The SiriObject class encapsulates the base functionality for all
    object being sent to the iPhone or to Apple's web server.

    .. note:: This class is meant to be subclassed to provide the
              implementation for a specific object.

    '''

    ProtocolVersion = "2.0"
    '''The identifier which indicates the version of the protocol.'''
  
    def __init__(self, className, group):
        '''
        * className -- The class name for the object
        * group -- The group name for the object

        '''
        self.__class = className
        self.__group = group

        self.__refId = None
        self.__aceId = None
        self.__version = None

    def setNonNoneArguments(self, argumentNames, localVars):
        '''Takes a list of strings which represent names of input variables and
        sets properties of the same name on the current object if the value of
        the argument is not None.

        * argumentNames -- The list of argument names to set
        * localVars -- The local variables

        '''
        for argName in argumentNames:
            # Get the value of the local argument
            argValue = localVars.get(argName)

            # Only set the argument if its value is not None
            if argValue is not None:
                setattr(self, argName, argValue)
  
    def toDict(self):
        '''Convert this object into a Python dictionary.'''
        dictionary = {
            Keys.Class: self.__class,
            Keys.Group: self.__group,
            Keys.Properties: {},
            }
      
        # Store the refId, aceId, and version values if we have one
        if self.__refId is not None:
            dictionary[Keys.RefId] = self.__refId
        if self.__aceId is not None:
            dictionary[Keys.AceId] = self.__aceId
        if self.__version is not None:
            dictionary[Keys.Version] = self.__version

        # Traverse all of the object's properties to add them each to
        # the output dictionary object
        for key, item in self.__getProperties().iteritems():
            # Determine how to handle the current property type
            if type(item) == type(list()):
                itemList = []

                # Convert all the items in the list to a dictionary, and keep
                # only the properties that are successfully converted
                for val in item:
                    try:
                        val = val.toDict()
                    except:
                        pass
                    itemList.append(val)

                dictionary[Keys.Properties][key] = itemList
            else:
                # Attempt to conver the current property into a dictionary
                try:
                    item = item.toDict()
                except:
                    pass

                dictionary[Keys.Properties][key] = item

        return dictionary

    def makeRoot(self, refId=None, aceId=None):
        '''Make the SiriObject the root object.

        * refId -- The refId for this object
        * aceId -- The aceId for this object

        '''
        self.setRefId(refId)
        self.setAceId(aceId)

        # Only the root object has a version entry
        self.__version = self.ProtocolVersion

    def setRefId(self, refId=None):
        '''Set the ref id for this object.

        * refId -- The refId for this object

        '''
        self.__refId = refId if refId is not None else self.__randomRefId()

    def setAceId(self, aceId=None):
        '''Set the ace id for this object.

        * aceId -- The aceId for this object

        '''
        self.__aceId = aceId if aceId is not None else self.__randomAceId()

    def __getProperties(self):
        '''Get all of the properties for this SiriObject.'''
        return dict((k, p) for k, p in self.__dict__.iteritems() \
                        if not k.startswith("_"))

    @classmethod
    def __randomRefId(cls):
        '''Create a random refId.'''
        return str(uuid4()).upper()

    @classmethod
    def __randomAceId(cls):
        '''Create a random aceId.'''
        return str(uuid4())

    @classmethod
    def isArgumentList(cls, obj):
        '''Determine if the given object is a list of arguments, or not.

        * obj -- The object
        
        '''
        return not SiriObject.isSiriObject(obj) and type(obj) == type(tuple())

    @classmethod
    def isSiriObject(cls, obj):
        '''Determine if the given object is a SiriObject, or not.

        * obj -- The object
        
        '''
        return isinstance(obj, SiriObject)
