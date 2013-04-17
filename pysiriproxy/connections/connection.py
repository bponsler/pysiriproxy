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
'''The connection module contains the Connection class which provides
the base functionality for creating concrete connections between two
networked computers.

'''
import re
import zlib
from os.path import join
from binascii import unhexlify
from struct import unpack, pack

from twisted.protocols.basic import LineReceiver

from pysiriproxy.plist import Plist
from pysiriproxy.utils import toHex
from pysiriproxy.interpreter import Interpreter
from pysiriproxy.constants import Modes, HeaderKeys
from pysiriproxy.plugins.manager import PluginManager
from pysiriproxy.connections.manager import ConnectionManager

from pyamp.logging import Colors, LogData


class Connection(LineReceiver):
    '''The Connection class implements the base functionaltiy for creating
    a concrete twisted internet protocol which is able to receive data in
    the form of lines.

    This base class implements the functionality of receiving data from the
    iPhone or from Apple's web server. The iPhone Apple's web server transmit
    plist objects which are compressed using zlib compression. This class
    implements the necessary functionality for receiving the data, and
    decompressing it to retrieve the plist object data that is being
    transmitted.

    The Connection objects are connected to the
    :class:`.connections.ConnectionManager` which provides the ability for
    one Connection to forward data to another Connection.

    .. note:: This class is intended to be subclassed to create a connection
              between two specific machines.

    '''

    def __init__(self, name, direction, logger,
                 logColor=Colors.Foreground.White):
        '''
        * name -- The name of this Connection
        * direction -- The direction of the data coming into this Connection
        * logger -- The logger for this Connection
        * logColor -- The log color for this Connection

        '''
        self.__direction = direction
    
        # Connect this connection to the connection manager
        self.__connectionManager = ConnectionManager(logger)
        self.__connectionManager.connect(self)

        # Grab an instance to the plugin manager
        self.__pluginManager = PluginManager(self.__connectionManager, logger)

        # If no logger is given, be sure to create it
        if logger is None:
            logger = LogData(name)
        self.log = logger.get(name, color=logColor)
        self.__logger = logger

        self.__compStream = zlib.compressobj()
        self.__zipStream = zlib.decompressobj()
        self.__processedHeaders = False
        self.__consumedAce = False

        self.__inputBuffer = ""
        self.__outputBuffer = ""
        self.__unzippedInput = ""
        self.__unzippedOutput = ""

        self.ssled = False
        self.__lastRefId = None
        self.__blockRestOfSession = False
        self.otherConnection = None

        # Starts in line mode
        self.__mode = Modes.Line

    def reset(self):
        '''Reset this connection.'''
        self.__lastRefId = None
        self.__blockRestOfSession = False

    def getDirection(self):
        '''Get the direction for this connection.'''
        return self.__direction

    def getMode(self):
        '''Get the current receiving mode the server is in.'''
        return self.__mode

    def setLineMode(self):
        '''Set the server to receive lines.'''
        LineReceiver.setLineMode(self)
        self.__mode = Modes.Line

    def setRawMode(self):
        '''Set the server to receive raw data.'''
        LineReceiver.setRawMode(self)
        self.__mode = Modes.Raw

    def connectionMade(self):
        '''This function is called when a connection is made.'''
        self.log.debug("Connection made.", level=2)

    def connectionLost(self, reason):
        '''This function is called when a connection is lost.

        * reason -- The reason the connection was lost

        '''
        self.log.debug("Connection lost: %s" % str(reason), level=2)

    def connectionFailed(self, reason):
        '''This function is called when a connection failed.

        * reason -- The reason the connection was lost

        '''
        self.log.error("Connection failed: %s" % str(reason))

    def lineReceived(self, line):
        '''This function is called when a line of data is received.

        * line -- The line of data

        '''
        self.log.debug("[Header]: %s" % line, level=5)

        # Parse the header if it's a data/value pair
        if line.find(": ") != -1:
            # Get the tag, and value from the header
            tag, value = line.split(": ")

            # Determine if this header contains the expected server hostname
            if tag == HeaderKeys.Host:
                self.log.debug("iPhone wants to connect to: %s" % value,
                               level=5)

        # An empty line denotes the end of the headers
        if line == "":
            self.log.debug("Found end of headers.", level=5)
            self.__processedHeaders = True
            self.setRawMode()

        # Restore the CR-LF to the end of the line
        self.__outputBuffer += line + "\x0d\x0a"
    
        self.__flushOutputBuffer()

    def rawDataReceived(self, data):
        '''This function is called when raw data is received.

        * data -- The raw data

        '''
        self.log.debug("Received data: %d" % len(data), level=7)

        self.__inputBuffer += data

        if not self.__consumedAce:
            self.log.debug("Consuming ace", level=5)
            self.__outputBuffer += self.__inputBuffer[:4]
            self.__inputBuffer = self.__inputBuffer[4:]
            self.__consumedAce = True

        self.__processCompressedData()

        self.__flushOutputBuffer()

    def __processCompressedData(self):
        '''Process compressed data.

        * data -- The compressed data to process

        '''
        # Unzip the input stream
        decomp = self.__zipStream.decompress(self.__inputBuffer)

        self.__unzippedInput = ''.join(decomp)
        self.__inputBuffer = ""

        # Print the decompressed data for debugging purposes
        lines = [
            "############# Decompressed Data #############",
            toHex(self.__unzippedInput),
            ]
        for line in lines:
            self.log.debug(line, level=7)
            self.log.debug("#" * 45, level=7)

        # Continue so long as there are other objects
        while self.__hasNextObject():
            obj = self.__readNextObjectFromUnzipped()

            # Will be nil if the next object is a ping/pong
            if obj is not None:
                self.log.debug("Received object: [%s]" % obj['class'], level=2)

                # Print the add views object for debugging purposes
                if obj.get('class') == 'AddViews':
                    self.log.debug("========== AddViews ==========", level=2)
                    self.log.debug(obj, level=2)
                    self.log.debug("========== AddViews ==========", level=2)

                # Give the world a chance to mess with folks
                newObject = self.__prepReceivedObject(obj)

                # Might be nil if "the world" decides to rid us of the object
                if newObject is not None:
                    self.injectObjectToOutputStream(newObject)

    def __hasNextObject(self):
        '''Determine if there is an object waiting to be processed.'''
        if len(self.__unzippedInput) == 0:
            return False

        unpacked = self.__unpackUnzippedInput(self.__unzippedInput[0:5])
        self.log.debug("Unpacked: %s" % unpacked, level=7)

        # Ping or pong packet
        pattern = re.compile("^0[34]")
        if pattern.match(unpacked) is not None:
            return True
    
        # Clear context packet
        pattern = re.compile("^ff")
        if pattern.match(unpacked) is not None:
            return True

        # Rogue packet
        pattern = re.compile("^[0-9][15-9]")
        if pattern.match(unpacked) is not None:
            return False

        # Data packet
        pattern = re.compile("^0200(.{6})")
        matched = pattern.match(unpacked)

        if matched is None:
            self.log.error("Error matching packet!")
            self.log.error(toHex(unpacked))
            return False

        objectLength = int(matched.groups()[0], 16)

        # Determine if the length of the next object (plus its prefix)
        # is less than the input buffer
        return (objectLength + 5) <= len(self.__unzippedInput)

    def __readNextObjectFromUnzipped(self):
        '''Read, and return, the next object from the unzipped input buffer.'''
        unpacked = self.__unpackUnzippedInput(self.__unzippedInput[0:5])

        pattern = re.compile("^(..)(.{8})$")
        matched = pattern.match(unpacked).groups()

        # Ping or pong -- just get these out of the way
        # (and log them for good measure)
        if matched is not None and (matched[0] == "03" or matched[0] == "04"):
            unzippedObject = self.__unzippedInput[0:5]
            self.__unzippedOutput += unzippedObject
      
            # Determine what type of packet this is
            if matched[0] == "03":
                objectType = "Ping"
            elif matched[0] == "04":
                objectType = "Pong"
            else:
                objectType = "ClearContext"

            self.log.debug("Received %s (%d)" % (objectType,
                                                 int(matched[1], 16)), level=7)
            self.__unzippedInput = self.__unzippedInput[5:]
      
            self.__flushUnzippedOutput()
            return None
  
        objectSize = int(matched[1], 16)
        prefix = self.__unzippedInput[0:5]
        objectData = self.__unzippedInput[5:objectSize + 5]
        self.__unzippedInput = self.__unzippedInput[objectSize + 5:]

        # Conver the object to a plist and return it
        return Plist.convert(objectData)

    def __prepReceivedObject(self, obj):
        '''Prep the object that was received.

        * obj -- The object that was received

        '''
        # Grab the ref and ace ids
        refId = obj.get("refId")
        aceId = obj.get("aceId")

        if refId is not None:
            # If the refId matches our last ref id and we are expected
            # to block the rest of the session than this packet should
            # be dropped
            if refId == self.__lastRefId and self.__blockRestOfSession:
                self.log.debug("Dropping object from Server: %s" % \
                                   obj.get("class"), level=2)
                return None
        elif aceId is not None:
            # The aceId in the request often refers to the refId in the
            # response from the server. If there was no refId given in
            # the request, then use the aceId instead
            if self.__blockRestOfSession and self.__lastRefId != aceId:
                self.__blockRestOfSession = False
            self.__setRefId(aceId)
    
        # Process the object filters for this object, and make sure an
        # object was returned from the object filters
        processedObject = self.__processObjectFilters(obj)
        if processedObject is None:
            self.log.debug("Dropping object [%s]" % obj["class"], level=2)
            return None

        # Block the rest of the session if a plugin claims ownership
        speech = Interpreter.speechRecognized(obj)
        if speech is not None:
            self.log.info("Speech recognized: [%s]" % speech)
            self.injectObjectToOutputStream(obj)

            # Process the speech with all of the known plugin speech rules
            if self.__pluginManager.processSpeechRules(speech):
                self.__blockRestOfSession = True

            return None
    
        return obj

    def __processObjectFilters(self, obj):
        '''Process all of the plugin filters for the given object.
        
        * obj -- The received object

        '''
        return self.__pluginManager.processFilters(obj, self.__direction)

    def __unpackUnzippedInput(self, unzipped):
        '''Unpack the given unzipped object into a hexadecimal string.

        * unzipped -- The unzipped object

        '''
        return ''.join(map(lambda a: '%.2X' % ord(a), unzipped))

    def injectObjectToOutputStream(self, obj):
        '''Inject the given object into the output stream of this
        connection. This effectively sends the object to the foward destination
        connection for this connection.

        * obj -- The object to inject into the output stream

        '''
        refId = obj.get("refId")
        if refId is not None and len(refId) > 0:
            # If the refIds have changed than this is a new session
            if self.__blockRestOfSession and self.__lastRefId != refId:
                self.__blockRestOfSession = False
            self.__setRefId(refId)

        # Convert the object to a binary plist
        objectData = Plist.toBinary(obj, self.__logger)

        # Recalculate the size in case the object gets modified. If new size is
        # zero, then remove the object from the stream entirely
        objLen = len(objectData)

        self.log.debug("Forwarding object [%s] to %s, len: %d" % \
                    (obj.get('class'),
                    self.__connectionManager.getForwardName(self.__direction),
                    objLen), level=5)
    
        if objLen > 0:
            # Get the header containing the length of the object, and pad
            # zeros to the left to make it ten digits long
            hexStr = '%X' % (0x0200000000 + objLen)
            hexStr = hexStr.rjust(10, '0')

            # Get the prefix by converting the hex length into binary
            prefix = unhexlify(hexStr)

            self.__unzippedOutput += prefix + objectData

        self.__flushUnzippedOutput()

    def __flushUnzippedOutput(self):
        '''Flush the unzipped output buffer.'''
        # Compress the unzipped output buffer
        self.__outputBuffer += \
            self.__compStream.compress(self.__unzippedOutput)
        self.__outputBuffer += self.__compStream.flush(zlib.Z_SYNC_FLUSH)

        self.__unzippedOutput = ""
    
        self.__flushOutputBuffer()

    def __flushOutputBuffer(self):
        '''Flush the output buffer.'''
        # Ensure the output buffer has data to flush
        if len(self.__outputBuffer) == 0:
            return

        # Ensure that this connection is connected to a destination connection
        if self.__connectionManager.hasConnection(self.__direction):
            self.__connectionManager.forward(self.__direction,
                                             self.__outputBuffer)
            self.__outputBuffer = ""
        else:
            self.log.debug("Buffering some data for later: %d bytes " \
                               "buffered" % len(self.__outputBuffer), level=5)

    def getConnectionManager(self):
        '''Get the ConnectionManager object for this Connection.'''
        return self.__connectionManager

    def getRefId(self):
        '''Get the most recently used reference id.'''
        return self.__lastRefId

    def setRefId(self, refId):
        '''Set the reference id.

        * refId -- The reference id

        '''
        self.__lastRefId = refId

    def __setRefId(self, refId):
        '''Set the ref id for this connection and our forward destination
        connection.

        * refId -- The ref id

        '''
        self.setRefId(refId)
        self.__connectionManager.setRefId(refId, self.__direction)
