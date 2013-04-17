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
'''The plugin module contains the BasePlugin class which provides the base
functionality from which all plugins will inherit.

'''
from types import GeneratorType

from pysiriproxy.constants import Keys
from pysiriproxy.plugins.speechRules import isSpeechRule, speechRuleMatches, \
    matches
from pysiriproxy.plugins.directions import isDirectionFilter, \
    directionsMatch, From_iPhone, From_Server
from pysiriproxy.plugins.objectClasses import isObjectClassFilter, \
    objectClassesMatch, SpeechPacket, SpeechRecognized, StartRequest

from pyamp.logging import Colors
from pyamp.util import getStackTrace


class BasePlugin:
    '''The BasePlugin class encapsulates the basic features of a plugin.
    This class provides the ability to load the set of filter functions,
    and then process them with a received object and an received direction.

    A filter function is created by decorating a class function with either
    the From_iPhone decorator, or the From_Server decorator. These filters
    will be processed in the event that an object is received from the given
    decorated direction. These functions can have any publicly visible name
    (i.e., do not start with __).

    Example::

        def Plugin(BasePlugin):
            @From_iPhone
            def exampleFilter(self, obj):
                self.log.debug("This will process all iPhone objects!")

    Filter functions can also be created to catch a specific object type by
    using specific object class decorators. The object class decorators are
    defined in the :mod:`.objectClasses` module.

    Example::

        def Plugin(BasePlugin):
            @StartRequest
            @From_iPhone
            def exampleFilter(self, obj):
                self.log.debug("This will process iPhone StartRequest objects!")

    In the above example, the *exampleFilter* function will be called in the
    event that a StartRequest object is received from the iPhone. Custom
    decorators can be created by calling the
    :func:`.objectClasses.createDecorator` function.

    Speech rules are created in a similar manner to object filters. Two
    decorators exist which allow a speech rule function to be called in the
    event that a given string matches the recognized speech, or if a regular
    expression matches the recognized speech.

    Example::

        def Plugin(BasePlugin):
            @matches("Test Siri Proxy")
            def testMatch(self, text):
                print "Matched the recognized speech!"

            @regex(".*Siri Proxy.*")
            def testRegex(self, text):
                print "Matched a regular expression!"

    The *@matches* decorator takes a string which it will compare to the
    recognized speech. A function using this decorator will be called in the
    event that the recognized speech matches the given string (it is case
    insensitive).

    The *@regex* decorator takes a regular expression which will use to
    match the recognized speech. A function using this decorator will be
    called in the event that the regular expression matches the recognized
    speech (it is case insensitive).

    Custom speech rule decorators can be created by creating a subclass of the
    :class:`.speechRules.Rule` class, and then calling the
    :func:`.speechRules.createDecorator` function with the 
    :class:`.speechRules.Rule` subclass.

    '''

    customCommandMap = {}
    '''The customCommandMap property defines a dictionary of custom command
    names mapped to the concrete plugin class function names that get called
    when the custom command is received from the iPhone.

    '''

    # Store the names of various properties that concrete plugins can override
    __NameProp = "name"
    __LogColorProp = "logColor"

    def __init__(self, manager, logger):
        '''
        * manager -- The PluginManager object
        * logger -- The logger

        '''
        self.__manager = manager

        # Force the name property to exist
        name = self.__forceProperty(self.__NameProp)

        # Get the logColor property which is optional
        logColor = self.__getProperty(self.__LogColorProp,
                                      Colors.Foreground.White)

        self.log = logger.get(name, color=logColor)
        self.__clearFilters()
        self.__clearSpeechRules()

        # Load the filters and speech rules for this plugin
        self.__loadFiltersAndRules()

        self.init()

    def getName(self):
        '''Get the name of this Plugin.'''
        return self.__getProperty(self.__NameProp)

    ##### Functions concrete plugins should override #####

    def init(self):
        '''Called after the BasePlugin is created.

        .. note:: This function can be overridden by concrete plugins.

        '''
        pass

    ##### Process filters for this plugin #####

    def processFilters(self, obj, direction):
        '''Process the filters for this Plugin.

        .. note:: This function should return False if the object should be
                  dropped, return None if the object is ignored by this
                  filter, or return the new object corresponding to the
                  response.

        * commandName -- The name of the object
        * direction -- The direction the object traveled to be received

        '''
        self.log.debug("Processing %d filters" % len(self.__filters), level=10)

        # Process all of the filters for this plugin
        for filterFunction in self.__filters:
            # Determine if this filter function applies to the current
            # object or direction
            if self.__filterApplies(filterFunction, direction, obj):
                # Filters return None when they ignore the object, otherwise
                # they have some effect on the current object
                try:
                    filterName = filterFunction.__name__
                    self.log.debug("Processing filter: %s" % filterName,
                                   level=10)

                    response = filterFunction(obj, direction)
                    if response is not None:
                        return response
                except:
                    self.log.error("Error in filter [%s]" % \
                                       filterFunction.__name__)
                    self.log.error(getStackTrace())

        # Object is ignored by this plugin
        return None

    @From_iPhone
    @StartRequest
    def customCommand(self, obj, direction):
        '''Create a default object filter for the start request command
        received from the iPhone. This allows the plugins to define a set
        of custom command names and map them to specific callback functions.

        * commandName -- The name of the object
        * direction -- The direction the object traveled to be received

        '''
        # Get the command name from the start request object
        commandName = self.__getStartRequestCommand(obj)

        functionName = self.customCommandMap.get(commandName)

        if functionName is not None:
            customFn = getattr(self, functionName, None)
            if customFn is not None:
                return customFn(obj)

        return None

    ##### Functions for processing speech rules #####

    def processSpeechRules(self, text):
        '''Process all of the speech rules for the recognized speech text.

        * text -- The recognized speech text

        '''
        self.log.debug("Processing %d speech rules for [%s]" % \
                           (len(self.__speechRules), text), level=10)

        # Process all of the speech rules for this plugin
        for ruleFunction in self.__speechRules:
            # If the given speech rule applies, then apply
            # it to the given text
            if self.__speechRuleApplies(ruleFunction, text):
                try:
                    self.log.debug("Processing speech rule: %s" % \
                                       ruleFunction.__name__, level=10)

                    # Speech rule functions have no return value, make sure
                    # to pass it the lowercase version of the text
                    resp = ruleFunction(text.lower())

                    # Only apply the first matched speech rule
                    return True if type(resp) != GeneratorType else resp
                except:
                    self.log.error("Error in speech rule [%s]" % \
                                       ruleFunction.__name__)
                    self.log.error(getStackTrace())

        # The text was not matched by any speech rules
        return False

    ##### Functions passed through to the PluginManager #####

    def showDirections(self, directionsType, source, destination,
                       utterance=None):
        '''Create a directions object and display it to the iPhone user.

        * directionsType -- The type of directions to show
        * source -- The starting location
        * destination -- The destination location
        * utterance -- The utterance to include

        '''
        self.__manager.showDirections(directionsType, source, destination,
                                      utterance=utterance)

    def showDrivingDirections(self, source, destination, utterance=None):
        '''Create driving directions object and display it to the iPhone user.

        * source -- The starting location
        * destination -- The destination location
        * utterance -- The utterance to include

        '''
        self.__manager.showDrivingDirections(source, destination,
                                             utterance=utterance)

    def showWalkingDirections(self, source, destination, utterance=None):
        '''Create walking directions object and display it to the iPhone user.

        * source -- The starting location
        * destination -- The destination location
        * utterance -- The utterance to include

        '''
        self.__manager.showWalkingDirections(source, destination,
                                             utterance=utterance)

    def showPublicTransitDirections(self, source, destination, utterance=None):
        '''Create public tranportation directions object and display it to
        the iPhone user.

        * source -- The starting location
        * destination -- The destination location
        * utterance -- The utterance to include

        '''
        self.__manager.showPublicTransitDirections(source, destination,
                                                   utterance=utterance)

    def makeView(self, views):
        '''Create a view and send it to the iPhone user.

        * views -- The list of views to create

        '''
        self.__manager.makeView(views)

    def ask(self, question, spoken=None):
        '''Command Siri to ask the user a question.

        * question -- The question to ask
        * spoken -- The text Siri will say

        '''
        self.__manager.ask(question, spoken)

    def resetContext(self):
        '''Reset the context.'''
        self.__manager.resetContext()

    def say(self, text, spoken=None):
        '''Command Siri to speak a piece of text.

        * text -- The text that Siri will display
        * spoken -- The text that Siri will speak

        '''
        self.__manager.say(text, spoken)

    def completeRequest(self):
        '''Complete a request to Siri.

        .. note:: This function should always be called by speech rules
                  otherwise Siri will continue to spin.

        '''
        self.__manager.completeRequest()

    ##### Private functions for loading filters #####

    def __clearFilters(self):
        '''Clear the filters for this plugin.'''
        self.__filters = []

    def __clearSpeechRules(self):
        '''Clear the speech rules for this plugin.'''
        self.__speechRules = []

    def __loadFiltersAndRules(self):
        '''Load all of the filters and speech rules for this Plugin.'''
        self.__clearFilters()
        self.__clearSpeechRules()

        # Traverse all of our functions
        for function in self.__getFunctions():
            # Handle a filter, or speech rule function accordingly
            if isDirectionFilter(function) or isObjectClassFilter(function):
                self.log.debug("Added filter [%s]" % function.__name__,
                               level=10)
                self.__filters.append(function)
            elif isSpeechRule(function):
                self.log.debug("Added speech rule [%s]" % function.__name__,
                               level=10)
                self.__speechRules.append(function)

    ##### Other private functions #####

    def __getFunctions(self):
        '''Return all of the functions for this class.'''
        # Filter out any builtin, and private functions
        attrs = filter(self.__isNotPrivateOrBuiltin, dir(self))

        # Get the objects for all of the class attributes
        objs = map(lambda attr: getattr(self, attr, None), attrs)

        # Filter out any non-existing attributes
        objs = filter(lambda obj: obj is not None, objs)

        # Now return only those that are functions
        return filter(lambda obj: hasattr(obj, "__call__"), objs)

    def __isNotPrivateOrBuiltin(self, attr):
        '''Determine if the given attribute is a private or builtin
        attribute name.

        * attr -- The name of the attribute

        '''
        return not attr.startswith("_") and not attr.find("__") != -1

    def __forceProperty(self, propName):
        '''Force the given property to exist.

        * propName -- The name of the property

        '''
        propValue = self.__getProperty(propName)

        # Check that the name property exists
        if propValue is None:
            raise Exception("Plugins must have a '%s' property!" % propName)

        return propValue

    def __getProperty(self, propName, default=None):
        '''Get the value of the given property.
        
        * default -- The default value

        '''
        return getattr(self, propName, default)

    def __filterApplies(self, function, direction, obj):
        '''Determine if the given filter function applies to either the
        given direction or the class of the given object.

        * direction -- The direction
        * obj -- The object

        '''
        objectClass = obj.get('class')
        return directionsMatch(function, direction) and \
            objectClassesMatch(function, objectClass)

    def __speechRuleApplies(self, function, text):
        '''Determine if the given speech rule function applies to
        the recognized text.

        * function -- The speech rule function
        * text -- The recognized text

        '''
        return speechRuleMatches(function, text)

    def __getStartRequestCommand(self, obj):
        '''Get the command name from the start request object.

        * obj -- The start request object

        '''
        utterance = None
        properties = obj.get(Keys.Properties)
        if properties is not None:
            utterance = properties.get(Keys.Utterance)

        return utterance
