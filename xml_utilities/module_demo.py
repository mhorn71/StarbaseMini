__author__ = 'mark'
# StarbaseMini Staribus/Starinet Client for the British Astronomical Association Staribus Protocol
# Copyright (C) 2015  Mark Horn
#
# This file is part of StarbaseMini.
#
# StarbaseMini is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#
# StarbaseMini is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with StarbaseMini.  If not, see <http://www.gnu.org/licenses/>.

import os

import xml_utilities

# Instruments Demo.

try:
    instruments_xml = xml_utilities.Instruments('..' + os.path.sep + 'instruments' + os.path.sep + 'instruments.xml')
except FileNotFoundError as msg:
    print('File Not Found : ' + str(msg))
else:
    try:
        for name in instruments_xml.get_names():
            print('Instrument Name : ' + name)
    except AttributeError as msg:
        print('Instrument Name Attribute Error : ' + str(msg))
    except IndexError as msg:
        print('Instrumet Name Index Error : ' + str(msg))
    else:
        try:
            filename = instruments_xml.get_file(instruments_xml.get_names()[0])
            print('Filename for Instrument at index 0 : ' + filename)
        except AttributeError as msg:
            print('Filename Attribute Error : ' + str(msg))


