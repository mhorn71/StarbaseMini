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
import re


def check_ip(ip):

    '''
    Checks IP address looks for correct it's not 100% full proof but should be fine on Win, Linux, OSX
    :param: IPv4 Address string
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


def check_starinet_port(port):

    '''
    Check network port range is between 1 - 65535
    :param: string port number
    :return: True or False
    '''

    if port is str:
        pass
    else:
        port = str(port)

    if re.match('^([1-9][0-9]{0,3}|[1-5][0-9]{4}|6[0-4][0-9]{3}|65[0-4][0-9]{2}|655[0-2][0-9]|6553[0-5])$', port):
        return True
    else:
        return False
