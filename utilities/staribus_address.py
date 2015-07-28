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

import re


def check_staribus_address(address):
    '''
    Checks Staribus address is within 001 - 253
    :param address: staribus address string.
    :return: True or False

    Notes: 000 is reserved for virtual instruments such as Starinet instrument
    254 is reserved for discovery
    255 is reserved for address not assigned.
    All of which will return False.

    '''

    if address is not str:
        address = str(address)

    if re.match('^0*([1-9][0-9]?|1[0-9]{2}|2[0-4][0-9]|25[0-3])$', address):
        return True
    else:
        return False