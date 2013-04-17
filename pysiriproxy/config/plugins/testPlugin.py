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
'''The testPlugin module contains the definition of the Test-Plugin.

This plugin gives examples of controlling Siri's responses to the user
in various ways, such as: responding with text, asking a question, and
waiting for the user to give a specific answer.

'''
from pysiriproxy.objects import Buttons, ObjectFactory
from pysiriproxy.plugins import BasePlugin, From_Server, From_iPhone, \
    SpeechPacket, StartRequest, matches, regex, ResponseList

from pyamp.logging import Colors


class Plugin(BasePlugin):
    '''This plugin contains examples of creating object filters, and
    speech rules in order to control Siri's responses to the user.

    '''
    # Define the name and log color for this plugin
    name = "Test-Plugin"
    logColor = Colors.Foreground.Cyan

    ##### Define all of the filters for this plugin. #####

    @From_Server
    def filterServer(self, obj, direction):
        '''Example of a directional filter for objects from Apple's
        web server.
        
        * obj -- The received object
        * direction -- The direction of the received data

        '''
        return obj

    @SpeechPacket
    def filterSpeech(self, obj, direction):
        '''Example of a class filter for a speech packet.
        
        * obj -- The received object
        * direction -- The direction of the received data

        '''
        return obj

    ##### Define all of the speech rules for this plugin. #####

    @matches("Test Siri Proxy")
    def testMatch(self, text):
        '''This is an example of a speech rule which triggers when
        the user says "Test Siri Proxy"

        * text -- The text spoken by the user

        '''
        self.say("Testing pure string matching")

        self.completeRequest()

    @regex(".*Regular test.*")
    def testRegex(self, text):
        '''This is an example of a speech rule which triggers when
        the user says a phrase containing "Regular test".

        * text -- The text spoken by the user

        '''
        self.say("Testing a regular expression")

        self.completeRequest()

    @matches("Ask me a question")
    def testAsk(self, text):
        '''This is an example of a speech rule which triggers when
        the user says "Ask me a question".

        This example demonstrates how to command Siri to ask the
        user a specific question, and then to perform some action
        using the user's response.

        * text -- The text spoken by the user

        '''
        # Ask the question and wait for the response
        self.ask("What question do you want me to ask?")
        response = yield

        self.ask("%s?" % response)
        response = yield

        # Example of having Siri display one thing, and say another
        self.say("You answered: %s" % response, spoken="Thanks for answering.")

        self.completeRequest()

    @regex(".*Confirmation.*")
    def confirmTest(self, text):
        '''This is an example of a speech rule which triggers when
        the user says a phrase containing "Confirmation".

        This example demonstrates how to command Siri to use a ResponseList
        to wait for the user to say a specific response.

        * text -- The text spoken by the user

        '''
        responses = ["yes", "no"]
        question = "Please confirm..."
        unknown = "Excuse me?"

        # Wait for a valid response to be spoken
        response = yield ResponseList(responses, question, unknown)

        self.say("You said %s" % response)
        self.completeRequest()
