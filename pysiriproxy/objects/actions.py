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
'''The actions module contains classes pertaining to creating objects which
can be sent to the iPhone or Apple's web server which pertain to specific
actions.

'''
from pysiriproxy.objects.commands import Commands
from pysiriproxy.objects.baseObject import SiriObject


class _CustomCommand(SiriObject):
    '''The _CustomCommand class creates a StartRequest object which contains a
    custom command.

    '''

    def __init__(self, command):
        '''
        * command -- The text command to issue

        '''
        SiriObject.__init__(self, "StartRequest", "com.apple.ace.system")
        self.utterance = self.__createCommand(command)
        self.handsFree = False

    def __createCommand(self, command):
        '''Create the command string.

        * command -- The command to execute

        '''
        return "%s" % command


class _WebSearch(SiriObject):
    '''The _WebSearch class creates a command to perform a web search
    for a particular search phrase.

    '''

    def __init__(self, query):
        '''
        * query -- The text to query on the web

        '''
        SiriObject.__init__(self, "StartRequest", "com.apple.ace.system")
        self.utterance = self.__createQuery(query)
        self.handsFree = False

    def __createQuery(self, query):
        '''Create the query string for the web search.

        * query -- The query

        '''
        before = "^webSearchQuery^=^"
        after = "^^webSearchConfirmation^=^Yes^"
        return "%s%s%s" % (before, query, after)


class Actions:
    '''The Actions class contains a list of Action types as well as a
    function for creating specific types of Actions.

    This class provides a factory function for creating Actions of a specific
    type.

    '''
    CustomCommand = "CustomCommand"
    '''The CustomCommand action type.'''

    WebSearch = "WebSearch"
    '''The WebSearch action type.'''

    # Create a dictionary mapping the types to their respective objects
    __TypeMap = {
        CustomCommand: _CustomCommand,
        WebSearch: _WebSearch
        }

    @classmethod
    def create(cls, actionType, *args, **kwargs):
        '''Return a specific Action wrapped in a SendCommands object so
        it can be sent to Siri as a command.

        * actionType -- The type of Action to create
        * args -- The arguments
        * kwargs -- The keyword arguments

        '''
        sendCommand = None

        # Create the action object if it is found
        actionClass = Actions.__TypeMap.get(actionType)
        if actionClass is not None:
            action = actionClass(*args, **kwargs)
            sendCommand = Commands.create(Commands.SendCommands, [action])

        return sendCommand
