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
# along with StarbaseMini.  If not, see <http:#www.gnu.org/licenses/>.

# todo add imports here.

# look at Starbase StaribusResponseMessage.java

# **************************************************************************************************
#    Response Only, or ErrorResponse for a Command which would expect a ResponseValue
#
#    Header          STX
#    Address         char char
#    CommandCode     char char char char
#    CommandVariant  char char char char
#    StatusCode      char char char char
#    CrcChecksum     char char char char  in Hex
#    Terminator      EOT CR LF
#
#    h n n n n n n n n n n n n n n n n n n e c l
#    i.e. must get at least 19 before looking for the terminator
#
# **************************************************************************************************
#    Response with Value
#
#    Header          STX
#    Address         char char
#    CommandCode     char char char char
#    CommandVariant  char char char char
#    StatusCode      char char char char
#    Separator       US
#    Value           char {char ..} US
#    CrcChecksum     char char char char  in Hex
#    Terminator      EOT CR LF
#
# ***************************************************************************************************