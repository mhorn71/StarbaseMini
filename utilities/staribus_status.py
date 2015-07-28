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


def staribus_status_str2b(error_name):

    '''
    :param error_name: [SUCCESS, ABORT, CRC_ERROR] etc ...
    :return: byte string error code. e.g. b'8000'
    '''
    for name, error_code in iter(response_message_status):
        if name == error_name:
            return error_code


def staribus_status_b2str(message):

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

