# Copyright 2012 Brett Ponsler
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
'''Contains the Reset-Plugin.'''
from pysiriproxy.plugins.plugin import BasePlugin
from pysiriproxy.plugins.objectClasses import ClearContext, \
    StartSpeechRequest, CancelRequest, CancelSpeech, CommandFailed

from pyamp.logging import Colors


class Plugin(BasePlugin):
    '''Handles resetting the context.'''

    # Define the name and log color for this plugin
    name = "Reset-Plugin"
    logColor = Colors.Foreground.Green

    ##### Define all of the filters for this plugin. #####

    @CancelRequest
    @CancelSpeech
    @ClearContext
    @CommandFailed
    def resetFilter(self, obj, direction):
        '''Reset the context when a request is completed, or the context is
        cleared.

        * obj -- The received object
        * direction -- The direction of the received data

        '''
        self.log.debug("Resetting object manager: %s" % obj.get("class", None),
                       level=0)
        self.resetContext()
        return obj
