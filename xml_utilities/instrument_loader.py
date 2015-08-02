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
import xml.etree.ElementTree as eTree
import re

import core.utilities.utilities as utils


class Instrument:
    def __init__(self, xml_file):


        self.logger = logging.getLogger('core.xmlLoad.Instrument')

        # The instrument module and command list see below for format etc ...
        self.instrument_mc_list = []

        # Create an xml dom object for the Instrument XML.
        try:

            # The tree root is the top level Instrument tag.
            self.xmldom = eTree.parse(xml_file)  # Open and parse xml document.
            self.logger.debug('Created XML Dom for Instrument.')

        except FileNotFoundError:

            self.logger.critical("Fatal Error - Missing Instrument XML.")
            utils.exit_message('Missing Instrument XML.')

        # Get Instrument Attributes, there can be multiple instruments in Starbase however StarbaseMini will only read
        # the primary Instrument Tag, index 0.

        try:

            self.instrument_identifier = self.xmldom.findtext('Identifier')
            self.logger.debug('Instrument Identifier = %s' % self.instrument_identifier)

            self.instrument_description = self.xmldom.findtext('Description')
            self.logger.debug('Instrument Description = %s' % self.instrument_description)

            self.instrument_staribus_address = self.xmldom.findtext('StaribusAddress')
            self.logger.info('Instrument Staribus Address = %s' % self.instrument_staribus_address)

            self.instrument_starinet_address = self.xmldom.findtext('StarinetAddress')
            self.logger.info('Instrument Starinet Address = %s' % self.instrument_starinet_address)

            self.instrument_starinet_port = self.xmldom.findtext('StarinetPort')
            self.logger.info('Instrument Starinet Port = %s' % self.instrument_starinet_port)

            # Check that either StaribusAddress and StarinetAddress aren't both set if they are exit.
            if self.instrument_starinet_address != 'None' and self.instrument_staribus_address != 'None':

                self.logger.critical('Instrument XML has both Staribus and Starinet Defined. Please fix before running '
                                     'software.')
                utils.exit_message('Both Starinet Address and Staribus Addresses set.')

            elif self.instrument_starinet_address == 'None' and self.instrument_staribus_address == 'None':

                self.logger.critical('Instrument XML has neither Staribus nor Starinet Defined.'
                                     ' Please fix before running software.')
                utils.exit_message('Neither Starinet Address nor Staribus Addresses set.')

            # Check that we have both Starinet Address and Starinet Port set.
            if self.instrument_starinet_address != 'None' and self.instrument_starinet_port == 'None':

                self.logger.critical('Neither Staribus nor Starinet address set.')
                utils.exit_message('Starinet Address defined but no Staribus Port set.')

            elif self.instrument_starinet_address == 'None' and self.instrument_starinet_port != 'None':

                self.logger.critical('Starinet Port defined but no Staribus Addresses set.')
                utils.exit_message('Starinet Port defined but no Staribus Addresses set.')

            if self.instrument_starinet_address != 'None':
                # Check for valid IPv4 Address.
                if utils.ip_checker(self.instrument_starinet_address):
                    # Check port is at least a number.
                    if utils.port_checker(self.instrument_starinet_port):

                        pass

                    else:

                        self.logger.critical('Unable to parse Starinet Port - %s', self.instrument_starinet_port)
                        utils.exit_message('Starinet Port out of range.')

                else:

                    self.logger.critical('Unable to parse Starinet Address - %s', self.instrument_starinet_address)
                    utils.exit_message('Starinet IP not in IPv4 format.')

            elif self.instrument_staribus_address != 'None':
                # Check Staribus Address is in range (001 - 254)
                if re.match('^([01][0-9][0-9]|2[0-4][0-9]|25[0-4])$', self.instrument_staribus_address):

                    if re.match('^000$', self.instrument_staribus_address):

                        self.logger.critical('Starbus Address out of range (001 - 255) currently set to %s',
                                             self.instrument_staribus_address)
                        utils.exit_message('Staribus Address out of range.')

                    else:
                        pass
                else:

                    self.logger.critical('Starbus Address out of range (001 - 255) currently set to %s',
                                         self.instrument_staribus_address)
                    utils.exit_message('Staribus Address out of range.')

            self.instrument_number_of_channels = self.xmldom.findtext('NumberOfChannels')
            self.logger.debug('Instrument Number of Channels = %s' % self.instrument_number_of_channels)

            # Add regex check of for Number of Channels (int 2 - 9)
            if re.match('^[2-9]$', self.instrument_number_of_channels):
                pass
            else:
                self.logger.critical('Number of Channels out of range = %s' % self.instrument_number_of_channels)
                utils.exit_message('Number of Channels out of range.')

        except IndexError:

            self.logger.critical("Fatal Error - Unable to parse XML")
            utils.exit_message('Missing Instrument XML Header.')

        except AttributeError:

            self.logger.critical("Unable to parse XML")
            utils.exit_message('Missing Instrument XML Attribute.')

        # First check we have plugins.
        if len(self.xmldom.findall('Plugin')) == 0:

            self.logger.critical('Instrument plugins missing.')
            utils.exit_message('Instrument plugins missing.')

        else:
            # Next check the core plugin exists if not exit.
            for plugin in self.xmldom.iter('Plugin'):

                if re.match('^[Cc]ore$', plugin.findtext('Identifier')):
                    core_match = True

            if core_match:
                pass
            else:
                self.logger.critical('Core plugin must be present in Instrument XML')
                utils.exit_message('Core plugin must be present in Instrument XML')

        for plugin in self.xmldom.iter('Plugin'):

            tmp_plugin = []

            plugin_ident = plugin.findtext('Identifier')
            self.logger.debug('Found plugin %s' % plugin_ident)
            plugin_desc = plugin.findtext('Description')
            self.logger.debug('Plugin description %s' % plugin_desc)
            plugin_cmdbase = plugin.findtext('CommandCodeBase')
            self.logger.debug('Plugin command code base %s' % plugin_cmdbase)

            tmp_plugin.append(plugin_ident)
            tmp_plugin.append(plugin_desc)
            tmp_plugin.append(plugin_cmdbase)

            self.logger.debug('Searching for plugin commands.')

            # The below bit needs changing to a dict which would make more sense.
            # This will also break the ui loader.

            for command in plugin.iter('Command'):

                tmp_command = []

                command_ident = command.findtext('Identifier')
                self.logger.debug('Found command %s' % command_ident)
                command_code = command.findtext('CommandCode')
                self.logger.debug('Command code %s' % command_code)
                command_variant = command.findtext('CommandVariant')
                self.logger.debug('Command variant %s' % command_variant)
                command_desc = command.findtext('Description')
                self.logger.debug('Command description %s' % command_desc)
                command_stp = command.findtext('SendToPort')
                self.logger.debug('Command send to port %s' % command_stp)
                command_blocked = command.findtext('BlockedDataCommand')
                self.logger.debug('Command blocked data command %s' % command_blocked)
                command_stepped = command.findtext('SteppedDataCommand')
                self.logger.debug('Command stepped data command %s' % command_stepped)

                tmp_command.append(command_ident)
                tmp_command.append(command_code)
                tmp_command.append(command_variant)
                tmp_command.append(command_desc)
                tmp_command.append(command_stp)
                tmp_command.append(command_blocked)
                tmp_command.append(command_stepped)

                for parameter in command.iter('Parameter'):
                    parameter_choices = parameter.findtext('Choices')
                    self.logger.debug('Command parameter choices %s' % parameter_choices)
                    parameter_regex = parameter.findtext('Regex')
                    self.logger.debug('Command parameter regex %s' % parameter_regex)
                    parameter_tooltip = parameter.findtext('Tooltip')
                    self.logger.debug('Command parameter tooltip %s' % parameter_tooltip)

                    tmp_command.append(parameter_choices)
                    tmp_command.append(parameter_regex)
                    tmp_command.append(parameter_tooltip)

                for response in command.iter('Response'):

                    response_datatype = response.findtext('DataTypeName')
                    self.logger.debug('Command response data type name %s' % response_datatype)
                    response_units = response.findtext('Units')
                    self.logger.debug('Command response units %s' % response_units)
                    response_regex = response.findtext('Regex')
                    self.logger.debug('Command response regex %s' % response_regex)

                    tmp_command.append(response_datatype)
                    tmp_command.append(response_units)
                    tmp_command.append(response_regex)

                self.logger.debug('Appending command to plugin list.')
                self.logger.debug('------')
                tmp_plugin.append(tmp_command)

            self.instrument_mc_list.append(tmp_plugin)

        # This bit was for testing but I'll leave it here as a reference.

        # print('Number of plugins %s' % len(self.instrument_mc_list))
        #
        # for i in range(len(self.instrument_mc_list)):  # For each plugin.
        #     print('\nPlugin ident %s' % self.instrument_mc_list[i][0])
        #     print('Plugin desc %s' % self.instrument_mc_list[i][1])
        #     print('Plugin CB %s' % self.instrument_mc_list[i][2])
        #
        #     # next iter over the commands.
        #     command_list_length = len(self.instrument_mc_list[i])
        #
        #     for n in range(3, command_list_length):  # Commands start after the first 4 items.
        #         print('\nCommand ident %s' % self.instrument_mc_list[i][n][0])
        #         print('Command CC %s' % self.instrument_mc_list[i][n][1])
        #         print('Command CV %s' % self.instrument_mc_list[i][n][2])
        #         print('Command desc %s' % self.instrument_mc_list[i][n][3])
        #         print('Command stp %s' % self.instrument_mc_list[i][n][4])
        #         print('Command blkCmd %s' % self.instrument_mc_list[i][n][5])
        #         print('Command stpCmd %s' % self.instrument_mc_list[i][n][6])
        #         print('Parameter Choices %s' % self.instrument_mc_list[i][n][7])
        #         print('Parameter Regex %s' % self.instrument_mc_list[i][n][8])
        #         print('Parameter Tooltip %s' % self.instrument_mc_list[i][n][9])
        #         print('Response DataTypeName %s' % self.instrument_mc_list[i][n][10])
        #         print('Response Units %s' % self.instrument_mc_list[i][n][11])
        #         print('Response Regex %s' % self.instrument_mc_list[i][n][12])

        # The metadata channel list see below for format etc ...
        self.channel_names = []

        # The metadata channel colour list
        self.channel_colours = []

        chart_metadata_dom = self.xmldom.find('ChartMetadata')

        self.YaxisLabel = chart_metadata_dom.findtext('YaxisLabel')
        self.YaxisRange = chart_metadata_dom.findtext('YaxisRange')
        self.YaxisScale = chart_metadata_dom.findtext('YaxisScale')
        self.XaxisLabel = chart_metadata_dom.findtext('XaxisLabel')

        for channel_metadata in self.xmldom.findall('ChannelMetadata'):
            self.channel_names.append(channel_metadata.findtext('ChannelLabel'))
            self.channel_colours.append(channel_metadata.findtext('ChannelColour'))

        Boolean = self.xmldom.find('BooleanMetadata')

        self.boolean_true = Boolean.findtext('True')
        self.boolean_false = Boolean.findtext('False')
