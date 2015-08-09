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
import logging


class Instruments:
    def __init__(self, instrument_xml_file):
        '''
        Initialise Instruments Class
        :param instrument_xml_file: include the relative path in relationship to this module
        and instrument xml file name.
        :return: object instance.
        '''
        logger = logging.getLogger('xml_utilities.Instruments')
        # Create an xml dom object for Instruments XML.
        try:
            # The tree root is the top level Instruments tag.
            self.xmldom = eTree.parse(instrument_xml_file)  # Open and parse xml document.
        except FileNotFoundError:
            raise FileNotFoundError(instrument_xml_file)
            logger.debug('XML File not found : %s' % instrument_xml_file)
        else:
            logger.debug('XML File found : %s' % instrument_xml_file)

    def get_names(self):
        '''
        Gets a list of instrument names from instruments.xml
        :return: list of names.
        :raises: AttributeError or IndexError
        '''

        logger = logging.getLogger('xml_utilities.Instruments.get_names')

        tmp_names = []
        for instrument in self.xmldom.findall('Instrument'):
            logger.debug('Instrument Name Object at : %s' % str(instrument))

            name = instrument.findtext('Name')
            logger.debug('Instrument Name Object Name : %s' % instrument.findtext('Name'))

            if name is None:
                raise AttributeError('INVALID_XML')
            else:
                tmp_names.append(name)
                logger.debug('Appending Instrument Name to return list : %s' % name)

        if len(tmp_names) == 0:
            raise IndexError('INVALID_XML')
        else:
            return tmp_names

    def get_filename(self, instrument_name):
        '''
        get the xml file name for the instrument name supplied.
        :param instrument_name:
        :return: xml file name excluding path (string)
        :raises: AttributeError
        '''

        logger = logging.getLogger('xml_utilities.Instruments.get_filename')

        logger.debug('Instrument Name : %s' % instrument_name)

        for instrument in self.xmldom.findall('Instrument'):

            logger.debug('Instrument Object at : %s' % str(instrument))
            logger.debug('Instrument Object Name : %s' % instrument.findtext('Name'))

            if instrument.findtext('Name') == instrument_name:
                return_name = instrument.findtext('File')
                logger.debug('Instrument Filename : %s' % return_name)

        if return_name is None:
            raise AttributeError('Instrument XML file not found.')
        else:
            return return_name


