# Copyright (C) (c) 2012 Brett Ponsler, Pete Lamonica, Pete Lamonica
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
'''Contains the Player class.'''
from pysiriproxy.utils import toHex
from pysiriproxy.constants import Modes

from pyamp.processes.threading import Thread


class Player(Thread):
    '''The Player class loads a file containing data which it proceeds
    to send to the given protocol class using the same interface used
    to handle connections to the server. This allows us to save incoming
    data to the server and replay it for testing purposes.

    '''

    def __init__(self, protocol, filename, logger):
        '''
        * protocol -- The server protocol class
        * filename -- The filename containing to data to replay
        * logger -- The logger

        '''
        Thread.__init__(self)
        self.__log = logger.get("PacketPlayer")
        self.__protocol = protocol(logger=logger)

        self.__content = file(filename).read()
        self.__lines = self.__content.split("-END_OF_DATA-")
        self.__index = 0

        # Start in Line mode
        self.__setMode(Modes.Line)

        # Map the fuction to call based on the current mode
        self.__modeMap = {Modes.Line: self.__sendLineData,
                          Modes.Raw: self.__sendRawData}

    def onCycle(self, i):
        '''Called during each cycle of the thread.'''
        if self.__index >= len(self.__lines):
            self.shutdown()
            return

        # The first cycle corresponds to a created connection
        if i == 1:
            self.__protocol.connectionMade()

        # Only send data once per second
        if i % 10 == 0:
            # Call the data sending function for the current mode
            modeFn = self.__modeMap.get(self.__protocol.getMode())
            if modeFn is not None:
                modeFn()

    def onShutdown(self):
        '''Called in the event that the thread is shutdown.'''
        self.__protocol.connectionLost("Player thread shutdown")

    def onException(self, e, traceback):
        '''An exception occurred.

        * e -- The exception
        * traceback -- The traceback

        '''
        self.__log.error("Traceback:", traceback)
        self.shutdown()

    ##### Private functions #####

    def __sendLineData(self):
        '''Send a line of data to the server.'''
        data = self.__lines[self.__index]
        self.__protocol.lineReceived(data)
        self.__index += 1

    def __sendRawData(self):
        '''Send raw data to the server.'''
        # True to send all remaining data, else to send parts
        _SEND_ALL = False

        # The two ways of choosing data to send
        if _SEND_ALL:
            # Send all remaining data at once
            lines = self.__lines[self.__index:]
            self.__index = len(self.__lines)
            data = '\n'.join(lines)
        else:
            # Send parts of the remaining data
            lines = self.__lines[self.__index]
            self.__index += 1
            data = lines

        self.__protocol.rawDataReceived(data)

    def __setMode(self, mode):
        '''Set the data sending mode.

        * mode -- The mode

        '''
        self.__mode = mode
