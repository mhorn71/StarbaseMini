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
            print('Instruments Name : ' + name)
    except AttributeError as msg:
        print('Instruments Name Attribute Error : ' + str(msg))
    except IndexError as msg:
        print('Instruments Name Index Error : ' + str(msg))
    else:
        try:
            filename = instruments_xml.get_file(instruments_xml.get_names()[0])
            print('Filename for Instruments at index 0 : ' + filename)
        except AttributeError as msg:
            print('Instruments Filename Attribute Error : ' + str(msg))
        finally:
            print('----------------------------------------------------')

try:
    filename = '..' + os.path.sep + 'instruments' + os.path.sep + filename
    instrument = xml_utilities.instrument_loader.Instrument(filename)
except FileNotFoundError:
    print('File Not Found : %s' % filename)
except LookupError as msg:
    print('Look up error : %s' % str(msg))
except ValueError as msg:
    print('Value Error : %s' % str(msg))
else:
    print('Instrument Attributes :')
    print('Instrument Identifier : %s' % instrument.instrument_identifier)
    print('Instrument Description : %s' % instrument.instrument_description)
    print('Instrument Staribus Address : %s' % instrument.instrument_staribus_address)
    print('Instrument Starinet Address : %s' % instrument.instrument_starinet_address)
    print('Instrument Starinet Port : %s' % instrument.instrument_starinet_port)
    print('Instrument Number of Channel : %s' % instrument.instrument_number_of_channels)
    print('----------------------------------------------------')
    print('Channel Names list :')
    print(instrument.channel_names)
    print('Channel Colours list :')
    print(instrument.channel_colours)
    print('----------------------------------------------------')
    print('Chart Attributes :')
    print('Y Axis Label : %s' % instrument.YaxisLabel)
    print('Y Axis Range : %s' % instrument.YaxisRange)
    print('Y Axis Scale : %s' % instrument.YaxisScale)
    print('----------------------------------------------------')
    print('Boolean Attributes :')
    print('Boolean True : %s' % instrument.boolean_true)
    print('Boolean False : %s' % instrument.boolean_false)
    print('----------------------------------------------------')
    print('Module list :')
    print(instrument.module_list)
    print('----------------------------------------------------')
    print('Command list :')
    print(instrument.command_list)
    print('----------------------------------------------------')

    base = instrument.module_list[0][2]

    i = instrument.command_list[0][0]

    CB = instrument.command_dict[i][base]['Base']
    CC = instrument.command_dict[i][base]['Code']
    CV = instrument.command_dict[i][base]['Variant']
    DESC = instrument.command_dict[i][base]['Description']
    STP = instrument.command_dict[i][base]['SendToPort']
    BLK = instrument.command_dict[i][base]['BlockedData']
    STC = instrument.command_dict[i][base]['SteppedData']
    PCH = instrument.command_dict[i][base]['Parameters']['Choices']
    PRX = instrument.command_dict[i][base]['Parameters']['Regex']
    PTT = instrument.command_dict[i][base]['Parameters']['Tooltip']
    RDT = instrument.command_dict[i][base]['Response']['DataType']
    RUT = instrument.command_dict[i][base]['Response']['Units']
    RRX = instrument.command_dict[i][base]['Response']['Regex']

    print('Command Name : %s' % i)
    print('Command Base : %s' % CB)
    print('Command Code : %s' % CC)
    print('Command Variant : %s' % CV)
    print('Command Description : %s' % DESC)
    print('Command Send To Port : %s' % STP)
    print('Command Blocked Data : %s' % BLK)
    print('Command Stepped Data : %s' % STC)
    print('\tParameter :')
    print('\t\t\tChoices : %s' % PCH)
    print('\t\t\tRegex : %s' % PRX)
    print('\t\t\tTooltip : %s' % PTT)
    print('\tResponse :')
    print('\t\t\tDataType : %s' % RDT)
    print('\t\t\tUnit : %s' % RUT)
    print('\t\t\tRegex : %s' % RRX)
