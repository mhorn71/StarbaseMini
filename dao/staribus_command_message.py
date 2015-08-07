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

# look at Starbase StaribusCommandMessage.java

# **************************************************************************************************
#     Request with no parameters, length 15 before EOT
# 
#     Header          STX
#     Address         char char  in Hex
#     CommandCode     char char char char
#     CommandVariant  char char char char
#     CrcChecksum     char char char char  in Hex
#     Terminator      EOT CR LF
# 
# **************************************************************************************************
#     Request with Parameters
# 
#     Header          STX
#     Address         char char  in Hex
#     CommandCode     char char char char
#     CommandVariant  char char char char
#     Separator       US
#     Parameters      char char {char char ..} US          parameter 0
#                     char char {char char ..} US          parameter 1
#     CrcChecksum     char char char char  in Hex
#     Terminator      EOT CR LF
# 
# ***************************************************************************************************
# StaribusCommandMessage.