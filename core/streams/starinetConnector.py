__author__ = 'mark'
import socket
import re
import logging
import serial
import resource
import threading
import datetime
import time

import core.utilities as utils

logging = logging.getLogger('core.starinetConnector')


class Connector:
    def __init__(self, parent):

        self.parent = parent

        if self.parent.config.get('StaribusPort', 'port') == 'None':
            self.parent.ui_message('No Staribus port set.')
            logging.critical('No Staribus port set.')
        else:
            # initialise serial port
            try:
                self.ser = serial.Serial()
                self.ser.port = self.parent.config.get('StaribusPort', 'port')
                self.ser.baudrate = int(self.parent.config.get('StaribusPort', 'baudrate'))
                self.ser.bytesize = serial.SEVENBITS
                self.ser.parity = serial.PARITY_EVEN
                self.ser.stopbits = serial.STOPBITS_ONE
                self.ser.timeout = 0
                self.ser.xonxoff = False
                self.ser.rtscts = False
                self.ser.dsrdtr = False
                self.ser.writeTimeout = float(self.parent.config.get('StaribusPort', 'write_timeout'))
            except IOError as msg:
                logging.critical('%s %s', 'Unable to initialise serial port -', msg)
                self.parent.ui_message('Unable to initialise Staribus port' + str(msg))
            except ValueError as msg:
                logging.critical('%s %s', "Unable to initialise serial port -", msg)
                self.parent.ui_message('Unable to initialise Staribus port' + str(msg))

            # Try to open serial port and close it.
            try:
                logging.debug('Attempting to open serial port')
                self.ser.open()
            except socket.error as msg:
                logging.critical('%s %s', 'Error opening serial port - ', msg)
                self.parent.ui_message('Unable to open Staribus port' + str(msg))
            finally:
                self.ser.close()

            # initialise network
            try:
                self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                self.sock.bind((self.parent.config.get('StarinetConnector', 'address'),
                           int(self.parent.config.get('StarinetConnector', 'port'))))
            except socket.error as msg:
                logging.critical('%s %s', 'Unable to initialise Starinet network port - ', msg)
                self.parent.ui_message('Unable to initialise Starinet port ' + str(msg))

            logging.info('StarinetConnector started.')

            t = threading.Thread(target=self.connectorx)
            t.daemon = True  # thread dies when main thread (only non-daemon thread) exits.
            t.start()

    def connectorx(self):

        while 1:  # main loop.

            data, addr = self.sock.recvfrom(1024)  # buffer size is 1024 bytes this was the default

            if re.match('\x02([0-9a-zA-Z]{14,14})\x04|\x02([0-9a-zA-Z]{10,10})\x1f', data.decode()):

                logging.info('%s %s', 'Connected from client -', addr)
                logging.info('%s %s', 'Data received from Staribus client -', data.decode())
                logging.debug('%s %s', 'Raw Data received from Staribus client -', repr(data.decode()))
                logging.debug('%s %s', 'Memory usage (bytes) -', resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)

                # Create command timeout encase we need it.
                command = re.match('\x02([0-9a-zA-Z]{14,14})\x04|\x02([0-9a-zA-Z]{10,10})\x1f', data.decode())

                command = command.group(0)  # get first match which should be the command.

                command = command.strip('\x02\x1F')  # strip control characters from command string.

                if len(command) == 10:  # Command has parameter.
                    timeout_base = '\x02' + command + '0001'
                    crc = utils.crc_create(timeout_base)
                    timeout_return_str = timeout_base + crc + '\x04\x0D\x0A'
                    logging.debug('%s %s', 'Return Timeout set to', repr(timeout_return_str))
                elif len(command) == 15:  # Command has no parameter.
                    timeout_base = '\x02' + command[:-5] + '0001'
                    crc = utils.crc_create(timeout_base)
                    timeout_return_str = timeout_base + crc + '\x04\x0D\x0A'
                    logging.debug('%s %s', 'Return Timeout set to', repr(timeout_return_str))
                else:
                    logging.critical('Unable to parse command')

                # A simple timeout
                timeout = self.parent.config.get('StaribusPort', 'timeout')
                current_time = datetime.datetime.now()
                timeout_time = current_time + datetime.timedelta(0, int(timeout))

                try:
                    logging.debug('Opening serial port')
                    self.ser.open()
                    self.ser.flushInput()  # flush input buffer, discarding all its contents
                    logging.debug('Flushing serial port input buffer')
                    self.ser.flushOutput()  # flush output buffer, aborting current output
                    logging.debug('Flushing serial port output buffer')
                    logging.debug('%s %s', 'Sending data to Staribus port ', data)
                    self.ser.write(data)  # write message to serial port, preceded

                    inbuff = 0

                    # serial port receive loop

                    while True:

                        if timeout_time >= datetime.datetime.now():
                            time.sleep(0.2)  # we sleep to stop race condition.
                            pass
                        else:
                            self.ser.close()
                            logging.debug('%s %s', 'Return Timeout being sent to', addr)
                            self.sock.sendto(timeout_return_str.encode(), addr)  # Send data back to Staribus client.
                            break

                        inbuff = self.ser.inWaiting()  # Wait for data

                        if inbuff == 0:
                            pass
                        elif inbuff > 0:
                            logging.debug('%s %s', 'Serial port inbuffer - ', inbuff)
                            received = self.ser.readline()

                            logging.info('%s %s', 'Data received from Staribus client -', received)
                            logging.debug('%s %s', 'Received data in hex -', repr(received))

                            received = received.decode()

                            rt_data = received.strip('\x16')  # strip DLE

                            self.sock.sendto(rt_data.encode(), addr)  # Send data back to Staribus client.

                except serial.SerialException as msg:
                    logging.critical("%s %s", "Critical serial port error - ", msg)
                    self.parent.ui_message('Staribus port exception ' + str(msg))
                except ValueError as msg:
                    logging.critical("%s %s", "Critical timeout value error - ", msg)
                    self.parent.ui_message('Staribus port error ' + str(msg))

