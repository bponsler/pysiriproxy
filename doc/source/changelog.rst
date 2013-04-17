================================================================================
Changelog
================================================================================

The following page describes all of the changes that were made for specific
versions of pysiriproxy.

----------------------------------------
Release 0.0.8
----------------------------------------

1. Added key for theatricalReleaseDate to the list of keys pertaining to Dates.
   This was causing movie requests to fail.

----------------------------------------
Release 0.0.7
----------------------------------------

1. Created a configuration section called 'Debug'. This section contains a
   single configuration property called 'ExitOnConnectionLost' which, when
   set to True, forces the pysiriproxy server to exit completely when an
   established connection to the iPhone is lost. This allows an external script
   to monitor the server and restart it when it crashes allowing the
   connections to be cleanly re-established.

2. Catching and handling the StopIteration exception which is raised when a
   speech rule function uses some form of 'yield' such that the yield is
   sometimes not called. Since yield is not called the generator is empty
   and throws the StopIteration exception when next() is called.

3. Updated the UnicodeItems list in the plist module to include the 'Title'
   key. This fixed the 'Cancel Alarm' request. The response (list of
   alarms) contained unicode data in the 'Title' entry and thus caused the
   iPhone to crash when it was displayed. This fixes that issue.

4. Merged iOS 6 bug fix from SiriProxy into our branch. This handles a new
   type of packet used to clear the context which is similar to a Ping or
   Pong message.

5. Fixed issue 10. When an unknown packet was encountered it was trying to
   convert the packet to a hexadecimal string, however, the function did
   not exist and thus caused an exception.

6. Added version key ('v') to all returned objects. Currently set to a
   constant value of '2.0' which can be configured in the SiriObject class.

7. Removed all instances of Guzzoni within the code when refering to Apple's
   web server by name. This is due to the fact that, as of iOS 6, there is
   another web server (kryten.apple.com) which means referring to the
   server as 'Guzzoni' is both confusing and incorrect.

8. Using the hostname base (e.g., Kryten for kryten.apple.com, or Guzzoni
   for guzzoni.apple.com) as the name of the Server connection class. This
   string will appear in all data logged by this class making it clear
   which of Apple's servers is actually being used during testing.

----------------------------------------
Release 0.0.6
----------------------------------------

1. Fixed bug with conversion from Python dictionary into a plist object.
   Currently there is an issue with the text to speech (tts) tags causing
   the iPhone to crash when sent to the phone (the hex characters in the
   tags are not being properly handled at this point in time). The current
   solution is to remove tts tags from the dictionary entries that contain
   tts tags. There was a bug in the previous version that only removed the
   first tts tag -- rather than all of them. With this update all of the
   tts tags are removed from the strings. This should fix queries such as
   "What time is it in New York?".

2. The server has been updated to better handle dates. In the previous version
   the server was replacing any time related dictionary entry with the current
   date and time of the server. The server has been updated to try to convert
   the time values given (number of seconds since the epoch) into the correct
   date. When doing this it seemed that the resulting date was usually thirty
   one years in the past from its actual date. The current solution (read:
   hack) is to simply add thirty one years to the resulting date. This seems
   to have worked for almost all of my tests, but I have noticed that it
   resulted in Siri speaking a date that was one day before the correct date
   (which was being displayed on the phone). This requires further
   investigation.

3. The Python object dictionaries that are recieved from the iPhone and the
   Guzzoni server often contain entries that have hexadecimal values within
   the strings. Sending these strings to the iPhone typically results in the
   iPhone crashing and rebooting. The current solution is to replace the
   common hexadecimal values in the strings with their ascii equivalent.
   The speakableSelectionResponse and selectionResponse keys sometimes
   contain hexadecimal values, but were not being replaced. This update
   makes sure to replace the hexadecimal characters in these entries as
   well. This fixes queries that involve button presses to disambiguate
   a specific query.

4. Added instructions to the online documentation for configuring
   pysiriproxy to use the iOS 6 server (kryten.apple.com).

5. Updated gen_certs.sh to take a "-v" argument which allows the user to
   specify the version of iOS the generated certificate should support.
   The default is for the certificate to support ``*.apple.com`` which will 
   support both iOS 5 and iOS 6.
   
   Example usage: ./gen_certs.sh -v iOS6

