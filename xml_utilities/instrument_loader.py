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
                channel_datatypename: list
                channel_units: list
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

        logger = logging.getLogger('xml_utilities.Instrument')

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
        except FileNotFoundError as msg:
            logger.critical('Instrument XML not Found : %s' % str(msg))
            raise FileNotFoundError('Instrument XML not found.')
        else:
            logger.debug('Instrument XML Found.')

        # Get Instrument Attributes, there can be multiple instruments in Starbase however StarbaseMini will only read
        # the primary Instrument Tag, index 0.

        try:

            self.instrument_identifier = self.xmldom.findtext('Identifier')
            logger.debug('Instrument identifier : %s' % self.instrument_identifier)

            self.instrument_description = self.xmldom.findtext('Description')
            logger.debug('Instrument description : %s' % self.instrument_description)

            self.instrument_staribus_address = self.xmldom.findtext('StaribusAddress')
            logger.debug('Instrument staribus address : %s' % self.instrument_staribus_address)

            self.instrument_starinet_address = self.xmldom.findtext('StarinetAddress')
            logger.debug('Instrument starinet address : %s' % self.instrument_starinet_address)

            self.instrument_starinet_port = self.xmldom.findtext('StarinetPort')
            logger.debug('Instrument starinet network port : %s' % self.instrument_starinet_port)

            self.instrument_datatranslator = self.xmldom.findtext('DataTranslator')
            logger.debug('Instrument data translator : %s' % self.instrument_datatranslator)

            # Check that we have both Starinet Address and Starinet Port set.
            if self.instrument_starinet_address != 'None' and self.instrument_starinet_port == 'None':
                logger.critical('INVALID_XML : Starinet port not set set.')
                raise ValueError('INVALID_XML : Starinet port not set set.')

            elif self.instrument_starinet_address == 'None' and self.instrument_starinet_port != 'None':
                logger.critical('INVALID_XML : Starinet address not set.')
                raise ValueError('INVALID_XML : Starinet address not set.')

            if self.instrument_starinet_address != 'None':
                logger.debug('Starinet address is not None.')
                # If we have a Starinet address then the Staribus Address must be 000
                if self.instrument_staribus_address != '000':
                    logger.critical('INVALID_XML : Starbus Address out of range for Starinet instrument, should be'
                                    ' 000 currently set to %s' % self.instrument_staribus_address)
                    raise ValueError('INVALID_XML : Starbus Address out of range for Starinet instrument, should be'
                                     ' 000 currently set to %s' % self.instrument_staribus_address)
                else:
                    logger.debug('Staribus address correct for Starinet instrument : 000')

                # Check for valid IPv4 Address.
                logger.debug('Checking starinet IPv4 address.')
                if utilities.check_ip(self.instrument_starinet_address):
                    # Check port is at least a number.
                    if utilities.check_starinet_port(self.instrument_starinet_port):
                        logger.debug('Starinet port is True.')
                    else:
                        logger.critical('INVALID_XML : Starinet port %s out of range.' % self.instrument_starinet_port)
                        raise ValueError('INVALID_XML : Starinet port %s out of range.' % self.instrument_starinet_port)
                else:
                    logger.critical('INVALID_XML : Unable to parse Starinet address  %s' %
                                    self.instrument_starinet_address)
                    raise ValueError('INVALID_XML : Unable to parse Starinet address  %s' %
                                     self.instrument_starinet_address)

            elif self.instrument_staribus_address != 'None' and self.instrument_starinet_address == 'None':
                # Check Staribus Address is in range (001 - 253)
                if utilities.check_staribus_address(self.instrument_staribus_address):
                    pass
                else:
                    logger.critical('INVALID_XML : Starbus Address out of range (001 - 253) currently set to %s' %
                                    self.instrument_staribus_address)
                    raise ValueError('INVALID_XML : Starbus Address out of range (001 - 253) currently set to %s' %
                                     self.instrument_staribus_address)

            self.instrument_number_of_channels = self.xmldom.findtext('NumberOfChannels')
            logger.debug('Instrument number of channels : %s' % self.instrument_number_of_channels)

            # Add regex check of for Number of Channels (int 2 - 9)
            if re.match('^[2-9]$', self.instrument_number_of_channels):
                logger.debug('Instrument number of channels with range.')
            else:
                logger.critical('INVALID_XML : Number of Channels out of range = %s' %
                                 self.instrument_number_of_channels)
                raise ValueError('INVALID_XML : Number of Channels out of range = %s' %
                                 self.instrument_number_of_channels)

        except IndexError as msg:
            logger.critical('INVALID_XML IndexError : %s' % str(msg))
            raise LookupError('INVALID_XML : Unable to parse XML')
        except AttributeError as msg:
            logger.critical('INVALID_XML AttributeError : %s' % str(msg))
            raise LookupError('INVALID_XML : Unable to parse XML')

        # First check we have plugins.
        logger.debug('Checking we have plugin and one of them is the Core plugin.')
        core_match = False
        if len(self.xmldom.findall('Plugin')) == 0:
            logger.critical('INVALID_XML : Instrument plugins missing.')
            raise LookupError('INVALID_XML : Instrument plugins missing.')
        else:
            # Next check the core plugin exists if not exit.
            for plugin in self.xmldom.iter('Plugin'):
                logger.debug('Checking if plugin : %s is Core.' % str(plugin))
                if re.match('^[Cc]ore$', plugin.findtext('Identifier')):
                    logger.debug('Core plugin found.')
                    core_match = True

            if core_match:
                pass
            else:
                logger.critical('INVALID_XML : Core plugin is missing!!')
                raise LookupError('INVALID_XML : Core plugin is missing!!')

        logger.debug('Iterating though plugins and appending data to lists')
        for plugin in self.xmldom.iter('Plugin'):
            logger.debug('Found Plugin Object : %s' % str(plugin))

            plugin_ident = plugin.findtext('Identifier')
            logger.debug('Plugin identifier : %s' % plugin_ident)

            plugin_desc = plugin.findtext('Description')
            logger.debug('Plugin description : %s' % plugin_desc)

            plugin_cmdbase = plugin.findtext('CommandCodeBase')
            logger.debug('Plugin command code base : %s' % str(plugin_cmdbase))

            logger.debug('Plugin appending ident, desc, CB to module_list')
            self.module_list.append([plugin_ident, plugin_desc, plugin_cmdbase])

            tmp_command = []

            logger.debug('Iterating though plugin commands adding to command_list and command_dict')
            for command in plugin.iter('Command'):

                command_ident = command.findtext('Identifier')
                logger.debug('Command identifier : %s' % command_ident)

                command_code = command.findtext('CommandCode')
                logger.debug('Command code : %s' % command_code)

                command_variant = command.findtext('CommandVariant')
                logger.debug('Command variant : %s' % command_variant)

                command_desc = command.findtext('Description')
                logger.debug('Command description : %s' % command_desc)

                command_stp = command.findtext('SendToPort')
                logger.debug('Command send to port : %s' % command_stp)

                command_blocked = command.findtext('BlockedDataCommand')
                logger.debug('Command - blocked command : %s' % str(command_blocked))

                command_stepped = command.findtext('SteppedDataCommand')
                logger.debug('Command - stepped command : %s' % str(command_stepped))

                logger.debug('Iterating over command parameter.')
                for parameter in command.iter('Parameter'):
                    parameter_choices = parameter.findtext('Choices')
                    logger.debug('Command parameter choices : %s' % parameter_choices)

                    parameter_regex = parameter.findtext('Regex')
                    logger.debug('Command parameter regex : %s' % parameter_regex)

                    parameter_tooltip = parameter.findtext('Tooltip')
                    logger.debug('Command parameter tooltip : %s' % parameter_tooltip)

                logger.debug('Iterating over command response')
                for response in command.iter('Response'):

                    response_datatype = response.findtext('DataTypeName')
                    logger.debug('Command response data type name : %s' % response_datatype)

                    response_units = response.findtext('Units')
                    logger.debug('Command response units : %s' % response_units)

                    response_regex = response.findtext('Regex')
                    logger.debug('Command response regex : %s' % response_regex)

                # This won't work for multiple parameters so needs a rewrite at some point.

                logger.debug('Adding command to command_dict')
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
                                                          'Response': {'DataTypeName': response_datatype,
                                                                       'Units': response_units,
                                                                       'Regex': response_regex}}})
                logger.debug('Appending to tmp_command list %s' % command_ident)
                tmp_command.append(command_ident)

            logger.debug('Appending tmp_command list to command_list : %s' % str(tmp_command))
            self.command_list.append(tmp_command)

        # The metadata channel list see below for format etc ...
        self.channel_names = []

        # The metadata channel colour list
        self.channel_colours = []

        # The metadata channel data type name list
        self.channel_datatypenames = []

        # The metadata channel units list
        self.channel_units = []

        chart_metadata_dom = self.xmldom.find('ChartMetadata')

        logger.debug('Found ChartMetadata Object : %s' % str(chart_metadata_dom))

        self.YaxisLabel = chart_metadata_dom.findtext('YaxisLabel')
        logger.debug('YaxisLabel : %s' % self.YaxisLabel)
        self.YaxisRange = chart_metadata_dom.findtext('YaxisRange')
        logger.debug('YaxisRange : %s' % self.YaxisRange)
        self.YaxisScale = chart_metadata_dom.findtext('YaxisScale')
        logger.debug('YaxisScale : %s' % self.YaxisScale)
        self.XaxisLabel = chart_metadata_dom.findtext('XaxisLabel')
        logger.debug('XaxisScale : %s' % self.XaxisLabel)

        logger.debug('Iterating of channel metadata adding channel labels and colours to respective lists.')
        for channel_metadata in self.xmldom.findall('ChannelMetadata'):
            logger.debug('Found ChannelMetadata Object %s' % str(channel_metadata))
            self.channel_names.append(channel_metadata.findtext('ChannelLabel'))
            logger.debug('Channel Label %s added to channel_names list.' % channel_metadata.findtext('ChannelLabel'))
            self.channel_colours.append(channel_metadata.findtext('ChannelColour'))
            logger.debug('Channel Colour %s added to channel_colour list.' % channel_metadata.findtext('ChannelColour'))
            self.channel_datatypenames.append(channel_metadata.findtext('ChannelDataTypeName'))
            logger.debug('Channel DataTypeName %s added to channel_datatypenames list.' % channel_metadata.findtext('ChannelDataTypeName'))
            self.channel_datatypenames.append(channel_metadata.findtext('ChannelDataTypeName'))
            logger.debug('Channel DataTypeName %s added to channel_datatypenames list.' % channel_metadata.findtext('ChannelDataTypeName'))

        Boolean = self.xmldom.find('BooleanMetadata')
        logger.debug('Found BooleanMetadata Object : %s' % str(Boolean))

        self.boolean_true = Boolean.findtext('True')
        logger.debug('Boolean True set to : %s' % self.boolean_true)
        self.boolean_false = Boolean.findtext('False')
        logger.debug('Boolean False set to : %s' % self.boolean_false)

        logger.debug('Instrument XML Loaded completed.')
