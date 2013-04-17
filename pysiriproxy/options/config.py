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
'''The config module contains constants pertaining to configuration of
pysiriproxy.

'''
from os import environ
from sys import version
from os.path import dirname, join, sep


class _Directory(str):
    '''The _Directory class extends the string class to encapsulate the concept
    of a directory. In addition, this class provides a function for retrieving
    a file located within the current directory.

    '''

    def getFile(self, filename):
        '''Return the _Directory object found by joining this _Directory
        with the given filename.

        * filename -- The filename

        '''
        return _Directory(join(self, filename))


class Directories:
    '''The Directories class contains various properties which define
    directories that contain pysiriproxy data.

    '''
    Home = _Directory(environ.get("HOME"))
    '''The Home property contains the user's home directory.'''

    Config = Home.getFile(".pysiriproxy")
    '''The Config directory contains the user's siri proxy configuration
    directory.

    '''

    Etc = _Directory(join("/", "etc"))
    '''The Etc property contains the path to the system etc directory.'''

    Scripts = Config.getFile("scripts")
    '''The Scripts property contains the scripts directory within the user's
    siri proxy configuration directory.

    '''

    # Get the path of this file, and pop up two directories to reach the
    # top level directory for pysiriproxy
    SiriInstall = _Directory(join("/", *(dirname(__file__).split(sep))[:-2]))
    '''The SiriInstall property contains the system installation directory
    for pysiriproxy.

    '''

    SystemDefaultConfig = join(SiriInstall, "pysiriproxy", "config")
    '''The SystemDefaultConfig property contains the path to the system
    directory which contains the default configuration files created when
    pysiriproxy is installed on the system.

    '''


class Files:
    '''The Files class contains definitions of various file paths that pertain
    to pysiriproxy configuration.
    
    '''

    GenCerts = join(Directories.Scripts, "gen_certs.sh")
    '''The GenCerts property contains the path to the bash script that
    generates certificates for pysiriproxy.

    '''

    ConfigFile = join(Directories.Config, "pysiriproxy.cfg")
    '''The ConfigFile property contains the path to the configuration file for
    pysiriproxy.

    '''

    CertFile = join(Directories.Config, "server.passless.crt")
    '''The CertFile property contains the path to the certification file for
    pysiriproxy.

    '''

    EtcHosts = join(Directories.Etc, "hosts")
    '''The EtcHosts property contains the path to the system hosts file.'''

    LogFile = join(Directories.Config, "pysiriproxy.log")
    '''The LogFile property contains the path to the log file to use for
    pysiriproxy.

    '''

    KeyFile = join(Directories.Config, "server.passless.key")
    '''The KeyFile property contains the path to the key file to use for
    pysiriproxy.

    '''


class Ids:
    '''The Ids class defines various configuration settings.

    .. note:: :mod:`ConfigParser` converts all properties to lower case

    '''

    CertFile = "certfile"
    '''The name of the configuration property that stores the certification
    file.

    '''

    DebugLevel = "debuglevel"
    '''The name of the configuration property that stores the debug level for
    the system.

    '''

    ErrorResponse = "error"
    '''The name of the configuration property that stores the string which
    Siri will respond with in the event that an Exception is encountered while
    processing an object filter, or a speech rule.

    '''

    ExitOnConnectionLost = "exitonconnectionlost"
    '''The name of the configuration property that determines whether the
    server application will exit in the event that the connection to the
    iPhone is lost. This will allow an external script to restart the
    server cleanly each time the connection is lost.

    '''

    GenCerts = "gencerts"
    '''The name of the command line property that determines if the SSL
    certificates should be generated.

    '''

    Host = "host"
    '''The name of the configuration property that stores a particular host
    name.

    '''

    IOsVersion = "ios"
    '''The name of the configuration property that stores the version of iOS
    that pysiriproxy should be configured for.

    '''

    KeyFile = "keyfile"
    '''The name of the configuration property that stores the path to the key
    file to use for the system.

    '''

    LogFile = "logFile"
    '''The name of the configuration property that stores the path to the log
    file to use for the system.

    '''

    LogLevel = "loglevel"
    '''The name of the configuration property that stores the log level to use
    for the system.

    '''

    PluginsDir = "pluginsdir"
    '''The name of the configuration property that stores the path to the
    directory containing the plugin scripts.

    '''

    Port = "port"
    '''The name of the configuration property that stores the port number
    to use.

    '''

    Timestamp = "timestamp"
    '''The name of the configuration property that stores the boolean
    indicating whether logged messages should be timestamped or not.

    '''

class Sections:
    '''The Sections class defines the names of the sections that can be
    used within the configuration file.

    '''
    Debug = "Debug"
    '''The section containing debugging configuration settings.'''

    General = "General"
    '''The section containing general configuration settings.'''

    Server = "Server"
    '''The section containing settings pertaining to Apple's web server.'''

    iPhone = "iPhone"
    '''The section containing settings pertaining to the iPhone connection.'''

    Logging = "Logging"
    '''The section containing settings pertaining to logging the system.'''

    Responses = "Responses"
    '''The section containing settings pertaining to creating responses.'''



class Vars:
    '''Define various variables that can be used within the
    configuration file.

    .. note:: Variables should be all caps

    '''
    Config = "PYSIRIPROXY"
    '''The name of the variable which stores the path to the configuration
    file.

    '''

    Home = "HOME"
    '''The name of the variable which stores the path to the user's home
    directory.

    '''
