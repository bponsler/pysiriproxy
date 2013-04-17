# Copyright 2012 Brett Ponsler
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
'''

'''
from pysiriproxy.constants import DirectionTypes
from pysiriproxy.plugins import BasePlugin, matches, regex
from pysiriproxy.objects import ObjectFactory, Buttons, DataObjects


class Plugin(BasePlugin):
    '''The LocationTest plugin.

    This plugin demonstrates how to create and use map locations with Siri.

    '''
    name = "LocationTest"

    # Define a dictionary mapping custom command names, to the plugin
    # function names that are called when the command is executed
    customCommandMap = {
        }

    ##### Define the speech rules for this plugin #####

    @matches("Create map location")
    def locationTest(self, _text):
        '''This is an example of a speech rule which triggers when
        the user says "Create map location ".

        This example demonstrates how create and display a specific
        map location to the Siri user.

        * _text -- The text spoken by the user

        '''
        # Create the two web search buttons to display to the user
        locations = [
            ("Apple HQ", ObjectFactory.location(street="1 Infinite Loop",
                                                city="Cupertino",
                                                stateCode="CA",
                                                countryCode="US",
                                                postalCode="95014")),
            ("Orlando", ObjectFactory.location(city="Olando", stateCode="FL",
                                               countryCode="US")),
            ]
        mapItem = ObjectFactory.mapItem(locations)

        # Create a view to display the utterance and the buttons
        self.makeView([mapItem])
        self.completeRequest()

    @matches("Create directions")
    def directionsTest(self, _text):
        '''Test creating directions between two locations.

        Note: Currently directions only work between two locations that
              are given the latitude and longitude coordinates.

        '''
        appleHq = ObjectFactory.location(latitude=37.331414,
                                         longitude=-122.030566)
        appleHq = DataObjects.create(DataObjects.MapItem,
                                     label="Apple HQ", location=appleHq)

        googleHq = ObjectFactory.location(street="1600 Amphitheatre Parkway",
                                          city="Mountain View", stateCode="CA",
                                          countryCode="US", postalCode="94043",
                                          latitude=37.422131,
                                          longitude=-122.083911)
        googleHq = DataObjects.create(DataObjects.MapItem, label="Google HQ",
                                      location=googleHq)

        # Note: Showing directions completes the request
        self.showDrivingDirections(appleHq, googleHq)
