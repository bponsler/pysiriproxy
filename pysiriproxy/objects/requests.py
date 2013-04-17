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
'''The request module contains classes pertaining to creating objects which
can be sent to the iPhone or Apple's web server which pertain to creating
requests to be sent to the iPhone.

'''
from pysiriproxy.objects.baseObject import SiriObject


class _RequestCompleted(SiriObject):
    '''The _RequestCompleted object notifies the iPhone that the current 
    request can be completed.

    '''
    def __init__(self, callbacks=None):
        '''
        * callbacks -- The list of callbacks

        '''
        SiriObject.__init__(self, "RequestCompleted", "com.apple.ace.system")
        self.callbacks = [] if callbacks is None else callbacks


class _StartRequest(SiriObject):
    '''The _StartRequest object signifies that a request is being started.

    '''
    def __init__(self, utterance="Testing", handsFree=False, proxyOnly=False):
        '''
        * utterance -- The utterance to perform
        * handsFree -- True if in hands free mode, False otherwise
        * proxyOnly -- True if proxy only mode, False otherwise

        '''
        SiriObject.__init__(self, "StartRequest", "com.apple.ace.system")
        self.utterance = utterance
        self.handsFree = handsFree
        if proxyOnly: # dont send local when false since its non standard
            self.proxyOnly = proxyOnly


class _GetRequestOrigin(SiriObject):
    '''The _GetRequestOrigin class creates an object that gets the
    origin of the request.

    '''

    def __init__(self, desiredAccuracy="HundredMeters", searchTimeout=8.0,
                 maxAge=1800):
        '''
        * desiredAccuracy -- The desired accuracy for the result
        * searchTimeout -- The timeout for the result
        * maxAge -- The maximum age for the result

        '''
        SiriObject.__init__(self, "GetRequestOrigin", "com.apple.ace.system")
        self.desiredAccuracy = desiredAccuracy
        self.searchTimeout = searchTimeout
        self.maxAge = maxAge


class _SetRequestOrigin(SiriObject):
    '''The _SetRequestOrigin class creates an object to set the origin of
    a request.

    '''

    def __init__(self, longitude=-122.030089795589, latitude=37.3317031860352,
                 desiredAccuracy="HundredMeters", altitude=0.0, speed=1.0,
                 direction=1.0, age=0, horizontalAccuracy=50.0,
                 verticalAccuracy=10.0):
        '''
        * longitude -- The longitude for the request
        * latitude -- The latitude for the request
        * desiredAccuracy -- The desired accuracy for the request
        * altitude -- The altitude for the request
        * speed -- The speed for the request
        * direction -- The direction for the request
        * age -- The age for the request
        * horizontalAccuracy -- The horizontal accuracy for the request
        * verticalAccuracy -- The vertical accuracy for the request

        '''
        SiriObject.__init__(self, "SetRequestOrigin", "com.apple.ace.system")
        self.horizontalAccuracy = horizontalAccuracy
        self.latitude = latitude
        self.desiredAccuracy = desiredAccuracy
        self.altitude = altitude
        self.speed = speed
        self.longitude = longitude
        self.verticalAccuracy = verticalAccuracy
        self.direction = direction
        self.age = age


class Requests:
    '''The Requests class contains the various types of Requests as well as a
    function for creating Requests of a specific type.

    This class contains a factory method for creating Request object of
    a specific type.

    '''
    GetRequestOrigin = "GetRequestOrigin"
    '''The GetRequestOrigin object type.'''

    RequestCompleted = "Completed"
    '''The RequestCompleted object type.'''

    SetRequestOrigin = "SetRequestOrigin"
    '''The SetRequestOrigin object type.'''

    StartRequest = "StartRequest"
    '''The StartRequest object type.'''


    # Create a dictionary mapping the types to their respective objects
    __TypeMap = {
        GetRequestOrigin: _GetRequestOrigin,
        RequestCompleted: _RequestCompleted,
        SetRequestOrigin: _SetRequestOrigin,
        StartRequest: _StartRequest
        }

    @classmethod
    def create(cls, requestType, *args, **kwargs):
        '''Create a Request of the given type.

        * requestType -- The request type
        * args -- The arguments
        * kwargs -- The keyword arguments

        '''
        request = None

        # Create the request object if it is found
        requestClass = Requests.__TypeMap.get(requestType)
        if requestClass is not None:
            request = requestClass(*args, **kwargs)

        return request
