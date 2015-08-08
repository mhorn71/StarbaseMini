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

        # Check staribus address is correct it should be as we have already checked in instrument loader.
        if utilities.check_staribus_address(addr):
            # covert string to int base 16
            addr = int(addr, 16)
            # change back to str and make sure length is two chars long padd with leading zero if not.
            addr = str(addr).zfill(2)
        else:
            return 'MALFORMED_MESSAGE'

        # The base and code are a hex byte and must be in the range 0x00 - 0xFF
        # so we'll use the check_staribus address to confirm they're in range.

        if utilities.check_hexbyte_string(base) is not True:
            return 'MALFORMED_MESSAGE'

        if utilities.check_hexbyte_string(code) is not True:
            return 'MALFORMED_MESSAGE'

        # Check the command variant is within in range for hex word 0x0000 - 0xFFFF
        if utilities.check_hexword_string(variant) is not True:
            return 'MALFORMED_MESSAGE'

        command = addr + base + code + variant

        if param is None:

            CRC = utilities.create_crc(command)

            command = command + CRC

            command = constants.STX + command + constants.EOT + constants.CR_LF

            response = command

        elif param is not None:

            parameters = param.split(',')

            if len(parameters) == 1:

                command = command + constants.US + parameters[0]

                CRC = utilities.create_crc(command)

                command = constants.STX + command + constants.US + CRC + \
                    constants.EOT + constants.CR_LF

                response = command

            elif len(parameters) > 1:

                parameter_length = len(parameters)

                parameter_construct = ''

                for i in range(parameter_length):
                    if i < (parameter_length - 1):
                        parameter_construct = parameter_construct + parameters[i] + constants.US
                    else:
                        parameter_construct = parameter_construct + parameters[i]

                command = command + constants.US + parameter_construct

                CRC = utilities.create_crc(command)

                command = constants.STX + command + constants.US + CRC + \
                    constants.EOT + constants.CR_LF

                response = command

        else:

            response = 'MALFORMED_MESSAGE'

        return response