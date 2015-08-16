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

# look at Starbase StaribusResponseMessage.java

# **************************************************************************************************
#    Response Only, or ErrorResponse for a Command which would expect a ResponseValue
#
#    Header          STX
#    Address         char char
#    CommandCode     char char char char
#    CommandVariant  char char char char
#    StatusCode      char char char char
#    CrcChecksum     char char char char  in Hex
#    Terminator      EOT CR LF
#
#    h n n n n n n n n n n n n n n n n n n e c l
#    i.e. must get at least 18 before looking for the terminator
#
# **************************************************************************************************
#    Response with Value
#
#    Header          STX
#    Address         char char
#    CommandCode     char char char char
#    CommandVariant  char char char char
#    StatusCode      char char char char
#    Separator       US
#    Value           char {char ..} US
#    CrcChecksum     char char char char  in Hex
#    Terminator      EOT CR LF
#
# ***************************************************************************************************


class StaribusResponseMessage:
    def __init__(self):
        self.logger = logging.getLogger('dao.StaribusResponsMessage')

    def decipher(self, message):

        # strip STX from message
        stx_stripped = message.strip(constants.STX)
        self.logger.debug('Message stripped of STX : %s' % repr(stx_stripped))

        # strip EOT CR LF
        to_strip = constants.EOT + constants.CR_LF
        message = stx_stripped.strip(to_strip)
        self.logger.debug('Message stripped of EOT CR LF : %s' % repr(message))

        if len(message) == 18:
            self.logger.debug('Message has no data payload.')
            if utilities.check_crc(message):
                self.logger.debug('Message passed crc check.')

                # Slice off the CRC code.
                message_minus_crc = message[:14]
                self.logger.debug('Message minus crc : %s' % message_minus_crc)

                # remove the being of the message to get at status code.
                status_code = message_minus_crc[-4:]
                self.logger.debug('Message status byte code : %s' % status_code)

                # convert the status code bytes to string.
                status = utilities.staribus_status_b2str(status_code)
                self.logger.debug('Message status code string : %s' % status)

                return status, None

            else:
                self.logger.debug('Message failed crc check.')
                return 'CRC_ERROR', None

        else:
            self.logger.debug('Message has payload.')
            # as we have data we need to strip the last US from the message string before passing to check_crc.
            message = message.strip(constants.US)
            self.logger.debug('Message stripped of last US : %s' % repr(message))

            if utilities.check_crc(message):
                self.logger.debug('Message passed crc check.')
                # strip data payload from message so we can get at status code.
                message_less_data = message[0:14]
                self.logger.debug('Message striped of payload data : %s' % repr(message_less_data))

                # remove the being of the message to get at status code.
                status_code = message_less_data[-4:]
                self.logger.debug('Message status byte code : %s' % status_code)

                # convert the status code bytes to string.
                status = utilities.staribus_status_b2str(status_code)
                self.logger.debug('Message status code string : %s' % status)

                # strip unwanted data from payload.
                payload = message[14:-4]
                self.logger.debug('Message payload : %s' % repr(payload))

                # strip US from message.
                payload = payload.replace(constants.US, '')

                return status, payload
            else:
                self.logger.debug('Message failed crc check.')
                return 'CRC_ERROR', None

