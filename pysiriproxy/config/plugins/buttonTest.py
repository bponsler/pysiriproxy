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
'''The buttonTest module contains the definition of a plugin which
demonstrates how to create a plugin which displays buttons to the user.

This plugin demonstrates creating buttons that execute custom commands, and
how to configure a plugin to respond to the custom command.

This plugin also demonstrates how to create buttons to perform web searches
for specific text.

'''
from pysiriproxy.plugins import BasePlugin, matches, regex
from pysiriproxy.objects import ObjectFactory, Buttons


class Plugin(BasePlugin):
    '''The ButtonTest plugin.

    This plugin demonstrates how to create and use buttons with Siri. It
    demonstrates using buttons that execute custom commands which can be
    handled by a plugin, or how to create buttons that perform web searches
    for specific text.

    '''
    name = "ButtonTest"

    # Define a dictionary mapping custom command names, to the plugin
    # function names that are called when the command is executed
    customCommandMap = {
        "Command 1": "_callbackOne",
        "Command 2": "_callbackTwo",
        "Command 3": "_callbackThree"
        }

    def init(self):
        '''This function is called once when the Plugin is created.'''
        # Create a list of tuples pairing the button text to the
        # commands that are executed when the button is pressed
        self.__buttonList = [
            ("Button 1", "Command 1"),
            ("Button 2", "Command 2"),
            ("Button 3", "Command 3")
            ]

    ##### Define the speech rules for this plugin #####

    @matches("Test custom buttons")
    def testButtons(self, text):
        '''This is an example of a speech rule which triggers when
        the user says "Test custom buttons".

        This example demonstrates how to display buttons to the user
        which execute custom commands when the button is pressed. This
        plugin is able to respond to the custom commands.

        * text -- The text spoken by the user

        '''
        # Create the custom command buttons
        buttons = self.__createCustomButtons()

        # Create an utterance to go along with the buttons
        utterance = ObjectFactory.utterance("Please press a button")

        # Now create a view which displays the utterance and the buttons
        self.makeView([utterance] + buttons)

        self.completeRequest()

    @regex("(Create|Make) a Button")
    def buttonTest(self, text):
        '''This is an example of a speech rule which triggers when
        the user says "Create a button" or "Make a button".

        This example demonstrates how to display buttons to the user
        which allow the user to perform a web search for specific text.

        * text -- The text spoken by the user

        '''
        # Create the two web search buttons to display to the user
        button1 = ObjectFactory.button(Buttons.WebSearch,"Search for Siri",
                                       "siri")
        button2 = ObjectFactory.button(Buttons.WebSearch, "Search for Python",
                                       "python")

        # Create an utterance to go along with the buttons
        utterance = ObjectFactory.utterance("Look! I made buttons",
                                            "Aren't they cool?")

        # Create a view to display the utterance and the buttons
        self.makeView([utterance, button1, button2])
        self.completeRequest()

    ##### Custom command callback functions #####

    def _callbackOne(self, _obj):
        '''Called when the 'Command 1' command is executed.

        * obj -- The object that contained the custom command

        '''
        self.say("You pressed the first button!")
        self.completeRequest()

    def _callbackTwo(self, _obj):
        '''Called when the 'Command 2' command is executed.

        * obj -- The object that contained the custom command

        '''
        self.say("You pressed the second button!")
        self.completeRequest()

    def _callbackThree(self, _obj):
        '''Called when the 'Command 3' command is executed.

        * obj -- The object that contained the custom command

        '''
        self.say("You pressed the third button!")
        self.completeRequest()

    ##### Private functions #####

    def __createCustomButtons(self):
        '''Create a list of buttons that perform custom commands.'''
        buttons = []

        # Create buttons to execute custom commands for each of the
        # buttons in the list of buttons
        for buttonText, command in self.__buttonList:
            button = ObjectFactory.button(Buttons.Custom, buttonText,
                                          command)
            buttons.append(button)

        return buttons
