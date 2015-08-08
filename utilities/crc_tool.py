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

import crcmod

# Set crc16 parameters to polynomial 8408, initial value 0xffff, reversed True, Final XOR value 0x00
crc16 = crcmod.mkCrcFun(0x018408, 0xFFFF, True, 0x0000)


def check_crc(buffer0):

    '''
     checks a received staribus message checksum.
     Note: the staribus protocol is used minus \x02\x04\x0D\x0A e.g. 010001000000200A80
           if the message has parameters strip last \x1F as well.
     Returns: True if success or False if failure.
    '''

    buffer0 = buffer0.encode('UTF-8')

    rxcrc = buffer0[-4:]  # assign the received crc to rxcrc

    newrxcrc = str(hex(crc16(buffer0[:-4])).replace('x', '')[1:].zfill(4)).upper()  # new crc

    newrxcrc = newrxcrc.encode('UTF-8')

    # Check old and new crc's match if they don't return string with 0200 crc error
    if newrxcrc != rxcrc:
        return False
    else:
        return True


def create_crc(buffer0):

    '''
     Returns checksum for the supplied data supplied data.

     Note: the supplied data must be everything after \x02 but before the last \x1F
    '''

    buffer0 = buffer0.encode('UTF-8')

    datacrc = str(hex(crc16(buffer0)).replace('x', '')[1:].zfill(4)).upper()

    return datacrc
