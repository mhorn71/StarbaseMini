import sys
import glob
import logging
import time
import datetime
import io

import serial

import core.utilities as utils
from core.configuration.configLoader import confLoader

config = confLoader()


# This script was directly lifted from :
# http://stackoverflow.com/questions/12090503/listing-available-com-ports-with-python
# Modified darwin to search for tty.usb* not just tty*

def autodetect(address, baudrate):
    """Autodetects the serial port to which the Staribus Instrument is attached.

    Sets port in configuration file.
    """
    logger = logging.getLogger('core.staribusPortDetect.autodetect')

    logger.info('autodetect running.')

    if sys.platform.startswith('win'):
        ports = ['COM' + str(i + 1) for i in range(256)]

    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this is to exclude your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')

    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.usb*')
    else:
        raise EnvironmentError('Unsupported platform', str(sys.platform))

    result = []
    for port in ports:
        logger.info('Serial ports found.')
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass

    if len(result) is 0:
        logger.warning('No serial ports found!!')
    else:
        logger.debug('%s %s', 'Serial ports found', str(result))
        s.close()
        check_port(address, baudrate, result)


def check_port(address, baudrate, result):

    address = address.lstrip()  # Strip leading zeros

    address = hex(int(address)).strip('0x')  # Change str to int then to hex and strip 0x

    address = address.zfill(2)  # Pad address to two places with leading zero.

    logger = logging.getLogger('core.staribusPortDetect.check_port')

    staribus_message = address + '00010000'

    checksum = utils.crc_create(staribus_message)

    staribus_port_message = ('\x02' + staribus_message + checksum + '\x04\x0D\x0A').encode('utf-8')

    logger.debug('Raw Staribus message ' + repr(staribus_port_message))

    staribus_ports = []

    for port in result:

        logger.debug('Scanning port %s for Staribus instrument address %s' % (port,address))

        data = []

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

            logger.debug('Flushing serial I/O buffers')
            s.flushInput()  # flush input buffer, discarding all its contents
            s.flushOutput()  # flush output buffer, aborting current output

            logger.debug('%s %s', 'Writing message to serial port', str(port))
            s.write(staribus_port_message)

            while True:

                logger.debug('Within receive loop')

                if timeout_time >= datetime.datetime.now():
                    time.sleep(0.25)
                else:
                    logger.warning('%s %s', 'Timed out waiting for response from controller on port', str(port))
                    s.close()
                    break

                inbuff = s.inWaiting()  # Wait for data

                if inbuff == 0:
                    logging.warning('inbuff empty')
                elif inbuff > 0:

                    logger.debug('%s %s', 'Serial port buffer length - ', inbuff)
                    received = ser_io.readline()

                    if received is None:
                        print('Received is None')
                        pass
                    else:
                        logger.debug('%s %s', 'Received rawdata', str(repr(received)))
                        logger.debug('Decoding bytes utf-8, stripping ctrl chars')
                        received = received.strip('\x16\x02\x04\x0D\x0A')

                    if utils.crc_check(received) is True:
                        # The length of ping packet response. This is a bodge in case a loop back device is found.
                        # The current UKRAA controller will return the sent message with a status of success, which
                        # once you strip off the beginning and end control characters the message length should be 25
                        # chars long, if it isn't the device is probably a loop back device.
                        if inbuff == 25:
                            logger.debug('Appending %s to staribus port list' % port)
                            staribus_ports.append(port)
                            s.close()
                            break
                        else:
                            logger.debug('%s %s', 'Looks like a loop back device dropping', port)
                            s.close()
                            break

        except serial.SerialException:
            pass

    logger.debug('Number of Staribus Ports found %s' % str(len(staribus_ports)))
    if len(staribus_ports) == 0:
        logger.critical('Staribus Port Autodetect - No instrument found on port.')
    elif len(staribus_ports) == 1:
        logger.info('%s %s', 'Staribus instrument found on port', str(staribus_ports))
        real_port = str(staribus_ports).strip('[\']')
        logger.debug('Writing port %s to configuration file', real_port)
        config.set('StaribusPort', 'port', real_port)
    elif len(staribus_ports) > 1:
        logger.info('%s %s', 'Multiple instruments found on ports', str(staribus_ports))
        logger.info('%s %s', 'Setting instrument to use first valid port', str(staribus_ports[0]))
        real_port = str(staribus_ports[0]).strip('[\']')
        logger.debug('Writing port %s to configuration file', real_port)
        config.set('StaribusPort', 'port', real_port)





