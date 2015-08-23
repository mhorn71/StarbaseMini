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

class MetaData:
    def __init__(self, parent):
        self.config = parent.config
        self.instrument = parent.instrument

    def starbase_metadata(self):
        # self.config.get()
        pass
        # Reference
        # [ObservatoryMetadata]
        # name = Wards Hill Observatory
        # description = Radio Telescope
        # contact_email = someone@wardshillobservatory.com
        # contact_telephone = +44 123 1234567
        # contact_url = http://wardshillobservatory.co.uk
        # country = GB
        # timezone = UTC
        # geodetic_datum = WGS84
        # geomagnetic_latitude = +00:00:00.000
        # geomagnetic_longitude = +000:00:00.000
        # geomagnetic_model = IGRF-11
        # latitude = +00:00:00.000
        # longitude = +000:00:00.000
        # hasl = 32.0
        #
        # [ObserverMetadata]
        # name = Oculo Gyric
        # description = The really observant Observer
        # contact_email = Oculo@gyric.com
        # contact_telephone = +44 123 1234567
        # contact_url = http://github.com/mhorn71/StarbaseMini
        # country = GB
        # notes = The Observer Notes
