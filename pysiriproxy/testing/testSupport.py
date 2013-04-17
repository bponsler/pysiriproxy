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
'''The testSupport class contains classes and utility functions designed
to aid the process of writing test modules for pysiriproxy.

'''
from pysiriproxy.constants import Directions

from pyamp.logging import LogData, LogLevel, Colors


class Connection:
    '''The Connection class implements the basic functionality of a
    :class:`.connections.Connection` which is used in responding to a
    request from Siri. This Connection class is compatible with
    the :class:`.connections.ConnectionManager` and the :class:`.PluginManager`
    and is used for testing purposes.

    '''

    Direction = None
    '''The Direction property defines the direction that data is traveling for
    this Connection.

    '''

    RefId = None
    '''The RefId property defines the reference ID for this Connection.

    '''

    Callback = None
    '''The Callback property defines the callback function that is called
    in the event that an object is injected into the output stream of a
    connection.

    '''

    def __init__(self):
        '''Create a Connection.'''
        if self.Direction is None:
            raise Exception("Must define the Direction property!")

    @classmethod
    def getRefId(cls):
        '''Return the RefId for this Connection.'''
        return cls.RefId

    @classmethod
    def injectObjectToOutputStream(cls, obj):
        '''Inject the given object to the output stream.

        * obj -- The object to inject to the output stream

        '''
        if cls.Callback is not None:
            # Have to pass an instance of the Connection to the callback
            # function in order for it to work
            cls.Callback(cls(), obj)
        else:
            cls.__log(obj)

    @classmethod
    def getDirection(cls):
        '''Get the data direction for this Connection.'''
        return cls.Direction

    ##### Private functions #####

    @classmethod
    def __log(cls, message):
        '''Log an information message to the output.

        * message -- The message to log

        '''
        logger = LogData().get(cls.Direction, color=Colors.Foreground.Red)
        logger.info(message)


class iPhone(Connection):
    '''Create an iPhone Connection for testing.'''

    Direction = Directions.From_iPhone
    '''Define the direction for this Connection to indicate that it is from
    the iPhone.

    '''

    RefId = "iPhone refId"
    '''Define the reference ID for the iPhone Connection.'''


class Server(Connection):
    '''Create a Server Connection for testing.'''

    Direction = Directions.From_Server
    '''Define the direction for this Connection to indicate that it is from
    Apple's web server.

    '''

    RefId = "Server refId"
    '''Define the reference ID for the server Connection.'''
