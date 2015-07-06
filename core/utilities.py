__author__ = 'mark'

import socket
import re
import sys

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
