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
'''The server module contains the necessary classes for creating a
concrete connection which is responsible for managing the connection between
pysiriproxy and Apple's web server.

'''
from os.path import join

from OpenSSL import SSL
from twisted.internet import protocol, reactor, ssl

from pysiriproxy.constants import Directions
from pysiriproxy.options.options import Options
from pysiriproxy.options.config import Ids, Sections
from pysiriproxy.connections.connection import Connection
from pysiriproxy.connections.manager import ConnectionManager

from pyamp.logging import Colors


class _Server(Connection):
    '''The _Server class manages a connection to the Apple server which
    proceses Siri requests and responds accordingly.

    '''

    def __init__(self, logger):
        '''
        * logger -- The logger

        '''
        # Grab the hostname of the Apple server to which we will be connecting
        # and use it as the name of this connection for debugging purposes
        hostname = Options.get(Sections.Server, Ids.Host)

        # Remove the '.apple.com' extension from the hostname, and also
        # capitalize it for better appearance
        hostname = hostname.replace(".apple.com", "")
        hostname = hostname.capitalize()

        Connection.__init__(self, hostname, Directions.From_Server,
                            logger=logger, logColor=Colors.Foreground.Blue)

    def connectionMade(self):
        '''Called when the connection has been made successfully.'''
        self.log.debug("Connection made.", level=2)
        self.ssled = True

        # Create the empty TLS context, and enable TLS mode
        ctx = ClientTLSContext()
        self.transport.startTLS(ctx, self.factory)
        
    def receiveObject(self, obj):
        '''Called when an object has been received.

        * obj -- The received object

        '''
        return obj


class ClientTLSContext(ssl.ClientContextFactory):
    '''The ClientTLSContext class creates a concrete factory class responsible
    for creating a client connection.

    '''
    isClient = 1
    '''Indicate that this is a client connection.'''

    def getContext(self):
        '''Get the context for this client connection.'''
        return SSL.Context(SSL.TLSv1_METHOD)


class _Factory(protocol.ClientFactory):
    '''The _Factory class is responsible for creating a _Server
    connection.

    '''
    # Define the name and log color used for logging messages for this class
    name = "ServerFactory"
    logColor = Colors.Foreground.Blue

    def __init__(self, logger=None):
        '''
        * logger -- The logger

        '''
        # Get an instance to the connection manager so we can properly
        # disconnect Apple's server connection when it is lost
        self.__connectionManager = ConnectionManager(logger)

        # If no logger is given, be sure to create it
        if logger is None:
            logger = LogData(self.name, color=self.logColor)

        self.log = logger.get(self.name)
        self.__logger = logger

    def buildProtocol(self, _addr):
        '''Build the protocol for the _Server connection.

        * _addr -- The address

        '''
        server = _Server(self.__logger)
        server.factory = self

        return server

    def clientConnectionFailed(self, connector, reason):
        self.log.debug("Connection failed: %s" % reason, level=2)
        protocol.ClientFactory.clientConnectionFailed(self, connector,
                                                      reason)

        # Delete the server connection
        self.__connectionManager.disconnect(Directions.From_Server)

    def clientConnectionLost(self, connector, reason):
        self.log.debug("Connection lost: %s" % reason, level=2)
        protocol.ClientFactory.clientConnectionLost(self, connector,
                                                    reason)

        # Delete the server connection
        self.__connectionManager.disconnect(Directions.From_Server)


def connect(logger):
    '''Connect the Siri server to handle server data.

    * logger -- The logger

    '''
    host = Options.get(Sections.Server, Ids.Host)
    port = Options.get(Sections.Server, Ids.Port)

    return reactor.connectTCP(host, port, _Factory(logger))
