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
'''The manager module contains the PluginManager class which encapsulates
the functionality of loading and managing a series of plugins. The
PluginManager is also responsible for processing the speech rules and object
filters for all the loaded plugins.

'''
from sys import path
from os import listdir
from os.path import join, split, splitext

from pysiriproxy.objects import ResponseFactory
from pysiriproxy.options import Options, Ids, Sections
from pysiriproxy.plugins import BasePlugin, handleResponse
from pysiriproxy.constants import Directions, DirectionTypes

from pyamp.logging import LogData
from pyamp.util import getStackTrace


class PluginManager:
    '''The PluginManager is responsible for loading all of the available
    plugins as well as processing the object filters and speech rules for
    each of the loaded plugins.

    '''
    # Implement the borg pattern
    __shared_state = {}

    # The class name that all plugins must have
    PluginClassName = "Plugin"

    def __init__(self, connectionManager, logger=None):
        '''
        * connectionManager -- An instance of the ConnectionManager
        * logger -- The LogData object

        '''
        self.__dict__ = self.__shared_state

        # If plugins have not been loaded, then load them
        if getattr(self, "_plugins", False) == False:
            self._connectionManager = connectionManager

            # Get data pertaining to the directory containing plugins
            self.PluginsDirectory = Options.get(Sections.General,
                                                Ids.PluginsDir)
            self.PluginsDirectoryName = split(self.PluginsDirectory)[-1]

            # Create a logger if one was not given
            if logger is None:
                logger = LogData()
            self.log = logger.get("PluginManager")
            self._logger = logger

            self._pluginMap = {}

            self._options = Options()
            self.loadPlugins(self.PluginsDirectory)

            # The Response object waiting for a response from Siri
            self._response = None

    ##### Interacting with Siri #####

    def showDirections(self, directionsType, source, destination,
                       utterance=None):
        '''Show the given type of directions between the two locations to the
        user.

        * directionsType -- The type of directions
        * source -- The source location
        * destination -- The destination location
        * utterance -- The utterance to speak

        '''
        server = Directions.From_Server
        connection = self._connectionManager.getConnection(server)

        if connection is not None:
            self.log.debug("Making directions [%s]" % directionsType, level=3)
            refId = connection.getRefId()

            directions = ResponseFactory.directions(refId, directionsType,
                                                    source, destination,
                                                    utterance=utterance)
            connection.injectObjectToOutputStream(directions)

    def showDrivingDirections(self, source, destination, utterance=None):
        '''Show driving directions between the two locations to the user.

        * source -- The source location
        * destination -- The destination location
        * utterance -- The utterance to speak

        '''
        self.showDirections(DirectionTypes.Driving, source, destination,
                            utterance=utterance)

    def showWalkingDirections(self, source, destination, utterance=None):
        '''Show walking directions between the two locations to the user.

        * source -- The source location
        * destination -- The destination location
        * utterance -- The utterance to speak

        '''
        self.showDirections(DirectionTypes.Walking, source, destination,
                            utterance=utterance)

    def showPublicTransitDirections(self, source, destination, utterance=None):
        '''Show public transportation directions between the two locations to
        the user.

        * source -- The source location
        * destination -- The destination location
        * utterance -- The utterance to speak

        '''
        self.showDirections(DirectionTypes.PublicTransit, source, destination,
                            utterance=utterance)

    def makeView(self, views):
        '''Create a view and send it to the iPhone.

        * views -- The list of views to create

        '''
        server = Directions.From_Server
        connection = self._connectionManager.getConnection(server)
        if connection is not None:
            self.log.debug("Making view", level=3)
            refId = connection.getRefId()

            view = ResponseFactory.view(refId, views)
            connection.injectObjectToOutputStream(view)

    def ask(self, question, spoken=None):
        '''Command Siri to ask the user a question.

        * question -- The question to ask
        * spoken -- The text Siri will say

        '''
        self.say(question, spoken, prompt=True)

        # Complete the request, otherwise Siri will freeze,
        # but be sure not to reset the context
        self.completeRequest(resetContext=False)

    def completeRequest(self, refId=None, resetContext=True):
        '''Complete a request to Siri.

        * refId -- The reference ID

        '''
        server = Directions.From_Server
        connection = self._connectionManager.getConnection(server)
        if connection is not None:
            self.log.debug("Sending Request Completed", level=3)

            refId = connection.getRefId() if refId is None else refId
            completed = ResponseFactory.requestCompleted(refId)
            connection.injectObjectToOutputStream(completed)

            # Reset the connection context
            if resetContext:
                self._connectionManager.resetConnections()

    def resetContext(self):
        '''Reset the context.'''
        self._connectionManager.resetConnections()

        # Clear the current plugin that is waiting for a response
        if self._response is not None:
            self._response.close()
            self._response = None

    def say(self, text, spoken=None, prompt=False, refId=None):
        '''Command Siri to speak a piece of text.

        * text -- The text that Siri will display
        * spoken -- The text that Siri will speak
        * prompt -- True to have Siri prompt for a response

        '''
        server = Directions.From_Server
        connection = self._connectionManager.getConnection(server)

        if connection is not None:
            self.log.debug("Saying:", level=3, text=text, spoken=spoken,
                           prompt=prompt)

            refId = connection.getRefId() if refId is None else refId

            # Create the utterance
            utterance = ResponseFactory.utterance(refId, text,
                                                  spoken, prompt)
            connection.injectObjectToOutputStream(utterance)

    ##### Plugin processing functions #####

    def processFilters(self, obj, direction):
        '''Process all the plugin filters for this object and data direction.

        * obj -- The object
        * direction -- The data direction

        '''
        response = None
        try:
            response = self.__processFilters(obj, direction)
        except:
            self.log.error("Failed processing filters")
            self.log.error(getStackTrace())

        # Determine if the response should be used
        if response is not None:
            # If the response is False, then the object should be dropped
            # If the object has the same class as the original object, then
            # it should be returning
            if response == False:
                obj = None
            elif response.get('class') == obj.get('class'):
                obj = response

        return obj

    def processSpeechRules(self, text):
        '''Process all the plugin speech rules for this recognized text.

        * text -- The recognized text

        '''
        try:
            # Speech rules return True to indicate that the response from
            # Apple's server should be overriden. The speech rules return
            # False to indicate that the response from Apple's server should
            # be used.
            return self.__processSpeechRules(text)
        except:
            self.log.error("Failed processing speech rules")
            self.log.error(getStackTrace())

            # Have Siri respond with the the error response
            self.say(self._options.get(Sections.Responses, Ids.ErrorResponse))
            self.completeRequest()
            return True

    def loadPlugins(self, directory):
        '''Load all of the plugins from the plugins directory.

        * directory -- The plugins directory

        '''
        self.__addPluginsToPath(directory)

        # Traverse through all of the plugins
        for filename in listdir(directory):
            if not filename.startswith("__") and filename.endswith(".py"):
                # Get the module name from the filename by removing the
                # file extension
                pluginName = splitext(filename)[0]

                try:
                    self.log.debug("Loading plugin [%s]" % pluginName,
                                   level=10)

                    # Get the plugin class, and create the plugin object
                    pluginClass = self.__importPlugin(pluginName)
                    plugin = pluginClass(self, self._logger)

                    # Ensure that all plugins subclass the base plugin
                    if isinstance(plugin, BasePlugin):
                        # Force plugins to have unique names
                        if plugin.name not in self._pluginMap:
                            self._pluginMap[plugin.name] = plugin
                        else:
                            self.log.error("Plugin in file [%s] has name " \
                                               "[%s] which already exists!" % \
                                               (pluginName, plugin.name))
                    else:
                        self.log.error("Plugin [%s] must be a subclass of " \
                                            "the BasePlugin class!" % \
                                            plugin.name)
                except:
                    self.log.error("Failed to load plugin [%s]" % pluginName)
                    self.log.error(getStackTrace())
                    continue

    ##### Private functions #####

    def __processFilters(self, obj, direction):
        '''Process all the plugin filters for this object and data direction.

        * obj -- The object
        * direction -- The data direction

        '''
        responses = []
        for plugin in self._pluginMap.values():
            response = plugin.processFilters(obj, direction)

            # Plugins return False to drop the packet, None to ignore
            # the packet, or an object to respond to the packet
            if response == False:
                return False
            elif response is not None:
                responses.append(response)

        # Now, we need to rank the responses by their corresponding scores
        # to determine the best response to push forward
        # @todo: for now return the first response....later rank by score
        retResponses = (responses + [None])[0]
        return retResponses

    def __processSpeechRules(self, text):
        '''Process all the plugin speech rules for this recognized text.

        * text -- The recognized text

        '''
        # If a response is waiting, pass it the text
        if self._response is not None:
            self.log.debug("Calling yield response function", level=3)

            try:
                self._response.send(text)
                return False
            except StopIteration:
                # Get rid of the response once it is through yielding
                self._response = None
                return True

        for plugin in self._pluginMap.values():
            # If any plugin returns True, then one of its speech rules
            # matched the given text, otherwise it has not been matched yet
            response = plugin.processSpeechRules(text)

            # If the speech rule returned True, then we are done, otherwise
            # it might have returned a response type
            if response == True:
                self.log.info("Plugin [%s] matched the recognized speech." % 
                              plugin.name)
                return True
            else:
                # Create the actual response type from the given response
                self._response = handleResponse(self, response)

                # Stop processing speech rules if one is waiting for a response
                if self._response is not None:
                    self.log.info("Plugin [%s] matched the recognized " \
                                      "speech." % plugin.name)
                    break

        # None of the plugins had speech rules that applied to this text
        return False

    def __addPluginsToPath(self, directory):
        '''Add the plugins directory to the path.

        * directory -- The plugins directory

        '''
        baseDirectory = split(directory)[0]

        # Only add the base directory (directory which contains the plugins
        # directory) to the path once
        if baseDirectory not in path:
            path.insert(0, baseDirectory)
            import plugins

    def __importPlugin(self, pluginName):
        '''Import the plugin with the given name and load the given class.

        * pluginName -- The name of the plugin

        '''
        module = __import__(self.PluginsDirectoryName, fromlist=[pluginName])
        pluginModule = getattr(module, pluginName)
        return getattr(pluginModule, self.PluginClassName)
