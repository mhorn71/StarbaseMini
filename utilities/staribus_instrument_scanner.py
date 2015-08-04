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

import datetime
import io
import time
import logging

import serial

import utilities.crc_tool as crc_tool

logger = logging.getLogger('check_serial_port_staribus_instrument')


def check_serial_port_staribus_instrument(address, ports, baudrate):

    '''
    Checks supplied serial ports for staribus instrument
    :param address: Staribus address 000 - 253
    :param ports: serial port or list of serial ports
    :param baudrate: serial port baudrate.
    :return: list of ports if more than one instrument found or None.
    '''

    address = address.lstrip()  # Strip leading zeros

    address = hex(int(address)).strip('0x')  # Change str to int then to hex and strip 0x

    address = address.zfill(2)  # Pad address to two places with leading zero.

    logger.debug('%s %s', 'Constructing Staribus message for address :', address)

    staribus_message = address + '00010000'

    checksum = crc_tool.create_crc(staribus_message)

    staribus_port_message = ('\x02' + staribus_message + checksum + '\x04\x0D\x0A').encode('utf-8')

    logger.debug('%s %s', 'Message to be sent to port :', repr(staribus_port_message.decode()))

    staribus_ports = []

    if ports is None:
        raise OSError('No serial ports supplied.')

    for port in ports:

        current_time = datetime.datetime.now()
        timeout_time = current_time + datetime.timedelta(0, 10)

        try:
            s = serial.Serial()
            s.port = port
            s.baudrate = int(baudrate)
            s.bytesize = serial.SEVENBITS
            s.parity = serial.PARITY_EVEN
            s.stopbits = serial.STOPBITS_ONE
            s.timeout = 0
            s.xonxoff = False
            s.rtscts = False
            s.dsrdtr = False
            s.writeTimeout = 0.2

            s.open()

            ser_io = io.TextIOWrapper(io.BufferedReader(s), encoding='utf-8', newline='\n', line_buffering=False)

            logger.debug('Flushing input and output buffers.')
            s.flushInput()  # flush input buffer, discarding all its contents
            s.flushOutput()  # flush output buffer, aborting current output

            s.write(staribus_port_message)

            while True:

                if timeout_time >= datetime.datetime.now():
                    time.sleep(0.25)
                else:
                    s.close()
                    break

                buffer = s.inWaiting()  # Wait for data

                if buffer == 0:
                    pass
                elif buffer > 0:

                    received = ser_io.readline()

                    if received is not None:
                        logger.debug('%s %s', 'Message received :', repr(received))
                        received = received.strip('\x16\x02\x04\x0D\x0A')

                    if crc_tool.check_crc(received) is True:
                        # The length of ping packet response. This is a bodge in case a loop back device is found.
                        # The current UKRAA controller will return the sent message with a status of success, which
                        # once you strip off the beginning and end control characters the message length should be 25
                        # chars long, if it isn't the device is probably a loop back device.
                        if buffer == 25:
                            staribus_ports.append(port)
                            s.close()
                            break
                        else:
                            s.close()
                            break

        except serial.SerialException:
            logger.critical('%s %s', 'Unable to open port ', str(port))

    if len(staribus_ports) == 0:
        return None
    elif len(staribus_ports) >= 1:
        return staribus_ports

