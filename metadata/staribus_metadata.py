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

import utilities


class StaribusMetaDataCreator:
    def __init__(self, parent):
        self.config = parent.config
        self.instrument = parent.instrument

    def observatory_metadata(self):
        name = self.config.get('ObservatoryMetadata', 'name')
        description = self.config.get('ObservatoryMetadata', 'description')
        email = self.config.get('ObservatoryMetadata', 'contact_email')
        telephone = self.config.get('ObservatoryMetadata', 'contact_telephone')
        url = self.config.get('ObservatoryMetadata', 'contact_url')
        country = self.config.get('ObservatoryMetadata', 'country')
        timezone = self.config.get('ObservatoryMetadata', 'timezone')
        datum = self.config.get('ObservatoryMetadata', 'geodetic_datum')
        maglat = self.config.get('ObservatoryMetadata', 'geomagnetic_latitude')
        maglon = self.config.get('ObservatoryMetadata', 'geomagnetic_longitude')
        magmodel = self.config.get('ObservatoryMetadata', 'geomagnetic_model')
        lat = self.config.get('ObservatoryMetadata', 'latitude')
        lon = self.config.get('ObservatoryMetadata', 'longitude')
        hasl = self.config.get('ObservatoryMetadata', 'hasl')

        metadata = ''

        if name is not None:
            if len(metadata) != 0:
                metadata += '\r\n'

            metadata += 'Observatory.Name,' + name + ',String,Dimensionless,The name of the Observatory'

        if description is not None:
            if len(metadata) != 0:
                metadata += '\r\n'

            metadata += 'Observatory.Description,' + description + ',String,Dimensionless,The description of the ' \
                        'Observatory'

        if email is not None:
            if len(metadata) != 0:
                metadata += '\r\n'

            metadata += 'Observatory.Contact.Email,' + email + ',String,Dimensionless,The email address of the ' \
                        'Observatory'

        if telephone is not None:
            if len(metadata) != 0:
                metadata += '\r\n'

            metadata += 'Observatory.Contact.Telephone,' + telephone + ',String,Dimensionless,The Observatory ' \
                        'telephone number'

        if url is not None:
            if len(metadata) != 0:
                metadata += '\r\n'

            metadata += 'Observatory.Contact.URL,' + url + ',URL,Dimensionless,The Observatory website URL'

        if country is not None:
            if len(metadata) != 0:
                metadata += '\r\n'

            metadata += 'Observatory.Country,' + country + ',String,Dimensionless,The Country containing the ' \
                        'Observatory (ISO 3166)'

        if timezone is not None:
            if len(metadata) != 0:
                metadata += '\r\n'

            metadata += 'Observatory.TimeZone,' + timezone + ',TimeZone,Dimensionless,The TimeZone containing the ' \
                        'Observatory  GMT-23:59 to GMT+00:00 to GMT+23:59'

        if datum is not None:
            if len(metadata) != 0:
                metadata += '\r\n'

            metadata += 'Observatory.GeodeticDatum,' + datum + ',String,Dimensionless,The GeodeticDatum used by the ' \
                        'Observatory'

        if maglat is not None:
            if len(metadata) != 0:
                metadata += '\r\n'

            metadata += 'Observatory.GeomagneticLatitude,' + maglat + ',Latitude,DegMinSec,The GeomagneticLatitude ' \
                        'of the Observatory (North is positive) -89:59:59.9999 to +00:00:00.0000 to +89:59:59.9999'

        if maglon is not None:
            if len(metadata) != 0:
                metadata += '\r\n'

            metadata += 'Observatory.GeomagneticLongitude,' + maglon + ',Longitude,DegMinSec,The GeomagneticLongitude ' \
                        'of the Observatory (West is positive) -179:59:59.9999 to +000:00:00.0000 to +179:59:59.9999'

        if magmodel is not None:
            if len(metadata) != 0:
                metadata += '\r\n'

            metadata += 'Observatory.GeomagneticModel,' + magmodel + ',String,Dimensionless,The GeomagneticModel ' \
                        'used by the Observatory'

        if lat is not None:
            if len(metadata) != 0:
                metadata += '\r\n'

            metadata += 'Observatory.Latitude,' + lat + ',Latitude,DegMinSec,The Latitude of the Framework (North is ' \
                        'positive)  -89:59:59.9999 to +00:00:00.0000 to +89:59:59.9999'

        if lon is not None:
            if len(metadata) != 0:
                metadata += '\r\n'

            metadata += 'Observatory.Longitude,' + lon + ',Longitude,DegMinSec,The Longitude of the Observatory ' \
                        '(West is positive)  -179:59:59.9999 to +000:00:00.0000 to +179:59:59.9999'

        if hasl is not None:
            if len(metadata) != 0:
                metadata += '\r\n'

            metadata += 'Observatory.HASL,' + hasl + ',DecimalFloat,m,The Height of the Observatory above Sea Level ' \
                        'in metres'

        if len(metadata) != 0:
            metadata += '\r\n'
            return metadata
        else:
            return None

    def observer_metadata(self):
        name = self.config.get('ObserverMetadata', 'name')
        description = self.config.get('ObserverMetadata', 'description')
        email = self.config.get('ObserverMetadata', 'contact_email')
        telephone = self.config.get('ObserverMetadata', 'contact_telephone')
        url = self.config.get('ObserverMetadata', 'contact_url')
        country = self.config.get('ObserverMetadata', 'country')
        notes = self.config.get('ObserverMetadata', 'notes')

        metadata = ''

        if name is not None:
            if len(metadata) != 0:
                metadata += '\r\n'

            metadata += 'Observer.Name,' + name + ',String,Dimensionless,The name of the Observer'

        if description is not None:
            if len(metadata) != 0:
                metadata += '\r\n'

            metadata += 'Observer.Description,' + description + ',String,Dimensionless,The description of the ' \
                        'Observer'

        if email is not None:
            if len(metadata) != 0:
                metadata += '\r\n'

            metadata += 'Observer.Contact.Email,' + email + ',String,Dimensionless,The email address of the Observer'

        if telephone is not None:
            if len(metadata) != 0:
                metadata += '\r\n'

            metadata += 'Observer.Contact.Telephone,' + telephone + ',String,Dimensionless,The Observer ' \
                        'telephone number'

        if url is not None:
            if len(metadata) != 0:
                metadata += '\r\n'

            metadata += 'Observer.Contact.URL,' + url + ',URL,Dimensionless,The Observer website URL'

        if country is not None:
            if len(metadata) != 0:
                metadata += '\r\n'

            metadata += 'Observer.Country,' + country + ',String,Dimensionless,The Country containing the Observer'

        if notes is not None:
            if len(metadata) != 0:
                metadata += '\r\n'

            metadata += 'Observer.Notes,' + notes + ',String,Dimensionless,The Observer Notes'

        if len(metadata) != 0:
            metadata += '\r\n'
            return metadata
        else:
            return None

    def observation_metadata(self):

        metadata = ''

        title = self.instrument.instrument_description
        count = self.instrument.instrument_number_of_channels
        xlabel = self.instrument.XaxisLabel
        ylabel = self.instrument.YaxisLabel

        if title != 'None':
            if len(metadata) != 0:
                metadata += '\r\n'

            metadata += 'Observation.Title,' + title + ',String,Dimensionless,The title of the observation.'

        if count != 'None':
            if len(metadata) != 0:
                metadata += '\r\n'

            metadata += 'Observation.Channel.Count,' + count + ',DecimalInteger,Dimensionless,The number of channels ' \
                        'of data produced by this Instrument'

        if xlabel != 'None':
            if len(metadata) != 0:
                metadata += '\r\n'

            metadata += 'Observation.Axis.Label.X,' + xlabel + ',String,Dimensionless,The X Axis Label'

        if ylabel != 'None':
            if len(metadata) != 0:
                metadata += '\r\n'

            metadata += 'Observation.Axis.Label.Y.0,' + ylabel + ',String,Dimensionless,The Y Axis Label'

        nameidx = 0
        for name in self.instrument.channel_names:

            if name != 'None':
                if len(metadata) != 0:
                    metadata += '\r\n'

                if nameidx == 0:
                    chanid = 'Temperature'
                else:
                    chanid = str(nameidx - 1)

                metadata += 'Observation.Channel.Name.' + chanid + ',' + name + ',String,Dimensionless,The name of the ' \
                            'channel'

                nameidx += 1

        colouridx = 0
        for colour in self.instrument.channel_colours:

            if colour != 'None':
                if len(metadata) != 0:
                    metadata += '\r\n'

                if colouridx == 0:
                    chanid = 'Temperature'
                else:
                    chanid = str(colouridx - 1)

                rgbcolour = utilities.hex2rgb(colour)

                red = str(rgbcolour[0]).zfill(3)
                grn = str(rgbcolour[1]).zfill(3)
                blu = str(rgbcolour[2]).zfill(3)

                metadata += 'Observation.Channel.Colour.' + chanid + ',r=' + red + ' g=' + grn + ' b=' + blu + ',' \
                            'ColourData,Dimensionless,The Colour of the channel graph'

                colouridx += 1

        dataidx = 0
        for datatype in self.instrument.channel_datatypenames:

            if datatype != 'None':
                if len(metadata) != 0:
                    metadata += '\r\n'

                if dataidx == 0:
                    chanid = 'Temperature'
                else:
                    chanid = str(dataidx - 1)

                metadata += 'Observation.Channel.DataType.' + chanid + ',' + datatype + ',DataType,Dimensionless,' \
                            'The DataType of the channel'

                dataidx += 1

        unitidx = 0
        for unit in self.instrument.channel_units:

            if unit != 'None':
                if len(metadata) != 0:
                    metadata += '\r\n'

                if unitidx == 0:
                    chanid = 'Temperature'
                else:
                    chanid = str(unitidx - 1)

                metadata += 'Observation.Channel.Units.' + chanid + ',' + unit + ',Units,Dimensionless,' \
                            'The Units of the channel'

                unitidx += 1

        if len(metadata) != 0:
            metadata += '\r\n'
            return metadata
        else:
            return None


