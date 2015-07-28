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

# http://stackoverflow.com/questions/214359/converting-hex-color-to-rgb-and-vice-versa
# Thanks to Jeremy Cantrell


def hex2rgb(value):

    '''
    Convert Hex colour to RGB
    :param value: '#FFFFFF'
    :return: (255, 255, 255)
    :raises: ValueError
    '''



    value = value.lstrip('#')

    hex_value = '0x' + value

    integer = int(hex_value, 16)

    if integer > 16777215:
        raise ValueError('Hex value out of range.')

    lv = len(value)
    return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))


def rgb2hex(rgb):

    '''
    Convert RGB Colour to Hex Colour.
    :param rgb: ((255, 255, 255))
    :return: '#FFFFFF'
    :raises: ValueError
    '''

    for i in rgb:
        if i > 255:
            raise ValueError('RGB value out of range.')

    return '#%02X%02X%02X' % rgb
