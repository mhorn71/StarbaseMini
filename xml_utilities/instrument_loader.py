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

# import logging
import xml.etree.ElementTree as eTree
import re

import utilities


class Instrument:
    def __init__(self, xml_file):
        '''
        Parses the instrument XMl to provide module and command lists, commands are also converted to dictionary.

        :param xml_file: must include path relative to this module.

        :return:
                instrument_identifier: str
                instrument_description: str
                instrument_staribus_address: str
                instrument_starinet_address: str
                instrument_starinet_port: str
                instrument_number_of_channels: str

                module_list: ['Module Identifier', 'Description', 'Module CB'
                command_list: ['Command Identifier, 'Description', 'Command Code']
                command_dict: {command_ident: {'Base': plugin_cmdbase,
                                                 'Code': command_code,
                                                 'Variant': command_variant,
                                                 'Description': command_desc,
                                                 'SendToPort': command_stp,
                                                 'BlockedData': command_blocked,
                                                 'SteppedData': command_stepped,
                                                 'Parameters': {'Choices': parameter_choices,
                                                                'Regex': parameter_regex,
                                                                'Tooltip': parameter_tooltip},
                                                 'Response': {'DataType': response_datatype,
                                                              'Units': response_units,
                                                              'Regex': response_regex}}}

                channel_names: list
                channel_colours: list
                YaxisLabel:str
                YaxisRange:str
                YaxisScale:str
                XaxisLabel:str
                boolean_true: str
                boolean_false: str

        :raises:    LookupError
                    ValueError
                    FileNotFoundError
        '''

        # The instrument module and command list see below for format etc ...
        # self.instrument_mc_list = []

        # The plugin module list
        self.module_list = []

        # The command list
        self.command_list = []

        # The command dictionary
        self.command_dict = {}

        # Create an xml dom object for the Instrument XML.
        try:
            # The tree root is the top level Instrument tag.
            self.xmldom = eTree.parse(xml_file)  # Open and parse xml document.
        except FileNotFoundError:
            raise FileNotFoundError('Fatal Error - Missing Instrument XML.')

        # Get Instrument Attributes, there can be multiple instruments in Starbase however StarbaseMini will only read
        # the primary Instrument Tag, index 0.

        try:

            self.instrument_identifier = self.xmldom.findtext('Identifier')

            self.instrument_description = self.xmldom.findtext('Description')

            self.instrument_staribus_address = self.xmldom.findtext('StaribusAddress')

            self.instrument_starinet_address = self.xmldom.findtext('StarinetAddress')

            self.instrument_starinet_port = self.xmldom.findtext('StarinetPort')

            # Check that either StaribusAddress and StarinetAddress aren't both set if they are exit.
            if self.instrument_starinet_address != 'None' and self.instrument_staribus_address != 'None':

                raise LookupError('Instrument XML has both Staribus and Starinet Defined. Please fix before running '
                                  'software.')

            elif self.instrument_starinet_address == 'None' and self.instrument_staribus_address == 'None':

                raise ValueError('Instrument XML has neither Staribus nor Starinet Defined.'
                                 ' Please fix before running software.')

            # Check that we have both Starinet Address and Starinet Port set.
            if self.instrument_starinet_address != 'None' and self.instrument_starinet_port == 'None':

                raise ValueError('Starinet port not set set.')

            elif self.instrument_starinet_address == 'None' and self.instrument_starinet_port != 'None':

                raise ValueError('Starinet address not set.')

            if self.instrument_starinet_address != 'None':
                # Check for valid IPv4 Address.
                if utilities.check_ip(self.instrument_starinet_address):
                    # Check port is at least a number.
                    if utilities.check_starinet_port(self.instrument_starinet_port):
                        pass
                    else:
                        raise ValueError('Starinet port %s out of range.' % self.instrument_starinet_port)
                else:
                    raise ValueError('Unable to parse Starinet address  %s' % self.instrument_starinet_address)

            elif self.instrument_staribus_address != 'None':
                # Check Staribus Address is in range (001 - 254)
                if utilities.check_staribus_address(self.instrument_staribus_address):
                    pass
                else:
                    raise ValueError('Starbus Address out of range (001 - 255) currently set to %s' %
                                     self.instrument_staribus_address)

            self.instrument_number_of_channels = self.xmldom.findtext('NumberOfChannels')

            # Add regex check of for Number of Channels (int 2 - 9)
            if re.match('^[2-9]$', self.instrument_number_of_channels):
                pass
            else:
                raise ValueError('Number of Channels out of range = %s' % self.instrument_number_of_channels)

        except IndexError:
            raise LookupError('Fatal Error - Unable to parse XML')
        except AttributeError:
            raise LookupError('Fatal Error - Unable to parse XML')

        # First check we have plugins.
        core_match = False
        if len(self.xmldom.findall('Plugin')) == 0:
            raise LookupError('Instrument plugins missing.')
        else:
            # Next check the core plugin exists if not exit.
            for plugin in self.xmldom.iter('Plugin'):
                if re.match('^[Cc]ore$', plugin.findtext('Identifier')):
                    core_match = True

            if core_match:
                pass
            else:
                raise LookupError('Core plugin is missing!!')

        for plugin in self.xmldom.iter('Plugin'):

            plugin_ident = plugin.findtext('Identifier')

            plugin_desc = plugin.findtext('Description')

            plugin_cmdbase = plugin.findtext('CommandCodeBase')

            self.module_list.append([plugin_ident, plugin_desc, plugin_cmdbase])

            # The below bit needs changing to a dict which would make more sense.
            # This will also break the ui loader.

            tmp_command = []

            for command in plugin.iter('Command'):

                command_ident = command.findtext('Identifier')

                command_code = command.findtext('CommandCode')

                command_variant = command.findtext('CommandVariant')

                command_desc = command.findtext('Description')

                command_stp = command.findtext('SendToPort')

                command_blocked = command.findtext('BlockedDataCommand')

                command_stepped = command.findtext('SteppedDataCommand')

                for parameter in command.iter('Parameter'):
                    parameter_choices = parameter.findtext('Choices')

                    parameter_regex = parameter.findtext('Regex')

                    parameter_tooltip = parameter.findtext('Tooltip')

                for response in command.iter('Response'):

                    response_datatype = response.findtext('DataTypeName')

                    response_units = response.findtext('Units')

                    response_regex = response.findtext('Regex')

                self.command_dict.update({command_ident: {'Base': plugin_cmdbase,
                                                 'Code': command_code,
                                                 'Variant': command_variant,
                                                 'Description': command_desc,
                                                 'SendToPort': command_stp,
                                                 'BlockedData': command_blocked,
                                                 'SteppedData': command_stepped,
                                                 'Parameters': {'Choices': parameter_choices,
                                                                'Regex': parameter_regex,
                                                                'Tooltip': parameter_tooltip},
                                                 'Response': {'DataType': response_datatype,
                                                              'Units': response_units,
                                                              'Regex': response_regex}}})

                tmp_command.append(command_ident)

            self.command_list.append(tmp_command)

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
