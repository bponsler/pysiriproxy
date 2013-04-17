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
'''The factory module contains classes which provide factory functions
for creating concrete :class:`.SiriObjects` for specific purposes.

'''
from pysiriproxy.constants import DirectionTypes
from pysiriproxy.objects.baseObject import SiriObject

# Include all the various types of objects we can create
from pysiriproxy.objects.views import Views
from pysiriproxy.objects.actions import Actions
from pysiriproxy.objects.buttons import Buttons
from pysiriproxy.objects.commands import Commands
from pysiriproxy.objects.requests import Requests
from pysiriproxy.objects.dataObjects import DataObjects


class ObjectFactory:
    '''The ObjectFactory provides factory methods for constructing concrete
    :class:`.SiriObject` objects of specific types.

    '''

    @classmethod
    def action(cls, actionType, *args, **kwargs):
        '''Create a :class:`.SiriObject` :class:`.Action` of the specific type.

        * actionType -- The type of action to create
        * args -- The arguments
        * kwargs -- The keyword arguments

        '''
        return Actions.create(actionType, *args, **kwargs)

    @classmethod
    def button(cls, buttonType, buttonText, *args, **kwargs):
        '''Create a :class:`.SiriObject` :class:`.Button` of the specific type.

        * buttonType -- The type of Button to create
        * buttonText -- The button text
        * args -- The argumnets
        * kwargs -- The keyword arguments

        '''
        return Buttons.create(buttonType, buttonText, *args, **kwargs)

    @classmethod
    def utterance(cls, displayText, spokenText=None, listenAfterSpeaking=False,
                  identifier="Misc#ident"):
        '''Create a :class:`.SiriObject` utterance.

        * displayText -- The text to display
        * spokenText -- The text that Siri will speak
        * listenAfterSpeaking -- True for Siri to listen for a response
        * identifier -- The identifier for the utterance

        '''
        return Views.create(Views.Utterance, displayText=displayText,
                            spokenText=spokenText,
                            listenAfterSpeaking=listenAfterSpeaking,
                            dialogIdentifier=identifier)

    @classmethod
    def location(cls, street=None, city=None, stateCode=None, countryCode=None,
                 postalCode=None, latitude=None, longitude=None):
        '''Create a :class:`.SiriObject` location.

        * street -- The string containing the street for the location
        * city -- The string containing the city for the location
        * stateCode -- The string containing the state code for the location
        * countryCode -- The string containing the country code for the
                         location
        * postalCode -- The string containing the postal code for the location
        * latitude -- The string containing the latitude for the location
        * longitude -- The string containing the longitude for the location

        '''
        return DataObjects.create(DataObjects.Location, street=street,
               city=city, stateCode=stateCode, countryCode=countryCode,
               postalCode=postalCode, latitude=latitude, longitude=longitude)

    @classmethod
    def currentLocation(cls, label=None):
        '''Create a :class:`.SiriObject` for the current location.

        * label -- The label to display on the map pin

        '''
        return DataObjects.create(DataObjects.CurrentLocation, label=label)

    @classmethod
    def mapItem(cls, locations):
        '''Create a :class:`.SiriObject` map item.

        * locations -- The list of locations to display on the map

        '''
        items = []

        # Create locations for all of the locations in the given list
        for label, location in locations:
            mapItem = DataObjects.create(DataObjects.MapItem, label=label,
                                         location=location)
            items.append(mapItem)

        return Views.create(Views.MapItemSnippet, useCurrentLocation=False,
                            items=items)

    @classmethod
    def directions(cls, directionsType, source, destination, utterance=None):
        '''Create a :class:`.SiriObject` to display directions between two
        locations.

        * directionsType -- The type of directions to provide
        * source -- The source location
        * destination -- The destination location
        * utterance -- The utterance to speak

        '''
        # @todo: Allow source and destination to be passed as
        #        Locations, OR MapItems, and convert the Locations
        #        to MapItems accordingly.
        mapPoints = Views.create(Views.MapPoints, source=source,
                                 destination=destination,
                                 directionsType=directionsType)

        commands = [mapPoints]
        resultCallback = Commands.create(Commands.ResultCallback,
                                         commands=commands)

        callbacks = [resultCallback]

        views = []
        # Add the utternace to the views, if an utterance is given
        if utterance is not None:
            views.append(utterance)

        addViews = Views.create(Views.AddViews, callbacks=callbacks,
                                views=views)

        # Note: Adding the ace id makes the map points work properly
        addViews.setAceId()

        commands = [addViews]
        resultCallback = Commands.create(Commands.ResultCallback,
                                         commands=commands)
        callbacks = [resultCallback]
        completed = Requests.create(Requests.RequestCompleted,
                                    callbacks=callbacks)
        return completed

    @classmethod
    def drivingDirections(cls, source, destination, utterance=None):
        '''Create driving directions between the two locations.

        * source -- The source location
        * destination -- The destination location
        * utterance -- The utterance to speak

        '''
        return cls.direction(DirectionTypes.Driving, source, destination,
                             utterance=utterance)

    @classmethod
    def walkingDirections(cls, source, destination, utterance=None):
        '''Create walking directions between the two locations.

        * source -- The source location
        * destination -- The destination location
        * utterance -- The utterance to speak

        '''
        return cls.direction(DirectionTypes.Walking, source, destination,
                             utterance=utterance)

    @classmethod
    def publicTransitDirections(cls, source, destination, utterance=None):
        '''Create public transportation directions between the two locations.

        * source -- The source location
        * destination -- The destination location
        * utterance -- The utterance to speak

        '''
        return cls.direction(DirectionTypes.PublicTransit, source, destination,
                             utterance=utterance)


