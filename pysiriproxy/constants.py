# Copyright (C) 2012 Brett Ponsler, Pete Lamonica
# See the file "COPYING" for the full license governing this code.
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
'''The constants module contains classes which contain properties that
define various constant values used throughout the system.

The majority of these properties are used to access certain values from the
object dictionaries sent between the iPhone and Apple's server.

'''
from pyamp.patterns import Enum


class Modes:
    '''The Modes class contains properties which define different types of
    data receiving modes.

    '''

    Line = "line"
    '''The Line property indicates the mode in which lines of data is
    sent and received.

    '''

    Raw = "raw"
    '''The Raw property indicates the mode in which raw data is sent
    and received.

    '''


class Directions:
    '''The Directions class contains several properties which are used to
    indicate which direction data is entering the system.

    '''

    From_Server = "From_Server"
    '''The From_Server property indicates that data was received from Apple's
    server.

    '''

    From_iPhone = "From_iPhone"
    '''The From_iPhone property indicates that data was received from the
    iPhone.

    '''


class ClassNames(Enum):
    '''The ClassNames class contains properties which define the names of the
    class names of objects sent between the iPhone and Apple's server.

    '''
    AnyObject = "AnyObject"
    '''The AnyObject property defined the AnyObject object class.'''

    CancelRequest = "CancelRequest"
    '''The CancelRequest property defined the CancelRequest object class.'''

    CancelSpeech = "CancelSpeech"
    '''The CancelSpeech property defined the CancelSpeech object class.'''

    ClearContext = "ClearContext"
    '''The ClearContext property defined the ClearContext object class.'''

    CommandIgnored = "CommandIgnored"
    '''The CommandIgnored property defined the CommandIgnored object class.'''

    CommandFailed = "CommandFailed"
    '''The CommandFailed property defined the CommandFailed object class.'''

    FinishSpeech = "FinishSpeech"
    '''The FinishSpeech property defined the FinishSpeech object class.'''

    LoadAssistant = "LoadAssistant"
    '''The LoadAssistant property defined the LoadAssistant object class.'''

    RequestCompleted = "RequestCompleted"
    '''The RequestCompleted property defined the RequestCompleted object
    class.

    '''

    SetApplicationContext = "SetApplicationContext"
    '''The SetApplicationContext property defined the SetApplicationContext
    object class.

    '''

    SetRequestOrigin = "SetRequestOrigin"
    '''The SetRequestOrigin property defined the SetRequestOrigin object
    class.

    '''

    SetRestrictions = "SetRestrictions"
    '''The SetRestrictions property defined the SetRestrictions object class.

    '''

    SpeechPacket = "SpeechPacket"
    '''The SpeechPacket property defined the SpeechPacket object class.'''

    SpeechRecognized = "SpeechRecognized"
    '''The SpeechRecognized property defined the SpeechRecognized object
    class.

    '''

    StartRequest = "StartRequest"
    '''The StartRequest property defined the StartRequest object class.'''

    StartSpeechRequest = "StartSpeechRequest"
    '''The StartSpeechRequest property defined the StartSpeechRequest
    object class.

    '''


class Keys:
    '''The Keys class defines various properties which contain strings which
    are keys to the dictionary objects sent between the iPhone and Apple's
    server.

    '''

    AceId = "aceId"
    '''The aceId key.'''

    AssistantId = 'AssistantId'
    '''The key for the AssistantId property of an object.'''

    Birthday = "birthday"
    '''The birthday key for an object.'''

    Class = "class"
    '''The class name for the object.'''

    Data = "data"
    '''The key for the data property of an object. '''

    Date = "date"
    '''The date key for an object.'''

    DateSent = "dateSent"
    '''The key for the dateSent property of an object.'''

    DisplayText = "displayText"
    '''The key for the displayText property of an object.'''

    DueDate = "dueDate"
    '''The due date key for an object.'''

    FirstName = "firstName"
    '''The key for the firstName property of an object.'''

    FullName = "fullName"
    '''The key for the fullName property of an object.'''

    Group = "group"
    '''The group for the object.'''

    Identifier = "identifier"
    '''The key for the identifier property of an object.'''

    Interpretations = "interpretations"
    '''The interpretations key for an object.'''

    Label = "label"
    '''The key for the label property of an object.'''

    LastName = "lastName"
    '''The key for the lastName property of an object.'''

    MsgSender = "msgSender"
    '''The key for the msgSender property of an object.'''

    Number = "number"
    '''The key for the number property of an object.'''

    OrderedContext = 'orderedContext'
    '''The key for the orderedContext property of an object.'''

    Outgoing = "outgoing"
    '''The key for the outgoing property of an object.'''

    Phones = "phones"
    '''The key for the phones property of an object.'''

    Phrases = "phrases"
    '''The phrases key for an object.'''

    Properties = "properties"
    '''The properties key for the object.'''

    Recognition = "recognition"
    '''The recognition key for an object.'''

    RefId = "refId"
    '''The refId for the object.'''

    RemoveSpaceAfter = "removeSpaceAfter"
    '''The removeSpaceAfter key for an object.'''

    RemoveSpaceBefore = "removeSpaceBefore"
    '''The removeSpaceBefore key for an object.'''

    SelectionResponse = "selectionResponse"
    '''The key for the selectionResponse property of an object.'''

    SessionValidationData = 'SessionValidationData'
    '''The key for the SessionValidationData property of an object.'''

    SpeakableSelectionResponse = "speakableSelectionResponse"
    '''The key for the speakableSelectionResponse property of an object.'''

    SpeakableText = "speakableText"
    '''The speakable text key for an object.'''

    SpeechId = 'SpeechId'
    '''The key for the SpeechId property of an object.'''

    Street = "street"
    '''The street value.'''

    Text = "text"
    '''The text key for an object.'''

    TheatricalReleaseDate = "theatricalReleaseDate"
    '''The theatrical release date.'''

    Title = "title"
    '''The title key for an object.'''

    Tokens = "tokens"
    '''The tokens key for an object.'''

    Utterance = "utterance"
    '''The utterance key for an object.'''

    Version = "v"
    '''The version key for an object.'''


class DirectionTypes:
    '''The DirectionTypes class encapsulates the various modes of
    transportation which can be used to generate directions.

    '''
    Driving = "ByCar"
    '''Directions for driving.'''

    PublicTransit = "ByPublicTransit"
    '''Directions for public transportation.'''

    Walking = "Walking"
    '''Directions for walking.'''


class HeaderKeys:
    '''The HeaderKeys class contains definitions of various tags
    that are sent in headers.

    '''

    ContentLength = "Content-Length"
    '''The content length header tag.'''

    Host = "Host"
    '''The Host header tag.'''

    UserAgent = "User-Agent"
    '''The user agent header tag.'''

    XAceHost = "X-Ace-Host"
    '''The x ace host header tag.'''
