__author__ = 'mark'

import socket
import logging
import resource
import threading
import datetime
import queue
import io
import time

import serial

from core.configLoader import confLoader

config = confLoader()

udp_buffer = 600
my_queue = queue.Queue()
timeout = config.get('StaribusPort', 'timeout')

logging = logging.getLogger('core.starinetConnector')


class ReadFromUDPSocket(threading.Thread):

    def __init__(self, my_queue):
        logging.info("ReadFromUDPSocket __init__ initialised.")
        threading.Thread.__init__(self)
        self.my_queue = my_queue

    def run(self):
        while True:
            buffer1, address = sock.recvfrom(udp_buffer)
            logging.debug("%s %s", "received data - ", repr(buffer1))

            if buffer1.decode().startswith('\x02') and buffer1.decode().endswith('\x04\r\n'):
                logging.info('%s %s',  'Starinet UDP Packet received from', address)
                logging.debug('%s %s',  'Starinet UDP Packet', repr(buffer1))
                logging.debug('%s %s', 'Memory usage (bytes) -', resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)

                self.my_queue.put((buffer1, address))
                self.my_queue.join()


class StaribusPort(threading.Thread):

    def __init__(self, my_queue):

        logging.info("StaribusPort translator __init__ initialised.")

        threading.Thread.__init__(self)
        self.my_queue = my_queue
        self.alive = threading.Event()
        self.alive.set()

    def run(self):

        logging.debug("Process run initialised.")

        while True:
            buffer3 = self.my_queue.get()

            if buffer3 is not None:

                current_time = datetime.datetime.now()
                timeout_time = current_time + datetime.timedelta(0, int(timeout))

                try:

                    ser.flushInput()  # flush input buffer, discarding all its contents
                    logging.debug('Flushing serial port input buffer')
                    ser.flushOutput()  # flush output buffer, aborting current output
                    logging.debug('Flushing serial port output buffer')

                    logging.info('Sending data to Staribus port')
                    ser.write(buffer3[0])  # write message to serial port, preceded

                    # serial port receive loop

                    data = []

                    while True:

                        if timeout_time >= datetime.datetime.now():
                            time.sleep(0.01)
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

if config.get('StaribusPort', 'port') == 'None':
    logging.critical('No Staribus port set.')
else:
    # Create socket (IPv4 protocol, datagram (UDP)) and bind to addressess
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind((config.get('StarinetConnector', 'address'),
                   int(config.get('StarinetConnector', 'port'))))
    except socket.error as msg:
        logging.critical('%s %s', 'Unable to initialise Starinet network port - ', msg)

# initialise serial port
try:
    ser = serial.Serial()
    ser.port = config.get('StaribusPort', 'port')
    ser.baudrate = int(config.get('StaribusPort', 'baudrate'))
    ser.bytesize = serial.SEVENBITS
    ser.parity = serial.PARITY_EVEN
    ser.stopbits = serial.STOPBITS_ONE
    ser.timeout = 0
    ser.xonxoff = False
    ser.rtscts = False
    ser.dsrdtr = False
    ser.writeTimeout = float(config.get('StaribusPort', 'write_timeout'))
except serial.SerialException as msg:
    logging.critical('%s %s', 'Unable to initialise serial port -', msg)
except ValueError as msg:
    logging.critical('%s %s', "Unable to initialise serial port -", msg)

ser_io = io.TextIOWrapper(io.BufferedReader(ser), encoding='utf-8', newline='\n', line_buffering=True)

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