class ResponseFactory:
    '''The ResponseFactory is responsible for creating specific
    :class:`.SiriObject` responses to be sent from pysiriproxy to the iPhone
    user. These responses include things such as, creating a view composed of
    :class:`.SiriObjects`, sending a request completed object, and others.

    '''

    @classmethod
    def directions(cls, refId, directionsType, source, destination,
                   utterance=None):
        '''Create directions to be sent to the iPhone.

        * refId -- The reference id
        * directionsType -- The type of directions to provide
        * source -- The source location
        * destination -- The destination location
        * utterance -- The utterance to speak

        '''
        directions = ObjectFactory.directions(directionsType, source,
                                              destination, utterance=utterance)
        directions.makeRoot(refId)
        return directions.toDict()

    @classmethod
    def drivingDirections(cls, refId, source, destination, utterance=None):
        '''Create driving directions to be sent to the iPhone.

        * refId -- The reference id
        * source -- The source location
        * destination -- The destination location
        * utterance -- The utterance to speak

        '''
        return cls.directions(DirectionTypes.Driving, source, destination,
                              utterance=utterance)

    @classmethod
    def walkingDirections(cls, refId, source, destination, utterance=None):
        '''Create walking directions to be sent to the iPhone.

        * refId -- The reference id
        * source -- The source location
        * destination -- The destination location
        * utterance -- The utterance to speak

        '''
        return cls.directions(DirectionTypes.Walking, source, destination,
                              utterance=utterance)

    @classmethod
    def publicTransitDirections(cls, refId, source, destination,
                                utterance=None):
        '''Create public transportation directions to be sent to the iPhone.

        * refId -- The reference id
        * source -- The source location
        * destination -- The destination location
        * utterance -- The utterance to speak

        '''
        return cls.directions(DirectionTypes.PublicTransit, source,
                              destination, utterance=utterance)

    @classmethod
    def view(cls, refId, subObjects, dialogPhase="Completion"):
        '''Create an utterance view composed of several sub objects.

        * refId -- The reference id
        * subObjects -- The list of SiriObjects the view will be composed of
                        or a list of tuple arguments to create SiriObjects
        * dialogPhase -- The dialogPhase

        '''
        addViews = Views.create(Views.AddViews, dialogPhase=dialogPhase,
                                views=subObjects)
        addViews.makeRoot(refId)
        return addViews.toDict()

    @classmethod
    def utterance(cls, refId, displayText, spokenText=None,
                  listenAfterSpeaking=False, identifier="Misc#ident"):
        '''Create an utterance with the given display text, and spoken text.

        * refId -- The reference id
        * displayText -- The text to be displayed
        * spokenText -- The text to be spoken by Siri
        * listenAfterSpeaking -- True for Siri to listen for a response
                                 after speaking, False otherwise

        '''
        utterance = ObjectFactory.utterance(displayText, spokenText,
                                            listenAfterSpeaking, identifier)
        return ResponseFactory.view(refId, [utterance])

    @classmethod
    def requestCompleted(cls, refId, callbacks=None):
        '''Create a request completed object.

        * refId -- The reference id
        * callbacks -- The list of callbacks

        '''
        completed = Requests.create(Requests.RequestCompleted,
                                    callbacks=callbacks)
        completed.makeRoot(refId)

        return completed.toDict()