6. Updated the setDnsmasq.sh script to add dnsmasq support for both the
   guzzoni and kryten webservers (which are iOS 5 and iOS 6 servers
   respectively). This allows the server to accept connections from
   iPhones with either version without being re-configured.

7. Updated the default pysiriproxy.cfg file to connect to the
   iOS 6 server at kryten.apple.com rather than the iOS 5 server
   at guzzoni.apple.com.

8. Updated the utf module to support replacing the hexadecimal
   characters representing a degree symbol. Currently the hex
   characters will be replaced by the string " degrees" which
   is semantically the same string.

9. Updated the setup.py script to add setup dependencies for specific
   version of: biplist, twisted, and pyamp. This should allow the
   setup script to handle downloading and installing the necessary
   versions of each of these modules.

10. Fixed the installation setup procedure. The previous version had an
    error due to the update to using setuptools rather than disttools.
    The default configuration files were no longer located in the
    expected directory and thus could not be copied to the user's
    home configuration directory. This has been fixed in this version.

11. Updated the documentation to explain modifications to support
    using iOS 5 and iOS 6 versions.

12. Created the **Timestamp** configuration property under the
    Logging section. This variable contains the format string which
    will be used to apply a date to all logged messages.

    Example format: "%Y-%m-%d" yields 2012-08-04

    For more details on the format string see the man page for the
    date command. No timestamp will be applied to logged messages 
    if this property is an empty string.

13. Moved config folder and files underneath the pysiriproxy source
    directory so that the setup script can include them automatically.
    Setuptools provides the ability to install any SVN controlled
    data files it finds with one line. This removed some unnecessary
    code in the setup script.

14. Added step to install python*-dev to the installation
    instructions for twisted. Without this easy_install fails to
    install twisted.

15. Fixed bug with converting specific object keys to unicode. In
    previous versions this was not functioning correctly, and thus
    text to speech (TTS) tags would cause the iPhone to crash. Now
    the strings are being converted to unicode properly which allows
    the TTS tags to function as expected. These strings no longer
    need to have special hexadecimal characters replaced either.

----------------------------------------
Release 0.0.5
----------------------------------------

1. Using StringIO to send a string containing plist data to CFPropertyList
   instead of writing a file and deleting the file afterward.

----------------------------------------
Release 0.0.4
----------------------------------------

1. Using the biplist module to convert plist objects created by
   CFPropertyList into binary plists. The previous method was to call the
   external plutil Perl script. This was reported as causing significant
   delays (0.5 to 1.5 seconds) while running pysiriproxy on an iPhone. This
   change solves that issue by doing the conversion in Python rather than
   using the Perl script.

2. Updated setup.py script to allow distributions to be created and uploaded
   to the Python Package Index.

3. Updated the documentation to include installation instructions for biplist,
   and for using setuptools to install pysiriproxy.

----------------------------------------
Release 0.0.3
----------------------------------------

1. The connection to the Guzzoni web server is now tied to the iPhone
   connection. The Guzzoni connection is only established once the iPhone
   connection is finished, and both are closed when the iPhone connection
   is lost. This resolves an issue where the server was no longer usable
   after a long period of inactivity -- the Guzzoni connection was closed
   and not being re-established.
2. Added the ability to create map locations and send them to the iPhone
   user so that they are displayed in a list of locations.
3. Added the ability to send directions between two locations to the
   iPhone user which are displayed in the map. The directions can be:
   walking, driving, or public transportation directions.
4. Created a new plugin to demonstrate how to create locations and
   directions.

----------------------------------------
Release 0.0.2
----------------------------------------

1. Documentation updated to fix small mistakes in installation instructions on
   Ubuntu 11.10, and 12.04.
2. The siriproxy script has been made executable to persist through the SVN
   checkout.
3. Added documentation on the changes made to each version of pysiriproxy.
4. Fixed issue with sequential requests not working. The new requests were
   blocked by the previously matched plugin causing the Siri button to continuously
   spin. Now the context is reset on a request completed message (which should
   be sent at the completion of all Plugins). This keeps new requests from being
   blocked, and allows Siri to properly respond to a series of questions.

----------------------------------------
Release 0.0.1
----------------------------------------

Initial release of pysiriproxy.
