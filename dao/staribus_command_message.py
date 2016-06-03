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
# along with StarbaseMini.  If not, see <http:#www.gnu.org/licenses/>.

import logging

import utilities
import constants

# look at Starbase StaribusCommandMessage.java

# **************************************************************************************************
#     Request with no parameters, length 15 before EOT
# 
#     Header          STX
#     Address         char char  in Hex
#     CommandCode     char char char char
#     CommandVariant  char char char char
#     CrcChecksum     char char char char  in Hex
#     Terminator      EOT CR LF
# 
# **************************************************************************************************
#     Request with Parameters
# 
#     Header          STX
#     Address         char char  in Hex
#     CommandCode     char char char char
#     CommandVariant  char char char char
#     Separator       US
#     Parameters      char char {char char ..} US          parameter 0
#                     char char {char char ..} US          parameter 1
#     CrcChecksum     char char char char  in Hex
#     Terminator      EOT CR LF
# 
# ***************************************************************************************************
# StaribusCommandMessage.


class StaribusCommandMessage:
    def __init__(self):
        logger = logging.getLogger('dao.StaribusCommandMessage.init')

        logger.debug('StaribusCommandMessage initialised')

    def construct(self, addr, base, code, variant, param):
        '''
        Construct staribus message string.
        :param addr: Instrument Address.
        :param base: Command Code Base.
        :param code: Command Code.
        :param variant: Command Variant.
        :param param: Command Parameter.
        :return: Return a single constructed staribus message string including control characters.
        '''

        logger = logging.getLogger('dao.StaribusCommandMessage.construct')

        # Convert staribus address to hexbyte.
        logger.debug('Message instrument address passed range check.')

        # covert string to hex base 16 and make sure length is two chars long padd with leading zero if not.
        addr = hex(int(addr)).split('x')[1].upper().zfill(2)

        logger.debug('Message instrument address converted to hexbyte : %s' % addr)

        # The base and code are a hex byte and must be in the range 0x00 - 0xFF
        # so we'll use the check_staribus address to confirm they're in range.

        if utilities.check_hexbyte_string(base) is not True:

            logger.warning('HexByte string check failed for base : %s' % base)

            return 'MALFORMED_MESSAGE'

        if utilities.check_hexbyte_string(code) is not True:

            logger.warning('HexByte string check failed for code : %s' % code)

            return 'MALFORMED_MESSAGE'

        # Check the command variant is within in range for hex word 0x0000 - 0xFFFF
        if utilities.check_hexword_string(variant) is not True:

            logger.warning('HexByte string check failed for variant : %s' % variant)

            return 'MALFORMED_MESSAGE'

        command = addr + base + code + variant

        logger.debug('Message command string : %s' % command)

        if param is None:

            logger.debug('Message has no parameter')

            CRC = utilities.create_crc(command)

            logger.debug('Message crc is : %s' % CRC)

            command = command + CRC

            logger.debug('Message command including crc : %s' % command)

            command = constants.STX + command + constants.EOT + constants.CR_LF

            logger.debug('Message string including ctrl chars : %s' % repr(command))

            response = command

        elif param is not None:

            logger.debug('Message has parameter')

            parameters = param.split(',')

            logger.debug('Message parameter is : %s' % repr(parameters))

            for i in range(len(parameters)):

                logger.debug('Message has single parameter')

                command = command + constants.US + parameters[i] + constants.US

                logger.debug('Message command string including parameter : %s' % repr(command))

                CRC = utilities.create_crc(command)

                logger.debug('Message crc is : %s' % CRC)

                command = constants.STX + command + CRC + constants.EOT + constants.CR_LF

                logger.debug('Message including crc and ctrl chars : %s' % repr(command))

                response = command

        return response