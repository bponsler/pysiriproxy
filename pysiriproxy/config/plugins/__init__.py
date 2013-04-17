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
'''The plugins directory contains all of the system accessible plugins
for the pysiriproxy program.

In order for pysiriproxy to properly locate a plugin the following must
be true:

    1) The plugin script name must have the .py extension,
    2) The plugin script name must not start with '__',
    3) The plugin script must be located within the plugins directory,
    4) The plugin script must contain a class named Plugin, and
    5) The Plugin class must subclass the 'BasePlugin' class.

'''