class StaribusMetaDataDeconstructor:
    def __init__(self, parent):
        self.parent = parent
        self.instrument = parent.instrument

        self.instrument_identifier = None

        self.channel_count = None

        # We'll use the below list to save the channel names and colours and then populate the real lists from this.
        self.base_channel_names = [None] * 9
        self.base_channel_colours = [None] * 9

        # The metadata channel list see below for format etc ...
        self.channel_names = []

        # The metadata channel colour list
        self.channel_colours = []

        self.YaxisLabel = None

        self.XaxisLabel = None

        self.name_idx = 0
        self.colour_idx = 0

        self.name_trip = False
        self.colour_trip = False

    def clear(self):

        self.instrument_identifier = None

        self.channel_count = None

        # We'll use the below list to save the channel names and colours and then populate the real lists from this.
        self.base_channel_names = [None] * 9
        self.base_channel_colours = [None] * 9

        # The metadata channel list see below for format etc ...
        self.channel_names = []

        # The metadata channel colour list
        self.channel_colours = []

        self.YaxisLabel = None

        self.XaxisLabel = None

        self.name_idx = 0
        self.colour_idx = 0
        self.name_trip = False
        self.colour_trip = False

    def meta_parser(self, data):

        if re.match('^Observation\.Channel\.Count$', data[0]):
            self.channel_count = data[1]

        if re.match('^Observation\.Title$', data[0]):
            self.instrument_identifier = data[1]

        if re.match('^Observation\.Axis\.Label\.X$', data[0]):
            self.XaxisLabel = data[1]

        if re.match('^Observation\.Axis\.Label\.Y\.0$', data[0]):
            self.YaxisLabel = data[1]

        # Channel 1 is the temperature while the data channels start from channel 2 but are referenced in metadata as
        # Channels 0 - 8

        if re.match('^Observation\.Channel\.Name\.Temperature$', data[0]):
            self.base_channel_names[0] = data[1]
            self.name_idx += 1

        if re.match('^Observation\.Channel\.Colour\.Temperature$', data[0]):
            hex_colour = self.colour_setter(data[1])

            if hex_colour is not None:
                self.base_channel_colours[0] = hex_colour

            self.colour_idx += 1

        if re.match('^Observation\.Channel\.Name\.0$', data[0]):
            self.base_channel_names[1] = data[1]
            self.name_idx += 1

        if re.match('^Observation\.Channel\.Colour\.0$', data[0]):
            hex_colour = self.colour_setter(data[1])

            if hex_colour is not None:
                self.base_channel_colours[1] = hex_colour

            self.colour_idx += 1

        if re.match('^Observation\.Channel\.Name\.1$', data[0]):
            self.base_channel_names[2] = data[1]
            self.name_idx += 1

        if re.match('^Observation\.Channel\.Colour\.1$', data[0]):
            hex_colour = self.colour_setter(data[1])

            if hex_colour is not None:
                self.base_channel_colours.insert(2, hex_colour)

            self.colour_idx += 1

        if re.match('^Observation\.Channel\.Name\.2$', data[0]):
            self.base_channel_names[3] = data[1]
            self.name_idx += 1

        if re.match('^Observation\.Channel\.Colour\.2$', data[0]):
            hex_colour = self.colour_setter(data[1])

            if hex_colour is not None:
                self.base_channel_colours[3] = hex_colour

            self.colour_idx += 1

        if re.match('^Observation\.Channel\.Name\.3$', data[0]):
            self.base_channel_names[4] = data[1]
            self.name_idx += 1

        if re.match('^Observation\.Channel\.Colour\.3$', data[0]):
            hex_colour = self.colour_setter(data[1])

            if hex_colour is not None:
                self.base_channel_colours[4] = hex_colour

            self.colour_idx += 1

        if re.match('^Observation\.Channel\.Name\.4$', data[0]):
            self.base_channel_names[5] = data[1]
            self.name_idx += 1

        if re.match('^Observation\.Channel\.Colour\.4$', data[0]):
            hex_colour = self.colour_setter(data[1])

            if hex_colour is not None:
                self.base_channel_colours[5] = hex_colour

            self.colour_idx += 1

        if re.match('^Observation\.Channel\.Name\.5$', data[0]):
            self.base_channel_names.insert[6] = data[1]
            self.name_idx += 1

        if re.match('^Observation\.Channel\.Colour\.5$', data[0]):
            hex_colour = self.colour_setter(data[1])

            if hex_colour is not None:
                self.base_channel_colours[6] = hex_colour

            self.colour_idx += 1

        if re.match('^Observation\.Channel\.Name\.6$', data[0]):
            self.base_channel_names[7] = data[1]
            self.name_idx += 1

        if re.match('^Observation\.Channel\.Colour\.6$', data[0]):
            hex_colour = self.colour_setter(data[1])

            if hex_colour is not None:
                self.base_channel_colours[7] = hex_colour

            self.colour_idx += 1

        if re.match('^Observation\.Channel\.Name\.7$', data[0]):
            self.base_channel_names[8] = data[1]
            self.name_idx += 1

        if re.match('^Observation\.Channel\.Colour\.7$', data[0]):
            hex_colour = self.colour_setter(data[1])

            if hex_colour is not None:
                self.base_channel_colours[8] = hex_colour

            self.colour_idx += 1

        if re.match('^Observation\.Channel\.Name\.8$', data[0]):
            self.base_channel_names[9] = data[1]
            self.name_idx += 1

        if re.match('^Observation\.Channel\.Colour\.8$', data[0]):
            hex_colour = self.colour_setter(data[1])

            if hex_colour is not None:
                self.base_channel_colours[9] = hex_colour

            self.colour_idx += 1

        if self.channel_count is not None:
            if self.colour_idx == int(self.channel_count):
                if self.colour_trip is not True:
                    for i in self.base_channel_colours:
                        if i is not None:
                            self.channel_colours.append(i)
                    self.colour_trip = True

            if self.name_idx == int(self.channel_count):
                if self.name_trip is not True:
                    for i in self.base_channel_names:
                        if i is not None:
                            self.channel_names.append(i)
                    self.name_trip = True

    def colour_setter(self,rgb):
        # remove leading spaces.
        rgb_colour = rgb.lstrip()

        # split colours into tuple
        rgb_colour = rgb_colour.split(' ')

        if len(rgb_colour) != 3:
            return None

        r = rgb_colour[0][2:]
        g = rgb_colour[1][2:]
        b = rgb_colour[2][3:]

        hex_colour = utilities.rgb2hex((int(r), int(g), int(b)))

        return hex_colour
