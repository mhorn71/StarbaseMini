__author__ = 'mark'
import socket
import logging
import resource
import threading
import datetime
import time
import queue
import serial
import io


udp_buffer = 700
my_queue = queue.Queue()

logging = logging.getLogger('core.starinetConnector')


class Connector:
    def __init__(self, parent):

        self.parent = parent

        if self.parent.config.get('StaribusPort', 'port') == 'None':
            self.parent.ui_message('No Staribus port set.')
            logging.critical('No Staribus port set.')
        else:
            # Create socket (IPv4 protocol, datagram (UDP)) and bind to addressess
            # initialise network
            try:
                self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                self.sock.bind((self.parent.config.get('StarinetConnector', 'address'),
                           int(self.parent.config.get('StarinetConnector', 'port'))))
            except socket.error as msg:
                logging.critical('%s %s', 'Unable to initialise Starinet network port - ', msg)
                self.parent.ui_message('Unable to initialise Starinet port ' + str(msg))

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
                # self.ser.writeTimeout = float(self.parent.config.get('StaribusPort', 'write_timeout'))
            except serial.SerialException as msg:
                logging.critical('%s %s', 'Unable to initialise serial port -', msg)
                self.parent.ui_message('Unable to initialise Staribus port' + str(msg))
            except ValueError as msg:
                logging.critical('%s %s', "Unable to initialise serial port -", msg)
                self.parent.ui_message('Unable to initialise Staribus port' + str(msg))

            self.ser_io = io.TextIOWrapper(io.BufferedReader(self.ser, 1), encoding='utf-8', newline='\n',
                                           line_buffering=False)

            # Try to open serial port and close it.
            try:
                logging.debug('Attempting to open serial port')
                self.ser.open()
            except socket.error as msg:
                logging.critical('%s %s', 'Error opening serial port - ', msg)
                self.parent.ui_message('Unable to open Staribus port' + str(msg))
            finally:
                self.ser.close()

            self.timeout = self.parent.config.get('StaribusPort', 'timeout')

            # Instantiate & start threads
            server = ReadFromUDPSocket(my_queue, self)
            interpreter = StaribusPort(my_queue, self)
            server.setDaemon(True)
            interpreter.setDaemon(True)

            server.start()
            interpreter.start()


class ReadFromUDPSocket(threading.Thread):

    def __init__(self, my_queue, parent):
        logging.info("ReadFromUDPSocket __init__ initialised.")
        threading.Thread.__init__(self)
        self.my_queue = my_queue
        self.parent = parent

    def run(self):
        while True:
            buffer1, address = self.parent.sock.recvfrom(udp_buffer)
            logging.debug("%s %s", "received data - ", repr(buffer1))

            if buffer1.decode().startswith('\x02') and buffer1.decode().endswith('\x04\r\n'):
                logging.info("%s %s %s",  'Starinet UDP Packet received from', address, repr(buffer1))
                logging.debug('%s %s', 'Memory usage (bytes) -', resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
                
                self.my_queue.put((buffer1, address))
                self.my_queue.join()


class StaribusPort(threading.Thread):

    def __init__(self, my_queue, parent):

        logging.info("StaribusPort translator __init__ initialised.")

        threading.Thread.__init__(self)
        self.my_queue = my_queue
        self.alive = threading.Event()
        self.alive.set()

        self.parent = parent

    def run(self):

        logging.debug("Process run initialised.")

        while True:

            buffer3 = self.my_queue.get()

            if buffer3 is not None:
                # A simple timeout
                timeout = self.parent.timeout
                current_time = datetime.datetime.now()
                timeout_time = current_time + datetime.timedelta(0, int(timeout))
    
                self.parent.ser.close()
    
                try:
    
                    logging.debug('Opening serial port')
                    self.parent.ser.open()
                    # self.parent.ser.flushInput()  # flush input buffer, discarding all its contents
                    # logging.debug('Flushing serial port input buffer')
                    # self.parent.ser.flushOutput()  # flush output buffer, aborting current output
                    # logging.debug('Flushing serial port output buffer')
                    logging.info('Sending data to Staribus port')
                    self.parent.ser.write(buffer3[0])  # write message to serial port, preceded
    
                    # serial port receive loop

                    data = []
    
                    while True:

                        if timeout_time >= datetime.datetime.now():
                            # time.sleep(0.5)
                            pass
                        else:
                            self.parent.ser.close()
                            logging.warning('Timed out waiting for response from controller.')
                            self.my_queue.task_done()
                            break
    
                        inbuff = self.parent.ser.inWaiting()  # Wait for data

                        if inbuff == 0:
                            pass
                        elif inbuff > 0:

                            logging.debug('%s %s', 'Serial port buffer length - ', inbuff)
                            received = self.parent.ser_io.read()
    
                            logging.info('%s %s', 'Data received from controller -', repr(received))

                            # rt_data = received #.strip('\x16')  # strip DLE

                            if received is None:
                                pass
                            else:
                                data.append(received)

                            datastring = ''.join(data)

                            if datastring is None:
                                pass
                            else:
                                if datastring.startswith('\x16') and datastring.endswith('\n'):
                                    logging.debug('%s %s', 'Found data to return ', repr(datastring))
                                    self.parent.sock.sendto(datastring.encode('utf-8'), buffer3[1])  # Send data back to client.
                                    logging.info('Sending data back to ' + str(buffer3[1]))
                                    self.my_queue.task_done()
                                    break

                except serial.SerialException as msg:
                    logging.critical("%s %s", "Critical serial port error - ", msg)
                    self.parent.parent.ui_message('Staribus port exception ' + str(msg))
                except ValueError as msg:
                    logging.critical("%s %s", "Critical timeout value error - ", msg)
                    self.parent.parent.ui_message('Staribus port error ' + str(msg))
            else:
                logging.critical('Queue is empty which it never should be, run with debug enabled and try again.')
                self.my_queue.task_done()