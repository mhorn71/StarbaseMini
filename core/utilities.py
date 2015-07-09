__author__ = 'mark'

import socket
import re
import sys
import crcmod

# Set crc16 parameters to polynomial 8408, initial value 0xffff, reversed True, Final XOR value 0x00
crc16 = crcmod.mkCrcFun(0x018408, 0xFFFF, True, 0x0000)


def exit_message(message):
    '''
    Display CmdLine Message then sys.exit(1).
    :param message: string
    '''

    print('\nFatal Error - Check log file for further details. %s' % message)
    sys.exit(1)


def ip_checker(ip):
    '''
    Checks IP address looks for correct it' 100% full proof but should be fine on Win, Linux, OSX
    :param ip: IPv4 Address
    :return: True or False
    '''

    # From socket API inet_aton: https://docs.python.org/3/library/socket.html
    # If the IPv4 address string passed to this function is invalid, OSError will be raised.
    # Note, exactly what is valid depends on the underlying C implementation of inet_aton().

    try:
        socket.inet_aton(ip)
        return True
    except OSError:
        return False


def port_checker(port):
    '''
    Check network port range is between 1 - 65535
    :param port:
    :return: True or False
    '''

    if re.match('^([1-9][0-9]{0,3}|[1-5][0-9]{4}|6[0-4][0-9]{3}|65[0-4][0-9]{2}|655[0-2][0-9]|6553[0-5])$', port):
        return True
    else:
        return False

response_message_status = [('SUCCESS', b'0000'),
                           ('TIMEOUT', b'0001'),
                           ('ABORT', b'0002'),
                           ('PREMATURE_TERMINATION', b'0004'),
                           ('INVALID_PARAMETER', b'0008'),
                           ('INVALID_MESSAGE', b'0010'),
                           ('INVALID_COMMAND', b'0020'),
                           ('INVALID_MODULE', b'0040'),
                           ('INVALID_INSTRUMENT', b'0080'),
                           ('MODULE_DATABUS', b'0100'),
                           ('CRC_ERROR', b'0200'),
                           ('INVALID_XML', b'0400'),
                           ('ERROR_12', b'0800'),
                           ('ERROR_13', b'1000'),
                           ('LOOK_AT_ME', b'2000'),
                           ('BUSY', b'4000'),
                           ('CAPTURE_ACTIVE', b'8000')]


def staribus_error(error_name):
    '''
    :param error_name: [SUCCESS, ABORT, CRC_ERROR] etc ...
    :return: byte string error code. e.g. b'8000'
    '''
    for name, error_code in iter(response_message_status):
        if name == error_name:
            return error_code


def staribus_status(message):

    '''
    :param message: 4 digit hex integer e.g. b'000A'
    :return: string consisting of status names or None
    '''

    response_message = []

    loop_logic = True
    try:
        message_int = int(message, 16)
    except TypeError:
        return None

    while True:
        for i in reversed(response_message_status):
            if int(i[1], 16) > message_int:
                pass
            elif 32768 == message_int:
                return 'SUCCESS - CAPTURE_ACTIVE'
            elif int(i[1], 16) <= message_int:
                if loop_logic is True:
                    response_message.append(i[0])
                    message_int -= int(i[1], 16)
                    if message_int is 0:
                        loop_logic = False
                else:

                    response_message = ' - '.join(reversed(response_message))

                    return response_message
            else:
                # This should never get returned as the CRC check should happen before this.
                return 'INVALID_STATUS_CODE'


def crc_check(buffer0):
    '''
     checks a received staribus message checksum.

     Note: the staribus protocol is used minus \x02\x04\x0D\x0A e.g. 010001000000200A80

     Returns: True if success or False if failure.
    '''


    buffer0 = buffer0.encode('UTF-8')

    rxcrc = buffer0[-4:]  # assign the received crc to rxcrc

    newrxcrc = str(hex(crc16(buffer0[:-4])).replace('x', '')[1:].zfill(4)).upper()  # new crc

    newrxcrc = newrxcrc.encode('UTF-8')


    #### Check old and new crc's match if they don't return string with 0200 crc error
    if newrxcrc != rxcrc:
        return False
    else:
        return True


def crc_create(buffer0):

    '''
     Returns checksum for the supplied data supplied data.

     Note: the supplied data must be everything after \x02 but before the last \x1F
    '''

    buffer0 = buffer0.encode('UTF-8')

    datacrc = str(hex(crc16(buffer0)).replace('x', '')[1:].zfill(4)).upper()

    return datacrc