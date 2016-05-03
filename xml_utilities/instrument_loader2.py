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

import constants

logger = logging.getLogger('xml_utilities.Instrument')


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

                instrument_staribus_type: str
                instrument_staribus_port: str
                instrument_staribus_baudrate: str
                instrument_staribus_timeout: str
                instrument_staribus_autodetect: str

                instrument_number_of_channels: str

                module_list: ['Module Identifier', 'Description', 'Module CB']

                command_list: ['Command Identifier, 'Description', 'Command Code']

                command_dict: {plugin_cmdbase: {command_code: {
                                                 'Identifier': command_ident,
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
                                                              'Regex': response_regex}}}}

                channel_names: list
                channel_colours: list
                channel_datatypename: list
                channel_units: list

                YaxisLabel:str
                YaxisRange:str
                YaxisScale:str
                XaxisLabel:str

        :raises:    LookupError
                    ValueError
                    FileNotFoundError
        '''

        # xmldom
        self.xmldom = None

        # The plugin module list
        self.module_list = []

        # The command list
        self.command_list = []

        # The command dictionary
        self.command_dict = {}

        # The metadata channel list see below for format etc ...
        self.channel_names = []

        # The metadata channel colour list
        self.channel_colours = []

        # The metadata channel data type name list
        self.channel_datatypenames = []

        # The metadata channel units list
        self.channel_units = []
        
        # The chart metadata attributes
        self.YaxisLabel = 'None'
        self.YaxisRange = 'None'
        self.YaxisScale = 'None'
        self.XaxisLabel = 'None'

        # Attributes, I've used a None string here as we use the None in the XML as well so using a str means I can
        # lose the None type test.
        self.instrument_identifier = 'None'
        self.instrument_description = 'None'
        self.instrument_staribus_address = 'None'
        self.instrument_starinet_address = 'None'
        self.instrument_starinet_port = 'None'
        self.instrument_staribus_type = 'None'
        self.instrument_staribus_port = 'None'
        self.instrument_staribus_baudrate = 'None'
        self.instrument_staribus_timeout = 'None'
        self.instrument_staribus_autodetect = 'None'
        self.instrument_number_of_channels = 'None'
        self.instrument_datatranslator = 'None'

    def clear_instrument(self):
        del self.module_list[:]
        del self.command_list[:]
        del self.channel_names[:]
        del self.channel_colours[:]
        del self.channel_datatypenames[:]
        del self.channel_units[:]

        self.command_dict.clear()

        self.YaxisLabel = 'None'
        self.YaxisRange = 'None'
        self.YaxisScale = 'None'
        self.XaxisLabel = 'None'

        self.instrument_identifier = 'None'
        self.instrument_description = 'None'
        self.instrument_staribus_address = 'None'
        self.instrument_starinet_address = 'None'
        self.instrument_starinet_port = 'None'
        self.instrument_staribus_type = 'None'
        self.instrument_staribus_port = 'None'
        self.instrument_staribus_baudrate = 'None'
        self.instrument_staribus_timeout = 'None'
        self.instrument_staribus_autodetect = 'None'
        self.instrument_number_of_channels = 'None'
        self.instrument_datatranslator = 'None'

    def load_xml(self, xml_file):

        # Create an xml dom object for the Instrument XML.
        try:
            # The tree root is the top level Instrument tag.
            self.xmldom = eTree.parse(xml_file)  # Open and parse xml document.
        except FileNotFoundError as msg:
            logger.critical('Instrument XML not Found : %s' % str(msg))
            raise FileNotFoundError('Instrument XML not found.')
        else:
            logger.debug('Instrument XML Found.')

        # Try and get the instrument XML header information.
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

            self.instrument_staribus_type = self.xmldom.findtext('StaribusPortType')
            logger.debug('Instrument staribus port type : %s' % self.instrument_staribus_type)

            self.instrument_staribus_port = self.xmldom.findtext('StaribusPort')
            logger.debug('Instrument staribus port : %s' % self.instrument_staribus_port)

            self.instrument_staribus_baudrate = self.xmldom.findtext('StaribusPortBaudrate')
            logger.debug('Instrument staribus port baudrate : %s' % self.instrument_staribus_baudrate)

            self.instrument_staribus_timeout = self.xmldom.findtext('StaribusPortTimeout')
            logger.debug('Instrument staribus port timeout : %s' % self.instrument_staribus_timeout)

            self.instrument_staribus_autodetect = self.xmldom.findtext('StaribusPortAutodetect')
            logger.debug('Instrument staribus port autodetect : %s' % self.instrument_staribus_autodetect)

            self.instrument_number_of_channels = self.xmldom.findtext('NumberOfChannels')
            logger.debug('Instrument number of channels : %s' % self.instrument_number_of_channels)

            self.instrument_datatranslator = self.xmldom.findtext('DataTranslator')
            logger.debug('Instrument data translator : %s' % self.instrument_datatranslator)

        except IndexError as msg:
            logger.critical('INVALID_XML Header IndexError : %s' % str(msg))
            raise LookupError('INVALID_XML : Unable to parse XML header')
        except AttributeError as msg:
            logger.critical('INVALID_XML Header AttributeError : %s' % str(msg))
            raise LookupError('INVALID_XML : Unable to parse XML header')
        else:
            # Now check the header XML makes sense before we move onto the command and chart keys.

            # Check instrument indentifier is set and valid.

            if self.instrument_identifier == 'None':
                logger.critical('INVALID_XML : Instrument Identifier is None!')
                raise LookupError('INVALID_XML : Instrument Identifier is None!')
            elif len(self.instrument_identifier) == 0:
                logger.critical('INVALID_XML : Instrument Identifier is zero length!')
                raise LookupError('INVALID_XML : Instrument Identifier is zero length!')

            # Check instrument description.

            if self.instrument_description == 'None':
                logger.warn('Instrument description set to None defaulting to NODATA')
                self.instrument_description = 'NODATA'
            elif len(self.instrument_description) == 0:
                logger.warn('Instrument description zero length defaulting to NODATA')
                self.instrument_description = 'NODATA'

            # Check Staribus Address, if zero it's Starinet otherwise it should be Staribus.
            # Staribus range 1 - 253 else out of range.

            if 0 < int(self.instrument_staribus_address) <= 253:
                logger.info('Instrument address appears to be Staribus')
                instrument = 'staribus'
            elif int(self.instrument_staribus_address) == 0:
                logger.info('Instrument address appears to be Starinet')
                instrument = 'starinet'
            else:
                raise ValueError('INVALID_XML : Starbus Address out of range %s' % self.instrument_staribus_address)

            # Check attributes for either Staribus or Starinet make sense overall

            if instrument == 'staribus':
                if self.instrument_starinet_address != 'None':
                    logger.critical('Staribus instrument address but Starinet address is not None')
                    raise ValueError('INVALID_XML : Staribus instrument address but Starinet address is not None')

                if self.instrument_starinet_port != 'None':
                    logger.critical('Staribus instrument address but Starinet port is not None')
                    raise ValueError('INVALID_XML : Staribus instrument address but Starinet port is not None')

                if not re.match('^RS232$|^RS485$', self.instrument_staribus_type):
                    logger.critical('Staribus port type not RS232 or RS485')
                    raise ValueError('INVALID_XML : Staribus port type not RS232 or RS485')

                if not re.match(constants.staribus_port, self.instrument_staribus_port):
                    logger.critical('Staribus port not valid')
                    raise ValueError('INVALID_XML : Staribus port not valid')

                if not re.match(constants.staribus_baudrate, self.instrument_staribus_baudrate):
                    logger.critical('Staribus baudrate not within range')
                    raise ValueError('INVALID_XML : Staribus baudrate not within range')

                if not re.match('^True$|^False$',  self.instrument_staribus_autodetect):
                    logger.critical('Staribus autodetect not True or False.')
                    raise ValueError('INVALID_XML : Staribus autodetect not True or False')

            if instrument == 'starinet':

                if self.instrument_staribus_type != 'None':
                    logger.critical('Starinet instrument address but Staribus port type not None')
                    raise ValueError('INVALID_XML : Starinet instrument but Staribus port type not None')

                if self.instrument_staribus_port != 'None':
                    logger.critical('Starinet instrument address but Staribus port is not None')
                    raise ValueError('INVALID_XML : Starinet instrument address but Staribus port is not None')

                if self.instrument_staribus_baudrate != 'None':
                    logger.critical('Starinet instrument address but Staribus baudrate is not None')
                    raise ValueError('INVALID_XML : Starinet instrument address but Staribus baudrate is not None')

                if self.instrument_staribus_autodetect != 'None':
                    logger.critical('Starinet instrument but Staribus autodetect is not None')
                    raise ValueError('INVALID_XML : Staribus autodetect not True or False')

                if not re.match(constants.starinet_ip, self.instrument_starinet_address):
                    logger.critical('Starinet instrument IP address not valid')
                    raise ValueError('INVALID_XML : Starinet instrument IP address not valid')

                if not re.match(constants.starinet_port, self.instrument_starinet_port):
                    logger.critical('Starinet instrument network port not valid')
                    raise ValueError('INVALID_XML : Starinet instrument network port not valid')

            # Check datatranslator is valid
            if not re.match(constants.datatranslator, self.instrument_datatranslator):
                logger.critical('Data Translator invalid')
                raise ValueError('INVALID_XML : Data Translator invalid')

            # Check that staribus timeout is valid
            if not re.match('^20|30|40|50|60$', self.instrument_staribus_timeout):
                logger.critical('Staribus timeout invalid')
                raise ValueError('INVALID_XML : Staribus timeout invalid')

            # Check the number of channels is between 2 - 9
            if not re.match('^[2-9]$', self.instrument_number_of_channels):
                logger.critical('Number of channels out of bounds, invalid')
                raise ValueError('INVALID_XML : Number of channels out of bounds, invalid')

            # Now we'll attempt to parse the chart metadata keys and values.
            try:
                chart_metadata_dom = self.xmldom.find('ChartMetadata')
    
                logger.debug('Found ChartMetadata Object : %s' % str(chart_metadata_dom))
    
                self.YaxisLabel = chart_metadata_dom.findtext('YaxisLabel')
                logger.debug('YaxisLabel : %s' % self.YaxisLabel)
                
                self.YaxisRange = chart_metadata_dom.findtext('YaxisRange')
                logger.debug('YaxisRange : %s' % self.YaxisRange)
                
                self.YaxisScale = chart_metadata_dom.findtext('YaxisScale')
                logger.debug('YaxisScale : %s' % self.YaxisScale)
                
                self.XaxisLabel = chart_metadata_dom.findtext('XaxisLabel')
                logger.debug('XaxisLabel : %s' % self.XaxisLabel)
            except IndexError as msg:
                logger.critical('INVALID_XML Chart metadata IndexError : %s' % str(msg))
                raise LookupError('INVALID_XML : Unable to parse chart metadata')
            except AttributeError as msg:
                logger.critical('INVALID_XML Chart metadata AttributeError : %s' % str(msg))
                raise LookupError('INVALID_XML : Unable to parse chart metadata')
            else:

                # Now attempt to see if we have valid data.

                if not re.match('^Lin$|^Log$', self.YaxisScale):
                    logger.critical('Y axis scale invalid')
                    raise ValueError('INVALID_XML : Y axis scale invalid')
                
                if self.YaxisLabel == 'None' or len(self.YaxisLabel) == 0:
                    self.YaxisLabel = 'NODATA'
                    
                if self.XaxisLabel == 'None' or len(self.XaxisLabel) == 0:
                    self.XaxisLabel = 'NODATA'

                if not re.match('^[0-9]*,([0-9]*)$', self.YaxisRange):
                    self.YaxisRange = None
                elif self.YaxisRange == 'None' or len(self.YaxisRange) == 0:
                    logger.critical('Y axis range invalid')
                    raise ValueError('INVALID_XML : Y axis range invalid')

            # Now we'll attempt to parse the channel metadata keys and values.
            # Channel item trip counter, we use this to compare to number of channels.

            channel_item_count = 0

            try:
                for channel_metadata in self.xmldom.findall('ChannelMetadata'):
                    logger.debug('Found ChannelMetadata Object %s' % str(channel_metadata))
                    self.channel_names.append(channel_metadata.findtext('ChannelLabel'))
                    logger.debug(
                        'Channel Label %s added to channel_names list.' % channel_metadata.findtext('ChannelLabel'))
                    self.channel_colours.append(channel_metadata.findtext('ChannelColour'))
                    logger.debug(
                        'Channel Colour %s added to channel_colour list.' % channel_metadata.findtext('ChannelColour'))
                    self.channel_datatypenames.append(channel_metadata.findtext('ChannelDataTypeName'))
                    logger.debug(
                        'Channel DataTypeName %s added to channel_datatypenames list.' % channel_metadata.findtext(
                            'ChannelDataTypeName'))
                    self.channel_units.append(channel_metadata.findtext('ChannelUnit'))
                    logger.debug(
                        'Channel Unit %s added to channel_units list.' % channel_metadata.findtext('ChannelUnit'))

                    channel_item_count += 1
                    
            except IndexError as msg:
                logger.critical('INVALID_XML Channel metadata IndexError : %s' % str(msg))
                raise LookupError('INVALID_XML : Unable to parse channel metadata')
            except AttributeError as msg:
                logger.critical('INVALID_XML Channel metadata AttributeError : %s' % str(msg))
                raise LookupError('INVALID_XML : Unable to parse channel metadata')
            else:

                # First check the amount of ChannelMetadata keys matches the Number of Channels.

                if int(self.instrument_number_of_channels) != channel_item_count:
                    logger.critical('INVALID_XML : Number to ChannelMetadata keys does not match NumberOfChannels')
                    raise LookupError('INVALID_XML : Number to ChannelMetadata keys does not match NumberOfChannels')

                # Check the channel colours are in hex

                for channel_colour in self.channel_colours:
                    if not re.match(constants.channel_hex_color, channel_colour):
                        logger.critical('INVALID_XML : Channel colour is not in hex')
                        raise LookupError(
                            'INVALID_XML : Channel colour is not in hex')

                # Now we finally attempt to populate the command dictionary.

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

                        self.command_dict.setdefault(plugin_cmdbase, []).append({command_code: {
                            'Identifier': command_ident,
                            'Variant': command_variant,
                            'Description': command_desc,
                            'SendToPort': command_stp,
                            'BlockedData': command_blocked,
                            'SteppedData': command_stepped,
                            'Parameters': {'Choices': parameter_choices,
                                           'Regex': parameter_regex,
                                           'Tooltip': parameter_tooltip},
                            'Response': {
                                'DataTypeName': response_datatype,
                                'Units': response_units,
                                'Regex': response_regex}}})

                        logger.debug('Appending to tmp_command list %s' % command_ident)
                        tmp_command.append([command_ident, command_desc, command_code])

                    logger.debug('Appending tmp_command list to command_list : %s' % str(tmp_command))
                    self.command_list.append(tmp_command)