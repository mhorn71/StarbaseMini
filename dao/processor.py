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

import dao
import logging


class DaoProcessor:
    def __init__(self):

        logger = logging.getLogger('dao.DaoProcessor')

        self.command_message = dao.StaribusCommandMessage()

        self.response_message = dao.StaribusResponseMessage()

        logger.debug('Initialised.')

    def start(self, serial_port, serial_baudrate, serial_timeout, starinet_address,
              starinet_port, stream, staribus_port_type):

        logger = logging.getLogger('dao.DaoProcessor.start')

        if stream == 'Starinet':

            logger.debug('Starinet Stream selected')

            # we use the serial_timeout as well for the StarinetStream.

            try:

                self.message_stream = dao.StarinetStream(starinet_address, starinet_port, serial_timeout)

            except IOError as msg:

                logger.warning(str(msg))

                raise IOError(msg)

            else:

                logger.debug('Stream set to Starinet')

        else:

            logger.debug('Staribus Stream selected')

            if staribus_port_type == 'RS232':

                try:

                    self.message_stream = dao.StaribusStream(serial_port, serial_baudrate, serial_timeout)

                except IOError as msg:

                    logger.warning(str(msg))

                    raise IOError(msg)

                else:

                    logger.debug('Stream set to Staribus')

            elif staribus_port_type == 'RS485':

                # Need to write the RS485 stream interface.

                pass

            else:

                logger.debug('Unknown port standard type : %s' % staribus_port_type)

                raise IOError('Unknown port standard type : %s' % staribus_port_type)

    def close(self):

        logger = logging.getLogger('dao.DaoProcessor.close')

        try:

            self.message_stream.close()

        except AttributeError as msg:

            logger.warning('Unable to close message stream : %s' % str(msg))

        else:

            logger.info('Message stream closed.')

    def star_message(self, addr, base, code, variant, param):
        '''

        :param addr:
        :param base:
        :param code:
        :param variant:
        :param param:
        :return: tuple (status_message, payload)
                 Error messsages returned : MALFORMED_MESSAGE, ERROR, TIMEOUT
        '''

        logger = logging.getLogger('dao.DaoProcessor.star_message')

        # Construct the Staribus Message this works for both Staribus and Starinet.

        constructed_message = self.command_message.construct(addr, base, code, variant, param)

        logger.debug('Message command string : %s' % repr(constructed_message))

        if constructed_message == 'MALFORMED_MESSAGE':

            logger.critical('Constructed message is malformed : %s' % repr(constructed_message))

            return 'MALFORMED_MESSAGE', None

        else:

            try:

                stream_reply = self.message_stream.stream(constructed_message)

            except IOError as msg:

                logger.critical('stream reply IOError : %s' % str(msg))

                return 'ERROR', str(msg)

            if stream_reply == 'TIMEOUT':

                logger.warning('stream reply TIMEOUT')

                return 'TIMEOUT', None

            elif stream_reply == 'ERROR':

                logger.warning('Error unable to send to socket')

                response = 'ERROR', 'Unable to send to socket.'

            else:

                response = self.response_message.decipher(stream_reply)

            return response
