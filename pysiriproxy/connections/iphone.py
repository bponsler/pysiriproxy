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
'''The iphone module contains the necessary classes for creating a concrete
connection which is responsible for managing the connection between
pysiriproxy and the iPhone.

'''
from time import sleep
from os.path import join
from os import getpid, system

from twisted.internet import reactor, protocol, ssl
from twisted.internet.ssl import DefaultOpenSSLContextFactory

from pysiriproxy.connections import server
from pysiriproxy.constants import Directions
from pysiriproxy.options.options import Options
from pysiriproxy.options.config import Ids, Sections
from pysiriproxy.connections.connection import Connection

from pyamp.logging import Colors, LogLevel


class _iPhone(Connection):
    '''The _iPhone class manages the SSL connection to Siri on the iPhone
    client. It processes requests from Siri and forwards them to Apple's
    server, and then intercepts the response and provides the ability to
    inject custom responses.

    '''

    def __init__(self, logger):
        '''
        * logger -- The logger

        '''
        self.__serverConnection = None
        self.__logger = logger
        Connection.__init__(self, "iPhone", Directions.From_iPhone,
                            logger=logger, logColor=Colors.Foreground.Purple)

    def connectionMade(self):
        '''Called when a connection is made.'''
        self.log.info("Connection made.")
        Connection.connectionMade(self)
        self.ssled = True

        # Initialize the connection to Apple's server
        self.reconnectServer()

    def reconnectServer(self):
        '''Disconnect and then re-connect the server connection.'''
        self.__disconnectServer()
        self.__serverConnection = server.connect(self.__logger)

    def connectionLost(self, reason):
        '''Called when the connection is lost.

        * reason -- The reason the connection was lost

        '''
        self.log.info("Connection lost: %s" % reason)
        self.__disconnectServer()

        # Signal the connection manager that the iPhone connection
        # has been closed
        connectionManager = self.getConnectionManager()
        connectionManager.disconnect(Directions.From_iPhone)

        # Determine if the server should exit due to the lost connection
        if Options.get(Sections.Debug, Ids.ExitOnConnectionLost):
            serverPid = getpid()
            self.log.info("Forcing server [%d] to exit!!!" % serverPid)
            system("kill -9 %d" % serverPid)

    def __disconnectServer(self):
        '''Disconnect the server connection if there is one.'''
        # Disconnect the server connection if we lost a connection
        # to the iPhone
        if self.__serverConnection is not None:
            self.log.info("Closing server connection.")
            self.__serverConnection.disconnect()

            # Signal the connection manager that the server connection
            # has been closed
            connectionManager = self.getConnectionManager()
            connectionManager.disconnect(Directions.From_Server)

            del self.__serverConnection
            self.__serverConnection = None


class _Factory(protocol.Factory):
    '''The _Factory class is responsible for creating an _iPhone connection.'''

    def __init__(self, logger):
        '''
        * logger -- The logger

        '''
        self.__logger = logger

    def buildProtocol(self, addr):
        '''build the protocol for an _iPhone connection.

        * _addr -- The address

        '''
        return _iPhone(self.__logger)


def connect(logger):
    '''Connect the Siri server to handle iPhone requests.

    * logger -- The logger

    '''
    # Grab the configured port for the iPhone
    port = Options.get(Sections.iPhone, Ids.Port)

    # Create the SSL context using the iPhone key and certificate files
    keyFile = Options.get(Sections.iPhone, Ids.KeyFile)
    certFile = Options.get(Sections.iPhone, Ids.CertFile)
    authentication = DefaultOpenSSLContextFactory(keyFile, certFile)

    # Create the SSL server using the given authentication files
    reactor.listenSSL(port, _Factory(logger), authentication)
