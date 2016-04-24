__author__ = 'Mark'
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
import socket
import datetime
import time

udp_buffer = 1024


class StarinetStream:
    def __init__(self, starinet_address, starinet_port, starinet_timeout):
        self.logger = logging.getLogger('dao.StarinetStream')

        # setup parameters.
        self.starinet_client_address = starinet_address, int(starinet_port)
        self.timeout = starinet_timeout

        # Create socket (IPv4 protocol, datagram (UDP)) and bind to all IPv4 Interfaces.
        self.logger.debug('Opening UDP interface.')
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.sock.settimeout(int(starinet_timeout))
            self.sock.bind(('', int(starinet_port)))
        except socket.error as msg:
            self.logger.critical('%s %s', 'Unable to initialise Starinet network port - ', msg)
            raise IOError(msg)

    def close(self):
        self.sock.close()

    def stream(self, message):
        '''
         Will return either a full formed Staribus/net response or TIMEOUT, PREMATURE_TERMINATION
        '''

        self.logger.info('%s %s', 'stream has been handed', repr(message))

        message = message.encode()

        self.logger.info("Sending data to starinet instrument")
        self.logger.debug("%s %s", 'UDP socket raw message encoded utf-8', repr(message))

        try:
            self.sock.sendto(message, self.starinet_client_address)
            self.logger.debug('UDP socket message sent to controller')
        except OSError:
            return 'ERROR'

        # Number of retries.
        retries = 1

        # socket port receive loop

        while True:

            try:
                buffer1, address = self.sock.recvfrom(udp_buffer)
            except socket.timeout:
                if retries < 4:
                    # write message to UDP socket.
                    try:
                        self.sock.sendto(message, self.starinet_client_address)
                    except OSError as msg:
                        self.logger.warning('UDP socket send message retry : %s ' % str(retries))
                        self.logger.warning(str(msg))

                        if retries == 3:
                            return 'TIMEOUT'

                    else:
                        self.logger.warning('UDP socket send message retry : %s' % str(retries))

                    retries += 1
                else:
                    self.logger.warning('Timed out waiting for response from controller.')
                    return 'TIMEOUT'
            else:
                if buffer1.decode().startswith('\x02') and buffer1.decode().endswith('\x04\r\n'):
                    self.logger.info('%s %s',  'Starinet UDP Packet received from', address)
                    self.logger.debug('%s %s',  'Starinet UDP Packet', repr(buffer1))
                    return buffer1.decode('utf-8')
