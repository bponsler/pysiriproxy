#!/usr/bin/python2.6
# -*-python-*-
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
'''The pluginTester module contains a class that provides the ability
to test the object filters and speech rules.

'''
from sys import argv, stdout

from pysiriproxy.options.config import Files
from pysiriproxy.options.options import Options
from pysiriproxy.plugins.manager import PluginManager
from pysiriproxy.testing.testSupport import iPhone, Server
from pysiriproxy.connections.manager import ConnectionManager

from pyamp.logging import LogData, LogLevel, Colors


class PluginTester:
    '''The PluginTester class provides the ability to test the configured
    plugins for pysiriproxy. The intent is for this class to be subclassed
    to preform desired tests. This class provides several callback functions
    which can be overridden by the concrete PluginTester subclasses for
    specific purposes. These functions are described below:

      * :func:`iPhoneCallback` -- This function is called in the event that
        data is being sent from the iPhone connection to the Server connection,
        where **obj** is the specific data being transmitted.

      * :func:`serverCallback` -- This function is called in the event that
        data is being sent from the Server connection to the iPhone connection,
        where **obj** is the specific data being transmitted.

    '''

    def __init__(self, logData=None, logColor=Colors.Foreground.Green):
        '''
        * logData -- The LogData object
        * logColor -- The color to use for the Logger

        '''
        # Create a logger just for the options loading
        if logData is None:
            logData = LogData()
        self.__log = logData.get("PluginTester", color=logColor)

        # Parse the siri proxy configuration options object
        options = Options(logData)
        options.parse(argv, Files.ConfigFile)

        # Set the callback for the iPhone, and Server connections
        Server.Callback = self.iPhoneCallback
        Server.Callback = self.serverCallback

        # Create the connection manager, and connect the iPhone and
        # Server connections to it
        connectionManager = ConnectionManager(logData)
        connectionManager.connect(iPhone)
        connectionManager.connect(Server)

        # Grab an instance to the plugin manager
        self.__pluginManager = PluginManager(connectionManager, logData)

    def testFilters(self, obj, direction):
        '''Test the object filters for all of the configured Plugins to
        determine if any respond to the given object for the given direction.
        This function returns None if no filters were applied to this object,
        it returns False if this object was dropped, or it returns the object
        modified by the object filters.

        * obj -- The object used to test filters
        * direction -- The direction the object was received (either from
                       the iPhone or from the Server)

        '''
        self.__log.debug("Testing filters: [%s], [%s]" % (direction, obj), 2)
        return self.__pluginManager.processFilters(obj, direction)

    def testSpeech(self, speech):
        '''Test the speech rules for all of the configured Plugins to determine
        if any respond to the given speech text. This function returns True if
        any Plugins had speech rules that matched the given text, otherwise it
        returns False.

        * speech -- The simulated text that was "spoken" by the user

        '''
        self.__log.debug("Testing speech: [%s]" % speech, 2)
        return self.__pluginManager.processSpeechRules(speech)

    ##### Callback methods #####

    def iPhoneCallback(self, cls, obj):
        '''The function called in the event that an object is received from
        the iPhone.

        * obj -- The object that was received

        '''
        self.__log.info(obj)

    def serverCallback(self, cls, obj):
        '''The function called in the event that an object is received from
        the Server server.

        * obj -- The object that was received

        '''
        self.__log.info(obj)


if __name__ == '__main__':
    args = argv[1:]
    if len(args) == 0:
        print "Syntax: %s [the text to test as speech]"
        exit(1)

    tester = PluginTester()
    tester.testSpeech(' '.join(argv[1:]))
