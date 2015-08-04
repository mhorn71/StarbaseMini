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

import xml.etree.ElementTree as eTree


class Instruments:
    def __init__(self, instrument_xml_file):
        '''
        Initialise Instruments Class
        :param instrument_xml_file: include the relative path in relationship to this module
        and instrument xml file name.
        :return: object instance.
        '''
        # Create an xml dom object for Instruments XML.
        try:
            # The tree root is the top level Instruments tag.
            self.xmldom = eTree.parse(instrument_xml_file)  # Open and parse xml document.
        except FileNotFoundError:
            raise FileNotFoundError(instrument_xml_file)

    def get_names(self):
        '''
        Gets a list of instrument names from instruments.xml
        :return: list of names.
        :raises: AttributeError or IndexError
        '''
        tmp_names = []
        for instrument in self.xmldom.findall('Instrument'):
            name = instrument.findtext('Name')

            if name is None:
                raise AttributeError('Name tag missing.')
            else:
                tmp_names.append(name)

        if len(tmp_names) == 0:
            raise IndexError('No names to return.')
        else:
            return tmp_names

    def get_filename(self, instrument_name):
        '''
        get the xml file name for the instrument name supplied.
        :param instrument_name:
        :return: xml file name excluding path (string)
        :raises: AttributeError
        '''

        for instrument in self.xmldom.findall('Instrument'):

            if instrument.findtext('Name') == instrument_name:
                return_name = instrument.findtext('File')
            else:
                raise AttributeError('Instrument not found.')

            if return_name is None:
                raise AttributeError('Instrument XML file not found.')
            else:
                return return_name


