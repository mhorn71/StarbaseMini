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

# TODO DataTypeDictionary  requires a lot more decent logic testing.

def DataTypeConverter(datatype, data):

    # Datatype              # Format     # Base # Size #
    ####################################################
    # None                  # None       # None # None  - Implemented
    # HexInteger            # ABCD       # 16   # 4     - Implemented
    # HexDigit              # A          # 16   # 1
    # UnsignedHexByte       # FF         # 16   # 2
    # SignedHexByte         # -FF        # 16   # 3
    # DecimalInteger        # 9999       # 10   # 4     - Implemented
    # DecimalDigit          # 7          # 10   # 1     - Implemented
    # DecimalFloat          # 1.23       # 10   # 50
    # DecimalDouble         # -1.123E-04 # 10   # 50
    # UnsignedDecimalByte   # 255        # 10   # 3     - Implemented
    # SignedDecimalByte     # -255       # 10   # 4
    # Boolean               # Y/N        # None # 1     - Implemented
    # String                # *          # None # ?     - Implemented
    # NumericIndexedList    #

    if datatype == 'None':

        return data

    elif datatype == 'HexInteger':

        if re.match('^[0-9A-F][0-9A-F][0-9A-F][0-9A-F]$', data):

            return data

        elif re.match('^[0-9A-F][0-9A-F][0-9A-F]$', data):

            return data.zfill(4)

        elif re.match('^[0-9A-F][0-9A-F]$', data):

            return data.zfill(4)

        elif re.match('^[0-9A-F]$', data):

            return data.zfill(4)

        else:

            return None

    elif datatype == 'DecimalInteger':

        data = data.zfill(4)

        if len(data) == 4:

            return data

        else:

            return None

    elif datatype == 'DecimalDigit':

        data = data.lstrip('0')

        if len(data) == 1:

            return data

        else:

            return None

    elif datatype == 'UnsignedDecimalByte':

        if len(data) > 1:
            data = data.lstrip('0')

        if len(data) >= 1 and len(data) <= 3:

            return data.zfill(3)

        else:

            return None


    elif datatype == 'Boolean':

        if re.match('^True$|^true', data):

            return 'Y'

        elif re.match('^False$|^false$', data):

            return 'N'

        else:

            return None

    elif datatype == 'String':

        #  Return string all lowercase.

        data = data.lower()

        return data






