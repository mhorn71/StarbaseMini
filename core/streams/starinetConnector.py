__author__ = 'mark'
import socket
import re
import logging
import os
import serial
import resource
import threading
import datetime
import time

import core.utilities as utils

logging = logging.getLogger('core.starinetConnector')


class connector:
    def __init__(self, parent):

        self.parent = parent
        t = threading.Thread(target=self.connectorx)
        t.daemon = True  # thread dies when main thread (only non-daemon thread) exits.
        t.start()

    def connectorx(self):

        # initialise serial port
        try:
            ser = serial.Serial()
            ser.port = self.parent.config.get('StaribusPort', 'port')
            ser.baudrate = int(self.parent.config.get('StaribusPort', 'baudrate'))
            ser.bytesize = serial.SEVENBITS
            ser.parity = serial.PARITY_EVEN
            ser.stopbits = serial.STOPBITS_ONE
            ser.timeout = 0
            ser.xonxoff = False
            ser.rtscts = False
            ser.dsrdtr = False
            ser.writeTimeout = float(self.parent.config.get('StaribusPort', 'write_timeout'))
        except IOError as msg:
            logging.critical("Unable to initialise serial port -" + msg)
            logging.info("Stopping starinetConnector ....")
            utils.exit_message('Unable to initialise Staribus port' + msg)
        except ValueError as msg:
            logging.critical("Unable to initialise serial port -" + msg)
            logging.info("Stopping starinetConnector ....")
            self.parent.ui_message('Unable to initialise Staribus port' + msg)

        logging.info("%s %s", "Found Staribus port - ", ser.name)
        logging.info("Staribus port initialised.")

        # initialise network
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.bind((self.parent.config.get('StarinetConnector', 'address'),
                       int(self.parent.config.get('StarinetConnector', 'port'))))
        except socket.error as msg:
            logging.critical("%s %s", "Unable to initialise network port - ", msg)
            logging.info("Stopping starinetConnector ....")
            self.parent.ui_message('Unable to initialise Starinet port' + str(msg))

        logging.info('starinetConnector started.')

        while 1:  # main loop.

            data, addr = sock.recvfrom(1024)  # buffer size is 1024 bytes this was the default

            if re.match('\x02([0-9a-zA-Z]{14,14})\x04|\x02([0-9a-zA-Z]{10,10})\x1f', data.decode()):

                logging.info("%s %s", "Connected from host -", addr)
                logging.info("%s %s", "Data received from Starbase -", data.decode())
                logging.debug("%s %s", "Data received from Starbase in hex -", repr(data.decode()))
                logging.debug("%s %s", "Memory usage (kb) -", resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)

                try:
                    logging.debug('Attempting to open serial port')
                    ser.open()
                except socket.error as msg:
                    logging.critical("%s %s", "Error opening serial port - ", msg)
                    logging.info("Stopping StaribusPyRouter ....")
                    self.parent.ui_message('Unable to open Staribus port' + str(msg))

                # A simple timeout
                timeout = self.parent.config.get('StaribusPort', 'timeout')
                current_time = datetime.datetime.now()
                timeout_time = current_time + datetime.timedelta(0, int(timeout))

                try:
                    logging.debug('Serial Port is open')
                    ser.flushInput()  # flush input buffer, discarding all its contents
                    ser.flushOutput()  # flush output buffer, aborting current output
                    ser.write(data)  # write message to serial port, preceded
                    # time.sleep(float(commandpause))  # give the serial port sometime to receive the data

                    inbuff = 0

                    # serial port receive loop

                    while 1:

                        if timeout_time >= datetime.datetime.now():
                            time.sleep(0.5)  # we sleep to stop race condition.
                            pass
                        else:
                            ser.close()
                            return 'TIMEOUT'

                        logging.debug("%s %s", "Serial port buffer data - ", inbuff)
                        logging.debug('Starting new serial port receive loop')
                        inbuff = ser.inWaiting()  # Wait for data
                        if inbuff > 0:  # If inbuff has data proceed
                            logging.debug("%s %s", "Serial port inbuffer - ", inbuff)
                            received = ser.readline()

                            logging.info("%s %s", "Data received from Staribus VLF Instrument -", received)
                            logging.debug("%s %s", "Received data in hex -", repr(received))

                            rt_data = received.translate(None, '\x16')  # strip DLE

                            sock.sendto(rt_data, (addr))  # Send data back to Starbase
                        else:
                            logging.debug("Serial port buffer empty - exiting serial port receive loop")
                            ser.close()
                            break

                except serial.SerialException as msg:
                    logging.critical("%s %s", "Critical serial port error - ", msg)
                    logging.info("Stopping StaribusPyRouter ....")
                    os.system('service staribuspyrouter stop')
                    self.parent.ui_message('Staribus port exception ' + str(msg))
                except ValueError as msg:
                    logging.critical("%s %s", "Critical timeout value error - ", msg)
                    logging.info("Stopping StaribusPyRouter ....")
                    os.system('service staribuspyrouter stop')
                    self.parent.ui_message('Staribus port error ' + str(msg))
        else:
            logging.info("Stopping StaribusPyRouter ....")
            os.system('service staribuspyrouter stop')

# if __name__ == "__main__":
#     # daemon = MyDaemon('/tmp/staribuspyrouter.pid')
#     if len(sys.argv) > 1:
#         if 'start' == sys.argv[1]:
#             logging.info('\n======================= Staribuspyrouter daemon starting =======================')
#             # daemon.start()
#         elif 'stop' == sys.argv[1]:
#             logging.info('\n========================= Staribuspyrouter shutdown ============================')
#             # daemon.stop()
#         elif 'restart' == sys.argv[1]:
#             logging.info('\n======================== Staribuspyrouter restarting ===========================')
#             # daemon.restart()
#         else:
#             print("Unknown command")
#             sys.exit(2)
#         sys.exit(0)
#     else:
#         print "usage: %s start|stop|restart" % sys.argv[0]


# def connector(self):
#     logger.info('StarinetConnector')
