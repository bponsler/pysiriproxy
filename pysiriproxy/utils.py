# Copyright (C) (c) 2012 Brett Ponsler, Pete Lamonica, Pete Lamonica
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
'''The utils module contains utility functions used throughout
the system.

'''

def characterToHex(character): 
    '''Convert a single character to hexadecimal.

    * character -- The character to convert to hexadecimal

    ''' 
    return hex(ord(character)).split('x')[1].rjust(2, '0') 


def toHex(string, separator=" "):
    '''Convert a string to hexadecimal.

    * string -- The string to convert to hexadecimal
    * seperator -- The seperator to use between each character

    '''
    return separator.join(map(characterToHex, string))
