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

'''
Regex for ConfigLoader text line edits.

'''

observatory_name = '^([a-zA-Z0-9\'., ])*$'
observatory_description = '^([a-zA-Z0-9\'.,/ \\-])*$'
observatory_email = '^.*$'
observatory_telephone = '^.*$'
observatory_url = '^.*$'
observatory_country = '^[A-Z][A-Z]$'
observatory_timezone = '^.*$'
observatory_datum = '^(WGS84)|(EGM96)$'
observatory_geomag_model = '^.*$'
observatory_geomag_latitude = '^.*$'
observatory_geomag_longitude = '^.*$'
observatory_latitude = '^.*$'
observatory_longitude = '^.*$'
observatory_hasl = '^.*$'

observer_name = '^([a-zA-Z0-9\'., ])*$'
observer_description = '^([a-zA-Z0-9\'.,/ \\-])*$'
observer_email = '^.*$'
observer_telephone = '^.*$'
observer_url = '^.*$'
observer_country = '^[A-Z][A-Z]$'
observer_notes = '^([a-zA-Z0-9\'.,/ \\-])*$'

staribus_port = '^.*$'

starinet_ip = '^((([01]?[0-9]?[0-9]|2[0-4][0-9]|25[0-5])[ (\[]?(\.)[ )\]]?){3}([01]?[0-9]?[0-9]|2[0-4][0-9]|25[0-5]))$'
starinet_port = '^([1-9][0-9]{0,3}|[1-5][0-9]{4}|6[0-4][0-9]{3}|65[0-4][0-9]{2}|655[0-2][0-9]|6553[0-5])$'

windows_path = '^.*$'
unix_path = '^.*$'

channel_name = '^.*$'
channel_hex_color = '^#([A-F0-9]{6})$'
