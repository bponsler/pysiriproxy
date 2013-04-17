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
'''The options module contains the Options class which provides the
ability to load settings from the pysiriproxy configuration file, as as
being able to parse the command line arguments.

'''
from pysiriproxy.options.config import Directories, Files, Ids, Sections, Vars

from pyamp.logging import Colors, LogData, LogLevel
from pyamp.config import conversions, OptionsParser, Option, ClOption, \
    ClBoolOption


###########################################################
# @todo: It would be pretty awesome to provide two things:
# @todo: A GUI dialog for updating/changing settings, and
# @todo: A web interface for updating/changing settings
###########################################################


class Values:
    '''The Values class contains definitions of values that are used for
    certain command line arguments, or configuration properties.

    '''

    IOs5 = "ios5"
    '''Configure for iOS version 5.'''

    IOs6 = "ios6"
    '''Configure for iOS version 6.'''

    IOs5Server = "guzzoni.apple.com"
    '''The server for iOS 5.'''

    IOs6Server = "kryten.apple.com"
    '''The server for iOS 6.'''


class Settings:
    '''The Settings class defines all of the specific configuration settings
    that can be used in the pysiriproxy configuration file.

    '''

    CertFile = Option(Ids.CertFile, defaultValue=Files.CertFile,
                      typeFn=conversions.string)
    '''This setting should contain the path to the file that is used as
    the certification file for connecting to the Apple's server.

    '''

    DebugLevel = Option(Ids.DebugLevel)
    '''This setting should contain the debug level which will be used by the
    system.

    '''

    ErrorResponse = Option(Ids.ErrorResponse, typeFn=conversions.string)
    '''This setting should contain a string that will be spoken by Siri in
    the event of an Exception while objects are being filtered or speech rules
    are being applied.

    '''

    ExitOnConnectionLost = Option(Ids.ExitOnConnectionLost,
                                  defaultValue=False,
                                  typeFn=conversions.boolean)
    '''This setting should contain be set to True in order to configure the
    server such that it exits every time an established connection to the
    iPhone is lost. This will allow an external script to restart the server
    cleanly each time the connection is lost.

    '''
    
    GenCerts = ClBoolOption(Ids.GenCerts, defaultValue=False,
                            helpText="Generate a certificate for the " \
                                "iPhone for a specific version of iOS. " \
                                "Either iOS5, or iOS6.")
    '''This setting should contain a boolean indicating whether the pysiriproxy
    SSL certificates should be generated or not.

    '''

    ServerHost = Option(Ids.Host, defaultValue=Values.IOs5Server,
                        typeFn=conversions.string)
    '''This setting should contain the host name of the Apple's server.
    Defaults to the iOS 5 server.

    '''

    ServerPort = Option(Ids.Port, defaultValue=443, typeFn=int)
    '''This setting should contain the port number used for connecting to
    Apple's web server.

    '''

    iPhonePort = Option(Ids.Port, defaultValue=443, typeFn=int)
    '''This setting should contain the port number that the iPhone uses
    for its connection.

    '''

    KeyFile = Option(Ids.KeyFile, defaultValue=Files.KeyFile,
                     typeFn=conversions.string)
    '''The setting should contain the path to the file that is used as
    the key file for connecting to the Apple's server.

    '''

    LogFile = ClOption(Ids.LogFile, defaultValue=Files.LogFile,
                       optionType="string")
    '''This setting should contain the path to the log file where pysiriproxy
    should log all of its logging messages.

    '''

    LogLevel = Option(Ids.LogLevel, typeFn=conversions.logLevel)
    '''This setting should contain the log level which will used by the system.

    Here are valid values for this setting:

        * DEBUG,
        * INFO,
        * WARN, and
        * ERROR

    '''

    PluginsDir = Option(Ids.PluginsDir, typeFn=conversions.string)
    '''This setting should contain the path to the system directory that
    contains the plugins which pysiriproxy should load.

    '''

    Timestamp = Option(Ids.Timestamp, typeFn=conversions.string)
    '''This setting should contain a string which is the format for the
    timestamp which will be applied to all logged messages. See the man
    page for the date command for more info on the format. If this is
    an empty string, no timestamp will be applied to logged messages.

    '''


class Options(OptionsParser):
    '''The Options class is responsible for parsing command line and
    configuration file options and providing the ability to get the value of
    a given option.

    '''

    # Implement the borg pattern
    __shared_state = {}

    # Define all of the usable configuration variables
    Variables = {
        Vars.Home: Directories.Home,
        Vars.Config: Directories.Config,
        }
    '''Define the dictionary of variables that can be used in the pysiriproxy
    configuration file.

    These variables can be used by adding a dollar sign before the variable
    name in the configuration file. These variables will be replaced in the
    configuration file prior to parsing it.

    Example::

        # If the following setting is configured in the configuration file,
        # the $HOME variable would be replaced by the user's home directory
        # prior to parsing the configuration file
        RandomSetting = $HOME/Documents

    '''

    Options = {
        Sections.General: [
            Settings.PluginsDir,
            ],
        Sections.Debug: [
            Settings.ExitOnConnectionLost,
            ],
        Sections.Server: [
            Settings.ServerHost,
            Settings.ServerPort,
            ],
        Sections.iPhone: [
            Settings.KeyFile,
            Settings.CertFile,
            Settings.iPhonePort,
            ],
        Sections.Logging: [
            Settings.LogLevel,
            Settings.DebugLevel,
            Settings.LogFile,
            Settings.Timestamp,
            ],
        Sections.Responses: [
            Settings.ErrorResponse,
            ],
        }
    '''Define the dictionary of possible configuration section names mapped to
    the list of configuration options available for that section.

    '''

    ClOptions = [
        Settings.GenCerts,
        ]
    '''Define the list of all of the options which are configurable only via
    the command line.

    '''
