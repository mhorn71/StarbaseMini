__author__ = 'Mark'

# import sys
import time
import serial
import logging
import datetime
from core.configLoader import confLoader

logger = logging.getLogger('core.streams.staribus')


class Serial:
    def __init__(self, parent):
        '''initialise serial port
            raises: IOError'''

        # logger = logging.getLogger('core.streams.staribus')
        self.config = confLoader()
        self.parent = parent

        global ser

        try:
            ser = serial.Serial()
            ser.port = self.config.get('serialport', 'port')
            ser.baudrate = int(self.config.get('serialport', 'baudrate'))
            ser.bytesize = serial.SEVENBITS
            ser.parity = serial.PARITY_EVEN
            ser.stopbits = serial.STOPBITS_ONE
            ser.timeout = None  # Can be None or Zero
            ser.xonxoff = False
            ser.rtscts = False
            ser.dsrdtr = False
            ser.writeTimeout = float(self.config.get('serialport', 'writeTimeout'))
            ser.open()
            ser.close()
        except IOError as msg:
            logger.critical("%s %s", "Unable to initialise serial port -", msg)
            raise IOError(msg)
        except ValueError as msg:
            logger.critical("%s %s", "Unable to initialise serial port -", msg)
            raise IOError(msg)
        else:
            logger.info("Serial port %s initialised.", ser.name)

    def stream(self, message):
        '''
         stream expects a full formed message excluding the start and end control characters  \x02\x04\x0D\x0A

         e.g. 0101010000\x1f2015-05-15\x1f1E24

         Returns TIME_OUT in the event of no data being received or the received Staribus message.

         e.g. 010101000000001B4A

         NOTE: No checking of the message is performed.

         Raises: IOError
        '''

        logger.info('%s %s', 'stream has been handed', message.strip('\r\n'))

        try:
            ser.open()
            logger.debug('Serial port opened')

            ser.flushInput()  # flush input buffer, discarding all its contents
            logger.debug('Serial port input buffer flushed')

            ser.flushOutput()  # flush output buffer, aborting current output
            logger.debug('Serial port output buffer flushed')

            message = message.encode()

            logger.info("Sending data to staribus instrument")
            logger.debug("%s %s", 'Serial port raw message encoded utf-8', repr(message))
            ser.write(message)  # write message to serial port, preceded
            logger.debug('Serial port message sent to controller')
            # time.sleep(float(self.config.get('serialport', 'pauseforresponse'))) # give the serial port
            # sometime to receive the data we don't need this now as we have a timeout which will pause
            # for 500m/s

            # A simple timeout
            timeout = self.config.get('serialport', 'timeout')
            current_time = datetime.datetime.now()
            timeout_time = current_time + datetime.timedelta(0, int(timeout))

            inbuff = 0

            logger.debug('Starting new serial port receive loop')

            # serial port receive loop

            while True:
                logger.debug("%s %s", "Serial port input buffer data - ", inbuff)

                if timeout_time >= datetime.datetime.now():
                    time.sleep(0.5)  # we sleep to stop race condition.
                    pass
                else:
                    ser.close()
                    return 'TIMEOUT'

                inbuff = ser.inWaiting()  # Wait for data

                if inbuff == 0:
                    pass
                elif inbuff > 0:  # If inbuff has data proceed

                    logger.debug("%s %s", "Serial port inbuffer size - ", inbuff)

                    received = ser.readline()

                    logger.info("Data received from staribus instrument")
                    logger.debug("%s %s", "Serial port received rawdata  -", repr(received))

                    received = received.decode('utf-8').strip('\x16\x02\x04\x0D\x0A')

                    logger.debug("%s %s", "Serial port message decoded - ", repr(received))

                    ser.close()

                    logger.debug('Serial port closed')

                    return received  # This returns the received response from the controller minus ctrl chars

        except IOError as msg:
            logger.critical('Serial IO Error - %s', msg)
            raise IOError()
        except TypeError as msg:
            logger.debug('Serial TypeError check the controller is connected? - %s', msg)
            logger.critical('Serial port error check the controller is connected?')
            raise IOError()


    def ctrlB(self):

        '''send ctrl-B 10 times to enable setting of controller baud rate.
         Currently doesn't work so don't use it unless you want to fix it. ;-))
        '''

        logger.info('ctrlB')

        try:
            ser.open()
            logger.debug('Serial port opened')
            ser.flushInput()  # flush input buffer, discarding all its contents
            logger.debug('Serial port input buffer flushed')
            ser.flushOutput()  # flush output buffer, aborting current output
            logger.debug('Serial port output buffer flushed')
            message = b'\x04\x04\x04\x04\x04\x04\x04\x04\x04\x04'
            logger.info("Sending data to staribus instrument")
            logger.debug("%s %s", 'Serial port raw message encoded utf-8', repr(message))
            ser.write(message)  # write message to serial port, preceded
            logger.debug('Serial port message sent to controller')
            time.sleep(float(self.config.get('serialport', 'pauseforresponse'))) # give the serial port
            #  sometime to receive the data

            inbuff = 0

            # serial port receive loop

            ## http://stackoverflow.com/questions/22275079/pyserial-write-wont-take-my-string

            while 1:
                logger.debug("%s %s", "Serial port input buffer data - ", inbuff)
                logger.debug('Starting new serial port receive loop')

                inbuff = ser.inWaiting()  # Wait for data

                if inbuff > 0:  # If inbuff has data proceed

                    logger.debug("%s %s", "Serial port inbuffer size - ", inbuff)

                    received = ser.readline()

                    logger.info("Data received from staribus instrument")
                    logger.debug("%s %s", "Serial port received rawdata  -", repr(received))

                    received = received.decode('utf-8').strip('\x16\x02\x04\x0D\x0A')

                    logger.debug("%s %s", "Serial port message decoded - ", repr(received))

                    self.parent.statusMessage.setText(repr(received))

                    ser.close()

                    logger.debug('Serial port closed')

                    return (received)  # This returns the received response from the controller minus ctrl chars
                else:
                    logger.debug("Serial port buffer empty - exiting serial port receive loop")

                    ser.close()

                    logger.debug('Serial port closed')

                    self.parent.statusMessage.setText('Error - Serial Port Timeout!!')

        except IOError as msg:
            logger.critical('Serial IO Error - %s', msg)
            raise IOError()
        except TypeError as msg:
            logger.debug('Serial TypeError check the controller is connected? - %s', msg)
            logger.critical('Serial port error check the controller is connected?')
            raise IOError()
