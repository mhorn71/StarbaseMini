__author__ = 'Mark'

import io
import time
import logging
import datetime

import serial

from core.configLoader import confLoader

config = confLoader()
logger = logging.getLogger('core.streams.staribus')
timeout = config.get('StaribusPort', 'timeout')

class Staribus:
    def __init__(self):
        pass

    def stream(message):
        '''
         Will return either a full formed Staribus response or TIMEOUT, PREMATURE_TERMINATION
        '''

        logger.info('%s %s', 'stream has been handed', repr(message))

        try:

            ser.flushInput()  # flush input buffer, discarding all its contents
            logger.debug('Serial port input buffer flushed')

            ser.flushOutput()  # flush output buffer, aborting current output
            logger.debug('Serial port output buffer flushed')

            message = message.encode()

            logger.info("Sending data to staribus instrument")
            logger.debug("%s %s", 'Serial port raw message encoded utf-8', repr(message))

            ser.write(message)  # write message to serial port, preceded
            logger.debug('Serial port message sent to controller')

            # A simple timeout
            current_time = datetime.datetime.now()
            timeout_time = current_time + datetime.timedelta(0, int(timeout))

            logger.debug('Starting new serial port receive loop')

            # serial port receive loop

            data = []

            while True:

                    if timeout_time >= datetime.datetime.now():
                        time.sleep(0.01)
                    else:
                        logging.warning('Timed out waiting for response from controller.')
                        return 'TIMEOUT'

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
                                return received

        except serial.SerialException as msg:
            logger.critical('Serial IO Error - %s', msg)
            return 'PREMATURE_TERMINATION'

if config.get('StaribusPort', 'port') == 'None':
    logging.critical('No Staribus port set.')
else:
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

    # Try to open serial port
    logger.debug('Opening serial port')
    try:
        ser.open()
    except serial.SerialException as msg:
        logging.critical('%s %s', 'Error opening serial port - ', msg)