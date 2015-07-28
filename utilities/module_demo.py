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

import utilities

message = b'8001'

response = utilities.staribus_status_b2str(message)
status_message = utilities.staribus_status_str2b('TIMEOUT')

print('Staribus Bytes to String : ' + response)
print('Staribus String to Bytes : ' + repr(status_message))

try:
    rgbcolour = utilities.hex2rgb('#FFFFFF')
    hexcolour = utilities.rgb2hex((255, 255, 255))
except ValueError as msg:
    print(msg)
else:
    print('Hex Colour to RGB : ' + repr(rgbcolour))
    print('RGB Colour to Hex : ' + repr(hexcolour))

if utilities.check_starinet_port('1205'):
    print('Starinet Port : valid')
else:
    print('Starinet Port : invalid')

if utilities.check_ip('192.168.1.1'):
    print('Starinet Address : valid')
else:
    print('Starinet Address : invalid')

if utilities.check_staribus_address('253'):
    print('Staribus Address : valid')
else:
    print('Staribus Address : invalid')

serial_port = utilities.serial_port_scanner()

if serial_port is not None:
    print('Serial port found : ' + str(serial_port))
else:
    print('No serial ports found')

if serial_port is not None:
    instrument_port = utilities.check_serial_port_staribus_instrument('001', serial_port, '57600')
    if instrument_port is not None:
        print('Staribus Instrument/s on port/s :' + str(instrument_port))
    else:
        print('No Staribus Instrument attached.')
