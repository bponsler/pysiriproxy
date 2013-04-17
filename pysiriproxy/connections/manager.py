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
'''The manager module contains the ConnectionManager class which is
responsible for managing the ability to transfer data between two
different connections.

'''
from pysiriproxy.constants import Directions

from pyamp.logging import LogData, Colors


class ConnectionManager:
    '''The ConnectionManager object managers incoming connection
    directions and provides the ability to forward data between them.

    It allows a connection direction to be connected to an opposite
    connection direction which allows data to be forwarded from the
    direction to the connected direction.

    '''
    # Implement the borg pattern
    __shared_state = {}

    def __init__(self, logger=None):
        '''
        * logger -- The logger

        '''
        self.__dict__ = self.__shared_state

        # If the manager has not been initialized, then initialize it
        if getattr(self, "_initialized", False) == False:
            # Create a map of directions to connection objects
            self._connections = {
                Directions.From_iPhone: None,
                Directions.From_Server: None,
                }

            # Map incoming direction, to its forwarding direction
            self._forwardMap = {
                Directions.From_iPhone: Directions.From_Server,
                Directions.From_Server: Directions.From_iPhone
                }

            # String readable versions of the directions
            self._nameMap = {
                Directions.From_iPhone: "iPhone",
                Directions.From_Server: "Server",
                }

            # Create the logger for this class
            if logger is None:
                logger = LogData()
            self._log = logger.get("ConnectionManager",
                                   color=Colors.Foreground.Orange)

            # The connection manager has now been initialized
            self._initialized = True

    def connect(self, connection):
        '''Add a connection to our set of connections.

        * connection -- The connection object to add

        '''
        direction = connection.getDirection()

        # Only add the connection a single time
        if self._connections.get(direction) is None:
            strDirection = self.__getName(direction)
            self._log.debug("Connected [%s]" % strDirection, level=0)

            self._connections[direction] = connection

    def disconnect(self, direction):
        '''Remove a directed connection from our set of connections.

        * direction -- The direction of the connection object to remove

        '''
        # Only remove the connection a single time
        if direction in self._connections:
            connection = self._connections[direction]
            if connection is not None:
                # Close the connection, and then remove it from the
                # dictionary of connections
                connection.transport.loseConnection()
                del self._connections[direction]

    def forward(self, direction, data):
        '''Forward the data from one connection to another.

        * direction -- The direction of the data
        * data -- The data to forward

        '''
        forwarded = False

        # Get the forwarding direction, and connection
        forwardDirection = self._forwardMap.get(direction)
        forwardConnection = self._connections.get(forwardDirection) 

        # If the connection is found, forward the data
        if forwardConnection is not None:
            strDirection = self.__getName(forwardDirection)
            self._log.debug("Forwarding %d bytes of data to %s" \
                                % (len(data), strDirection), level=5)
            forwardConnection.transport.write(data)
            forwarded = True

        return forwarded

    def resetConnections(self):
        '''Reset all of the connections that are being managed.'''
        for connection in self._connections.values():
            if connection is not None:
                connection.reset()
        
    def hasConnection(self, direction):
        '''Determine if there is a connection to forward data to.

        * direction -- The incoming data direction

        '''
        # Get the forwarding direction, and connection
        forwardDirection = self._forwardMap.get(direction)
        forwardConnection = self._connections.get(forwardDirection)

        return forwardConnection is not None

    def injectObject(self, direction, obj):
        '''Inject an object into the connection with the given direction.

        * direction -- The direction to inject the object
        * obj -- The object to inject

        '''
        connection = self._connections.get(direction)

        if connection is not None:
            connection.injectObjectToOutputStream(obj)

    def getConnection(self, direction):
        '''Get the connection for the specific direction.

        * direction -- The direction for the connection to retrieve

        '''
        return self._connections.get(direction)

    def getRefId(self, direction):
        '''Get the most recently used reference id for the connection with
        the given direction.

        * direction -- The direction for the connection

        '''
        connection = self._connections.get(direction)

        refId = None
        if connection is not None:
            refId = connection.getRefId()

        return refId

    def setRefId(self, refId, direction):
        '''Set the ref id for the forward connection.

        * refId -- The ref id
        * direction -- The data direction

        '''
        # Get the forwarding direction, and connection
        forwardDirection = self._forwardMap.get(direction)
        forwardConnection = self._connections.get(forwardDirection)

        if forwardConnection is not None:
            forwardConnection.setRefId(refId)

    def getForwardName(self, direction):
        '''Get the formatted name of the forward direction for the
        given direction.

        * direction -- The data direction

        '''
        forwardDirection = self._forwardMap.get(direction)
        return self.__getName(forwardDirection)

    def __getName(self, direction):
        '''Format the given direction into a string.

        * direction -- The direction to format

        '''
        return self._nameMap.get(direction, str(direction))
