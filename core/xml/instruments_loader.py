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

import logging
import sys

import xml.etree.ElementTree as eTree

import core.utilities.utilities as utils


class Instruments:
    def __init__(self):
        self.logger = logging.getLogger('core.xmlLoad.Instruments')

        # Create an xml dom object for Instruments XML.
        try:

            # The tree root is the top level Instruments tag.
            self.xmldom = eTree.parse('instruments/instruments.xml')  # Open and parse xml document.
            self.logger.debug('Created XML Dom for Instruments.')

        except FileNotFoundError:

            self.logger.critical("Fatal Error - instruments.xml missing.")
            utils.exit_message('instruments.xml missing.')

        if sys.platform.startswith('win32'):
            self.sep = '\\'
        else:
            self.sep = '/'

    def get_names(self):
        '''
        Gets a list of instrument names from instruments.xml
        :return: list of names.
        '''
        tmp_names = []
        for instrument in self.xmldom.findall('Instrument'):
            name = instrument.findtext('Name')
            self.logger.debug('%s %s', 'Appending instrument to list', name)
            tmp_names.append(name)

        self.logger.debug('%s %s', 'Returning list', str(tmp_names))
        return tmp_names

    def get_file(self, instrument_name):
        '''
        get the xml file name for the instrument name supplied.
        :param instrument_name:
        :return: xml file name including path (string)
        '''

        for instrument in self.xmldom.findall('Instrument'):
            if instrument.findtext('Name') == instrument_name:
                return_name = 'instruments' + self.sep + instrument.findtext('File')
                self.logger.debug('%s %s', 'Instrument XML file and path', return_name)
                return return_name


