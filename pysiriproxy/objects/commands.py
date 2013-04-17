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
'''The commands module contains classes pertaining to creating objects which
can be sent to the iPhone or Apple's web server which pertain to creating
commands which are sent from the iPhone to Apple's web server.

'''
from pysiriproxy.objects.baseObject import SiriObject


class _SendCommands(SiriObject):
    '''The _SendCommands class creates an object that is able to send a series
    of commands from the iPhone to Apple's web server which are to be executed.

    '''

    def __init__(self, commands=None):
        '''
        * commands -- The list of commands to execute

        '''
        SiriObject.__init__(self, "SendCommands", "com.apple.ace.system")
        self.commands = [] if commands is None else commands


class _ConfirmationOptions(SiriObject):
    '''The _ConfirmationOptions class provides the ability to create a
    dialog that presents the user with confirmation options such as:
    submit, and cancel buttons that each perform different actions.

    '''

    def __init__(self, submitCmds=None, cancelCmds=None, denyCmds=None,
                 confirmCmds=None, denyText="Cancel", cancelLabel="Cancel",
                 submitLabel="Send", confirmText="Send", cancelTrigger="Deny"):
        '''
        * submitCmds -- The list of commands that are executed when the submit
                        button is pressed
        * cancelCmds -- The list of commands that are executed when the cancel
                        button is pressed
        * denyCms -- The list of commands that are executed when the deny
                     button is pressed
        * confirmCmds -- The list of commands that are executed when the confirm
                         button is pressed
        * denyText -- The text that is displayed on the deny button
        * cancelLabel -- The text that is displayed on the cancel button
        * submitLabel -- The text that is displayed on the submit button
        * confirmText -- The text that is displayed on the confirm button
        * cancelTrigger -- The trigger that performs the cancel action

        '''
        SiriObject.__init__(self, "ConfirmationOptions",
                            "com.apple.ace.assistant")

        self.submitCommands = [] if submitCmds is None else submitCmds
        self.cancelCommands = [] if cancelCmds is None else cancelCmds
        self.denyCommands = [] if denyCmds is None else denyCmds
        self.confirmCommands = [] if confirmCmds is None else confirmCmds

        self.denyText = denyText 
        self.cancelLabel = cancelLabel 
        self.submitLabel = submitLabel 
        self.confirmText = confirmText 
        self.cancelTrigger = cancelTrigger 


class _ConfirmSnippetCommand(SiriObject):
    '''The _ConfirmSnippetCommand class creates a confirmation command.'''

    def __init__(self, requestId=""):
        '''
        * request_id -- The request id for this object

        '''
        SiriObject.__init__(self, "ConfirmSnippet", "com.apple.ace.assistant")
        self.request_id = requestId


class _CancelSnippetCommand(SiriObject):
    '''The _CancelSnippetCommand class creates a cancel command.'''

    def __init__(self, requestId=""):
        '''
        * request_id -- The request id for this object

        '''
        SiriObject.__init__(self, "CancelSnippet", "com.apple.ace.assistant")
        self.request_id = requestId


class _CancelRequest(SiriObject):
    '''The _CancelRequest class creates an object to cancel the current
    request.

    '''

    def __init__(self, requestId):
        '''
        * request_id -- The request id for this object

        '''
        SiriObject.__init__(self, "CancelRequest", "com.apple.ace.system")

        self.request_id = refId


class _ResultCallback(SiriObject):
    '''The _ResultCallback class creates a result callback Siri object.'''

    def __init__(self, commands, code=0):
        '''
        * commands -- The commands for the result callback
        * code -- The code for the callback

        '''
        SiriObject.__init__(self, "ResultCallback", "com.apple.ace.system")
        self.commands = [] if commands is None else commands
        self.code = code


class Commands:
    '''The Commands class contains the various types of Commands as well
    as a function for creating Commands of a specific type.

    This class provides a factory method for creating Commands of a specific
    type.

    '''
    CancelSnippet = "CancelSnippet"
    '''The CancelSnippet command type.'''

    CancelRequest = "CancelRequest"
    '''The CancelRequest command type.'''

    ConfirmationOptions = "ConfirmationOptions"
    '''The ConfirmationOptions command type.'''

    ConfirmSnippet = "ConfirmSnippet"
    '''The ConfirmSnippet command type.'''

    SendCommands = "SendCommands"
    '''The SendCommands command type.'''

    ResultCallback = "ResultCallback"
    '''The ResultCallback command type.'''

    # Create a dictionary mapping the types to their respective objects
    __TypeMap = {
        CancelSnippet: _CancelSnippetCommand,
        CancelRequest: _CancelRequest,
        ConfirmationOptions: _ConfirmationOptions,
        ConfirmSnippet: _ConfirmSnippetCommand,
        SendCommands: _SendCommands,
        ResultCallback: _ResultCallback
        }

    @classmethod
    def create(cls, commandType, *args, **kwargs):
        '''Create a Command of the specific type.

        * commandType -- The type of Command to create
        * args -- The arguments
        * kwargs -- THe keyword arguments

        '''
        command = None

        # Create the command object if it is found
        commandClass = Commands.__TypeMap.get(commandType)
        if commandClass is not None:
            command = commandClass(*args, **kwargs)

        return command
