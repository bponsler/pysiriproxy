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
'''The responses module contains classes associated with waiting for specific
types of responses from Siri.

'''
from types import GeneratorType


class Response:
    '''The Response class encapsulates the logic of waiting for a
    response from the Siri user. It keeps track of the speech rule generator
    function that should be called with the response, and sends the
    response to that function once a response is received.

    '''

    def __init__(self):
        '''Create the Response.'''
        self.manager = None
        self.__callback = None

    def setManager(self, manager):
        '''Set the manager object for this Response.

        * response -- The response

        '''
        self.manager = manager

    def setCallback(self, callback):
        '''Set the callback function for this response.

        * callback -- The callback function

        '''
        self.__callback = callback

    def wait(self):
        '''Wait for a response from the Siri user.'''
        keepYielding = True

        # Continue yielding until the callback function is no longer yielding
        while keepYielding:
            response = yield
            try:
                self.callback(response)
            except StopIteration:
                # The callback function is no longer yielding
                keepYielding = False

    def callback(self, response):
        '''Call the callback function with the given response.

        * response -- The Siri user's response

        '''
        if self.__callback is not None:
            self.__callback.send(response)


class ResponseList(Response):
    '''The ResponseList class manages the logic for commanding Siri to ask
    the user for a specific response. Once one of the expected responses is
    received, the callback function will be notified with the response. If
    an unexpected response is received, this class handles the logic of
    commanding Siri to say something to indicate that this was not a valid
    response, and then this class continues to wait for a valid response. This
    class also provides the ability to limit the number of attempts so that it
    does not continue waiting for a valid response forever.

    The callback function using the ResponseList will get notified with a value
    which will either be a string representing the user's valid response, or
    it will be None indicating that the maximum number of attempts was reached
    prior to receiving a valid response.

    '''

    def __init__(self, responses, question=None, unknown=None,
                 maxAttempts=None):
        '''
        * responses -- The list of accepted (case insensitive) responses
        * question -- The question Siri will ask the user
                      (None means nothing will be asked)
        * unknown -- What Siri will say when an unexpected response is received
                     (None means nothing will be said)
        * maxAttempts -- The maximum number of attempts before giving up
                         (None indicates an infinite number of tries)

        '''
        Response.__init__(self)
        self.__responses = responses
        self.__question = question
        self.__unknown = unknown
        self.__maxAttempts = maxAttempts

    def wait(self):
        '''Wait for the user to respond in a specific way.'''
        response = ""
        attempt = 0

        # Continue until we receive an expected response
        while response not in self.__responses:
            # Make sure we have attempts remaining
            if not self.__remainingAttempts(attempt):
                response = None
                break

            # Ask the user the given question
            self.__askQuestion()

            # Wait for the response
            response = yield
            response = response.lower()

            # Command Siri to notify the user of any unexpected responses
            if response not in self.__responses:
                self.__sayUnknown()

            # Keep track of the number of attempts
            attempt +=1

        self.callback(response)

    def __askQuestion(self):
        '''Ask the user the given question.'''
        if self.__question is not None:
            self.manager.ask(self.__question)

    def __sayUnknown(self):
        '''Handle commanding Siri to speak in the event of an
        unexpected response.

        '''
        if self.__unknown is not None:
            self.manager.say(self.__unknown)

    def __remainingAttempts(self, attempt):
        '''Determine if there are attempts remaining.

        * attempt -- The current attempt number

        '''
        return self.__maxAttempts is None or attempt < self.__maxAttempts


def _createResponse(manager, response):
    '''Create a response object from a generator response.

    * manager -- The PluginManager object
    * response -- The received response

    '''
    # The list of response objects we know how to convert
    typeList = [ResponseList]

    # Get the actual return of the generator
    try:
        actualResponse = response.next()
    except StopIteration:
        # No response was given
        actualResponse = None

    # Determine if the actual response is a known response object type
    isResponse = False
    for responseType in typeList:
        if isinstance(actualResponse, responseType):
            isResponse = True
            break

    # Create a basic response object to wrap the callback, if a response
    # object was not given
    if not isResponse:
        actualResponse = Response()

    # Initialize the response callback
    actualResponse.setManager(manager)
    actualResponse.setCallback(response)

    return actualResponse

def handleResponse(manager, response):
    '''Handle the given response.

    * manager -- The PluginManager object
    * response -- The received response

    '''
    actualResponse = None

    # Handle any responses that are generators
    if type(response) == GeneratorType:
        # Create a response object from the generator
        responseObj = _createResponse(manager, response)

        # Tell the response method to start waiting, and initialize it by
        # calling next
        actualResponse = responseObj.wait()
        actualResponse.next()

    return actualResponse
