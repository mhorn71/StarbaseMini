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

import socket
import logging
import threading
import datetime
import queue
import io

import serial


udp_buffer = 1024
my_queue = queue.Queue()

logger = logging.getLogger('StarinetConnector')


class ReadFromUDPSocket(threading.Thread):

    def __init__(self, my_queue):
        logger.info("Read from UDP socket initialised.")
        threading.Thread.__init__(self)
        self.my_queue = my_queue

    def run(self):

        while True:
            buffer1, address = sock.recvfrom(udp_buffer)
            logger.debug("%s %s", "received data - ", repr(buffer1))

            if buffer1.decode().startswith('\x02') and buffer1.decode().endswith('\x04\r\n'):
                logger.info('%s %s',  'Starinet UDP Packet received from', address)
                logger.debug('%s %s',  'Starinet UDP Packet', repr(buffer1))

                self.my_queue.put((buffer1, address))
                self.my_queue.join()


class StaribusPort(threading.Thread):

    def __init__(self, my_queue):

        logger.info("StaribusPort translator initialised.")

        threading.Thread.__init__(self)
        self.my_queue = my_queue
        self.alive = threading.Event()
        self.alive.set()

    def run(self):

        logger.debug("Process run initialised.")

        while True:
            buffer3 = self.my_queue.get()

            if buffer3 is not None:

                current_time = datetime.datetime.now()
                timeout_time = current_time + datetime.timedelta(0, int(timeout))

                try:

                    ser.flushInput()  # flush input buffer, discarding all its contents
                    logger.debug('Flushing serial port input buffer')
                    ser.flushOutput()  # flush output buffer, aborting current output
                    logger.debug('Flushing serial port output buffer')

                    logger.info('Sending data to Staribus port')
                    ser.write(buffer3[0])  # write message to serial port, preceded

                    # serial port receive loop

                    data = []

                    while True:

                        if timeout_time >= datetime.datetime.now():
                            pass
                        else:
                            logging.warning('Timed out waiting for response from controller.')
                            self.my_queue.task_done()
                            break

                        inbuff = ser.inWaiting()  # Wait for data

                        if inbuff == 0:
                            pass
                        elif inbuff > 0:

                            logging.debug('%s %s', 'Serial port buffer length - ', inbuff)
                            received = ser_io.read()

                            logging.debug('%s %s', 'Data received from controller -', repr(received))

                            received = received.strip('\x16')  # strip SYN

                            if received is None:
                                pass
                            else:

                                data.append(received)

                                datastring = ''.join(data)

                                if datastring.startswith('\x02') and datastring.endswith('\n'):
                                    logging.debug('%s %s', 'Found data to return ', repr(datastring))
                                    sock.sendto(datastring.encode('utf-8'), buffer3[1])  # Send data back to client.
                                    logging.info('Sending received data from controller to' + str(buffer3[1]))
                                    self.my_queue.task_done()
                                    break

                except serial.SerialException as msg:
                    logging.critical("%s %s", "Critical serial port error - ", msg)
                except ValueError as msg:
                    logging.critical("%s %s", "Critical timeout value error - ", msg)
            else:
                logging.critical('Queue is empty which it never should be, run with debug enabled and try again.')
                self.my_queue.task_done()


class StarinetConnectorStart:
    def __init__(self,starinet_ipv4, starinet_port, serial_port, serial_baudrate, serial_timeout):

        '''
        StarinetConnectorStart initialises and starts the starinet to staribus relay service.
        :param starinet_ipv4: string
        :param starinet_port: string
        :param serial_port: string
        :param serial_baudrate: string
        :param serial_timeout: string
        '''

        global sock, ser, ser_io, timeout

        timeout = serial_timeout

        # Create socket (IPv4 protocol, datagram (UDP)) and bind to addressess
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.bind((starinet_ipv4, int(starinet_port)))
        except socket.error as msg:
            logging.critical('%s %s', 'Unable to initialise Starinet network port - ', msg)

        # initialise serial port
        try:
            ser = serial.Serial()
            ser.port = serial_port
            ser.baudrate = serial_baudrate
            ser.bytesize = serial.SEVENBITS
            ser.parity = serial.PARITY_EVEN
            ser.stopbits = serial.STOPBITS_ONE
            ser.timeout = 0
            ser.xonxoff = False
            ser.rtscts = False
            ser.dsrdtr = False
            ser.writeTimeout = 0.5
        except serial.SerialException as msg:
            logging.critical('%s %s', 'Unable to initialise serial port -', msg)
        except ValueError as msg:
            logging.critical('%s %s', "Unable to initialise serial port -", msg)

        ser_io = io.TextIOWrapper(io.BufferedReader(ser), encoding='utf-8', newline='\n', line_buffering=False)

        # Try to open serial port and close it.
        logging.debug('Opening serial port')
        try:
            ser.open()
        except serial.SerialException as msg:
            logging.critical('%s %s', 'Error opening serial port - ', msg)
        else:
            # Instantiate & start threads
            server = ReadFromUDPSocket(my_queue)
            interpreter = StaribusPort(my_queue)
            server.setDaemon(True)
            interpreter.setDaemon(True)
            server.start()
            interpreter.start()
