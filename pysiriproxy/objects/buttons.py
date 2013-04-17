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
'''The buttons module contains classes pertaining to creating objects which
can be sent to the iPhone or Apple's web server which pertain to creating
buttons on the iPhone.

'''
from pysiriproxy.objects.actions import Actions
from pysiriproxy.objects.baseObject import SiriObject


class _Button(SiriObject):
    '''The _Button class encapsulates the base functionality for creating a
    button on the iPhone Siri view.

    '''
    def __init__(self, buttonText, commands=None):
        '''
        * buttonText -- The text displayed on the button
        * commands -- The commands executed by the button when it is pressed

        '''
        SiriObject.__init__(self, "Button", "com.apple.ace.assistant")
        self.text = buttonText
        self.commands = [] if commands is None else commands


class _Custom(_Button):
    '''The _Custom class creates a button that has the iPhone send a
    custom command to the event that it is pressed.

    '''
    def __init__(self, buttonText, command):
        '''
        * buttonText -- The text displayed on the button
        * command -- The command that is executed when the button is pressed

        '''
        action = Actions.create(Actions.CustomCommand, command)
        _Button.__init__(self, buttonText, [action])


class _WebSearchButton(_Button):
    '''The _WebSearchButton creates a button on the iPhone Siri view which will
    perform a web search for a specific query in the event that the button is
    pressed.

    '''
    def __init__(self, buttonText, query):
        '''
        * buttonText -- The text displayed on the button
        * query -- The search query to perform

        '''
        action = Actions.create(Actions.WebSearch, query)
        _Button.__init__(self, buttonText, [action])


class Buttons:
    '''The Buttons class contains the various types of Buttons as well as
    a function for creating Buttons of a specific type.

    This class provides a factory function for creating Buttons of a specific
    type.

    '''
    Custom = "Custom"
    '''A button that executes a custom command when it is pressed.'''

    WebSearch = "WebSearch"
    '''A button that performs a web search for a specific query when it is
    pressed.

    '''

    __TypeMap = {
        Custom: _Custom,
        WebSearch: _WebSearchButton
        }

    @classmethod
    def create(cls, buttonType, buttonText, *args, **kwargs):
        '''Create a Button of the given type.

        * buttonType -- The type of Button to create
        * buttonText -- The text displayed on the button
        * args -- The arguments
        * kwargs -- The keyword arguments

        '''
        button = None

        # Create the button object if it is found
        buttonClass = Buttons.__TypeMap.get(buttonType)
        if buttonClass is not None:
            button = buttonClass(buttonText, *args, **kwargs)

        return button
