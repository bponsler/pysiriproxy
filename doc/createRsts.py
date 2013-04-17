#!/usr/bin/python2.6
# Copyright 2012 Brett Ponsler
# This file is part of pyamp.
#
# pyamp is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# pyamp is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with pyamp.  If not, see <http://www.gnu.org/licenses/>.
'''The createRsts script generated all the reStructured text files for
the current project.

'''
from pyamp.documentation import generateAllRsts


# The name of the project
_PROJECT_NAME = "pysiriproxy"

# The list of module names that should never be generated
_IGNORED_MODULES = ["speechRules", "objectClasses"]


if __name__ == '__main__':
    # Generate all of the RST files
    generateAllRsts(_PROJECT_NAME, _IGNORED_MODULES)
