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
'''The views module contains classes pertaining to creating objects which
can be sent to the iPhone or Apple's web server which pertain to creating
views on the iPhone.

'''
from pysiriproxy.constants import DirectionTypes
from pysiriproxy.objects.baseObject import SiriObject


class _AddViews(SiriObject):
    '''The _AddViews class creates an object that can create a series of views
    to be displayed on the iPhone.

    '''

    def __init__(self, scrollToTop=False, temporary=False,
                 dialogPhase="Completion", views=None, callbacks=None):
        '''
        * scrollToTop -- True to scroll to the top of the Siri view
        * temporary -- True for a temporary view, False otherwise
        * dialogPhase -- The dialog phase indicator
        * views -- The list of views to display
        * callbacks -- The list of callbacks

        '''
        SiriObject.__init__(self, "AddViews", "com.apple.ace.assistant")

        # Set the default value of all properties
        self.scrollToTop = scrollToTop
        self.views = [] if views is None else views
        self.temporary = temporary
        self.dialogPhase = dialogPhase
        self.callbacks = [] if callbacks is None else callbacks


class _Utterance(SiriObject):
    '''The _Utterance class creates an object that can display a given piece
    of text and have Siri speak another given piece of text (or the same
    piece of text).

    '''

    def __init__(self, displayText="", spokenText=None,
                 listenAfterSpeaking=False, dialogIdentifier="Misc#ident"):
        '''
        * displayText -- The text to be displayed
        * spokenText -- The text that Siri will speak, if None is given then
                        Siri will speak the text that is displayed
         * listenAfterSpeaking -- True to have Siri listen after she is done
                                  speaking
         * dialogIdentifier -- The identifier for the dialog

        '''
        SiriObject.__init__(self, "AssistantUtteranceView",
                            "com.apple.ace.assistant")
        self.text = displayText
        self.speakableText = displayText if spokenText is None else spokenText
        self.dialogIdentifier = dialogIdentifier
        self.listenAfterSpeaking = listenAfterSpeaking


class _MapItemSnippet(SiriObject):
    '''The _MapItemSnippet class creates a map item snippet to be displayed
    to the iPhone user.

    '''
    def __init__(self, useCurrentLocation=True, items=None):
        '''
        * useCurrentLocation -- True to use the user's current location
        * items -- The list of map items

        '''
        SiriObject.__init__(self, "MapItemSnippet",
                            "com.apple.ace.localsearch")

        self.useCurrentLocation = useCurrentLocation
        self.items = [] if items is None else items


class _ShowMapPoints(SiriObject):
    '''The _ShowMapPoints class creates a series of map poitns to be displayed
    to the iPhone user.

    '''

    def __init__(self, showDirections=True, showTraffic=False,
                 directionsType=DirectionTypes.Driving, callbacks=None,
                 source=None, destination=None):
        '''
        * showDirections -- True to show the directions, False otherwise
        * showTraffic -- True to show the traffic, False otherwise
        * directionsType -- The type of directions to display
        * callbacks -- The callbacks to use
        * source -- The starting location
        * destination -- The ending destination

        '''
        SiriObject.__init__(self, "ShowMapPoints", "com.apple.ace.localsearch")

        self.showDirections = showDirections
        self.showTraffic = showTraffic
        self.directionsType = directionsType
        self.callbacks = [] if callbacks is None else callbacks
        self.itemSource = SiriObject() if source is None else source
        self.itemDestination = SiriObject() if destination is None else \
            destination


class _AnswerSnippet(SiriObject):
    '''The _AnswerSnipper class creates an answer snippet to be displayed
    to the iPhone user.

    '''

    def __init__(self, answers=None, confirmationOptions=None):
        '''
        * answers -- The list of answers to display
        * confirmationOptions -- True to display the confirmation options

        '''
        SiriObject.__init__(self, "Snippet", "com.apple.ace.answer")

        self.answers = [] if answers is None else answers

        if confirmationOptions:
            self.confirmationOptions = confirmationOptions


class Views:
    '''Contains the various types of Views as well as a function for
    creating Views of a specific type.

    This class also contains a factory method for creating views of a specific
    type.

    '''

    AddViews = "AddViews"
    '''The AddViews object type.'''

    AnswerSnippet = "AnswerSnippet"
    '''The AnswerSnippet object type.'''

    MapItemSnippet = "MapItemSnippet"
    '''The MapItemSnippet object type.'''

    MapPoints = "MapPoints"
    '''The ShowMapPoints object type.'''

    Utterance = "Utterance"
    '''The Utterance object type.'''

    # Create a dictionary mapping the types to their respective objects
    __TypeMap = {
        AddViews: _AddViews,
        AnswerSnippet: _AnswerSnippet,
        MapItemSnippet: _MapItemSnippet,
        MapPoints: _ShowMapPoints,
        Utterance: _Utterance
        }

    @classmethod
    def create(cls, viewType, *args, **kwargs):
        '''Create a View of the given type.

        * viewType -- The type of View to create
        * args -- The arguments
        * kwargs -- The keyword arguments to create

        '''
        view = None

        # Create the view object if it is found
        viewClass = Views.__TypeMap.get(viewType)
        if viewClass is not None:
            view = viewClass(*args, **kwargs)

        return view
