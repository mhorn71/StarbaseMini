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

import io
import time
import logging
import datetime

import serial


class StaribusStream:
    def __init__(self, serial_port, serial_baudrate, serial_timeout):

        # initialise the logger
        self.logger = logging.getLogger('dao.staribus.stream')

        # initialise serial port
        try:
            self.staribus_port = serial.Serial()
            self.staribus_port.port = serial_port
            self.staribus_port.baudrate = serial_baudrate
            self.staribus_port.bytesize = serial.SEVENBITS
            self.staribus_port.parity = serial.PARITY_EVEN
            self.staribus_port.stopbits = serial.STOPBITS_ONE
            self.staribus_port.timeout = 0
            self.staribus_port.xonxoff = False
            self.staribus_port.rtscts = False
            self.staribus_port.dsrdtr = False
            self.staribus_port.writeTimeout = 1.0
        except serial.SerialException as msg:
            self.logger.critical('%s %s', 'Unable to initialise serial port -', msg)
            raise IOError(msg)
        except ValueError as msg:
            self.logger.critical('%s %s', "Unable to initialise serial port -", msg)
            raise IOError(msg)

        self.timeout = serial_timeout

        self.ser_io = io.TextIOWrapper(io.BufferedReader(self.staribus_port), encoding='utf-8',
                                       newline='\n', line_buffering=True)

        # Try to open serial port
        self.logger.debug('Opening serial port')
        try:
            self.staribus_port.open()
        except serial.SerialException as msg:
            self.logger.critical('%s %s', 'Error opening serial port - ', msg)
            raise IOError(msg)

    def stream(self, message):
        '''
         Will return either a full formed Staribus response or TIMEOUT, PREMATURE_TERMINATION
        '''

        self.logger.info('%s %s', 'stream has been handed', repr(message))

        try:

            # self.staribus_port.flushInput()  # flush input buffer, discarding all its contents
            # logger.debug('Serial port input buffer flushed')
            #
            # self.staribus_port.flushOutput()  # flush output buffer, aborting current output
            # logger.debug('Serial port output buffer flushed')

            message = message.encode()

            self.logger.info("Sending data to staribus instrument")
            self.logger.debug("%s %s", 'Serial port raw message encoded utf-8', repr(message))

            self.staribus_port.write(message)  # write message to serial port, preceded
            self.logger.debug('Serial port message sent to controller')

            # A simple timeout
            current_time = datetime.datetime.now()
            timeout_time = current_time + datetime.timedelta(0, int(self.timeout))

            # Number of retries.
            retries = 1

            self.logger.debug('Starting new serial port receive loop')

            # serial port receive loop

            data = []

            while True:

                    if timeout_time >= datetime.datetime.now():
                        time.sleep(0.01)
                    else:
                        if retries < 4:
                            self.staribus_port.write(message)  # write message to serial port, preceded
                            self.logger.warning('Serial port send message retry : %s' % str(retries))
                            retries += 1
                        else:
                            self.logger.warning('Timed out waiting for response from controller.')
                            return 'TIMEOUT'

                    inbuff = self.staribus_port.inWaiting()  # Wait for data

                    if inbuff == 0:
                        pass
                    elif inbuff > 0:

                        self.logger.debug('%s %s', 'Serial port buffer length - ', inbuff)
                        received = self.ser_io.read()

                        self.logger.debug('%s %s', 'Data received from controller -', repr(received))

                        received = received.strip('\x16')  # strip SYN

                        if received is None:
                            pass
                        else:

                            data.append(received)

                            datastring = ''.join(data)

                            if datastring.startswith('\x02') and datastring.endswith('\n'):
                                self.logger.debug('%s %s', 'Found data to return ', repr(datastring))
                                return datastring

        except serial.SerialException as msg:
            self.logger.critical('Serial IO Error - %s', msg)
            raise IOError(msg)
