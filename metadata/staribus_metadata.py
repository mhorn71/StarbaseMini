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
import logging
import utilities

meta_data_a = ['Observatory.Name','name','String','Dimensionless','The name of the Observatory']

meta_data_b = ['Observatory.Description', 'description', 'String', 'Dimensionless', 'The description of the Observatory']

meta_data_c = ['Observatory.Contact.Email', 'email', 'String', 'Dimensionless', 'The email address of the Observatory']

meta_data_d = ['Observatory.Contact.Telephone', 'telephone', 'String', 'Dimensionless', 'The Observatory telephone number']

meta_data_e = ['Observatory.Contact.URL', 'url', 'URL', 'Dimensionless', 'The Observatory website URL']

meta_data_f = ['Observatory.Country', 'country', 'String', 'Dimensionless', 'The Country containing the Observatory (ISO 3166)']

meta_data_g = ['Observatory.TimeZone', 'timezone', 'TimeZone', 'Dimensionless', 'The TimeZone containing the Observatory GMT-23:59 to GMT+00:00 to GMT+23:59']

meta_data_h = ['Observatory.GeodeticDatum', 'datum', 'String', 'Dimensionless', 'The GeodeticDatum used by the Observatory']

meta_data_i = ['Observatory.GeomagneticLatitude', 'maglat', 'Latitude', 'DegMinSec', 'The GeomagneticLatitude of the Observatory (North is positive) -89:59:59.9999 to +00:00:00.0000 to +89:59:59.9999']

meta_data_j = ['Observatory.GeomagneticLongitude', 'maglon', 'Longitude', 'DegMinSec', 'The GeomagneticLongitude of the Observatory (West is positive) -179:59:59.9999 to +000:00:00.0000 to +179:59:59.9999']

meta_data_k = ['Observatory.GeomagneticModel','magmodel','String','Dimensionless','The GeomagneticModel used by the Observatory']

meta_data_l = ['Observatory.Latitude', 'lat', 'Latitude', 'DegMinSec', 'The Latitude of the Framework (North is positive) -89:59:59.9999 to +00:00:00.0000 to +89:59:59.9999']

meta_data_m = ['Observatory.Longitude', 'lon', 'Longitude', 'DegMinSec', 'The Longitude of the Observatory (West is positive) -179:59:59.9999 to +000:00:00.0000 to +179:59:59.9999']

meta_data_n = ['Observatory.HASL', 'hasl', 'DecimalFloat', 'The Height of the Observatory above Sea Level in metres']

meta_data_aa = ['Observer.Name','name','String','Dimensionless','The name of the Observer']

meta_data_ab = ['Observer.Description','description','String','Dimensionless','The description of the Observer']

meta_data_ac = ['Observer.Contact.Email','email','String','Dimensionless','The email address of the Observer']

meta_data_ad = ['Observer.Contact.Telephone','telephone','String','Dimensionless','The Observer telephone number']

meta_data_ae = ['Observer.Contact.URL','url','URL','Dimensionless','The Observer website URL']

meta_data_af = ['Observer.Country','country','String','Dimensionless','The Country containing the Observer']

meta_data_ag = ['Observer.Notes','notes','String','Dimensionless','The Observer Notes']

meta_data_ba = ['Observation.Title', 'title', 'String', 'Dimensionless', 'The title of the observation.']

meta_data_bb = ['Observation.Channel.Count', 'count', 'DecimalInteger', 'Dimensionless', 'The number of channels of data produced by this Instrument']

meta_data_bc = ['Observation.Axis.Label.X', 'xlabel', 'String', 'Dimensionless', 'The X Axis Label']

meta_data_bd = ['Observation.Axis.Label.Y.0', 'ylabel', 'String', 'Dimensionless', 'The Y Axis Label']

meta_data_be = ['Observation.Notes','note','String','Dimensionless','The Observation Notes']


def colour_setter(rgb):
    # remove leading spaces.
    rgb_colour = rgb.lstrip()

    # split colours into tuple
    rgb_colour = rgb_colour.split(' ')

    if len(rgb_colour) != 3:
        return None

    r = rgb_colour[0].strip('r=')
    g = rgb_colour[1].strip('g=')
    b = rgb_colour[2].strip('b=')

    hex_colour = utilities.rgb2hex((int(r), int(g), int(b)))

    return hex_colour


class StaribusMetaData:
    def __init__(self, parent):

        logger = logging.getLogger('StaribusMetaData')

        self.application_configuration = parent.application_configuration

        self.data_store = parent.data_store

        self.instrument = parent.instrument

        self.instrument_identifier = None

        self.instrument_number_of_channels = None

        # We'll use the below list to save the channel names and colours and then populate the real lists from this.
        self.channel_names = ['NO_DATA'] * 9

        self.channel_colours = ['#E31A1C', '#A6CEE3', '#1F78B4', '#B2DF8A', '#33A02C', '#F69A99', '#FDBF6F', '#FF7F00',
                                '#CAB2D6']

        self.channel_datatypenames = ['NO_DATA'] * 9

        self.channel_units = ['NO_DATA'] * 9

        self.YaxisLabel = 'NO_DATA'

        self.XaxisLabel = 'NO_DATA'

        self.ObservationNotes = None

        self.ObservatoryName = None
        self.ObservatorDescription = None
        self.ObservatoryEmail = None
        self.ObservatoryTelephone = None
        self.ObservatoryUrl = None
        self.ObservatoryCountry = None
        self.ObservatoryTimezone = None
        self.ObservatoryDatum = None
        self.ObservatoryMagLatitude = None
        self.ObservatoryMagLongitude = None
        self.ObservatoryMagModel = None
        self.ObservatoryLatitude = None
        self.ObservatoryLongitude = None
        self.ObservatoryHasl = None

        self.ObserverName = None
        self.ObserverDescription = None
        self.ObserverContactEmail = None
        self.ObserverContactTelephone = None
        self.ObserverContactUrl = None
        self.ObserverCountry = None
        self.ObserverNotes = None

        self.ObservationNotesChanged = False

        self.metadata = []

        logger.debug('Initialised')

    def clear(self):

        logger_clear = logging.getLogger('StaribusMetaData.clear')

        self.instrument_identifier = 'NO_DATA'
        logger_clear.debug('Instrument identifier set to None')

        # We'll use the below list to save the channel names and colours and then populate the real lists from this.
        self.channel_names.clear()
        logger_clear.debug('Deleting channel names')

        self.channel_colours.clear()
        logger_clear.debug('Deleting channel colours')

        self.channel_datatypenames.clear()
        logger_clear.debug('Deleting channel data type names')

        self.channel_units.clear()
        logger_clear.debug('Deleting channel units')

        self.channel_names = ['NO_DATA'] * 9
        logger_clear.debug('Channel names set to default n * 9 matrix')

        self.channel_colours = ['#E31A1C','#A6CEE3','#1F78B4','#B2DF8A','#33A02C','#F69A99','#FDBF6F','#FF7F00',
                                '#CAB2D6']
        logger_clear.debug('Channel colour set to default n * 9 matrix')

        self.channel_datatypenames = ['NO_DATA'] * 9
        logger_clear.debug('Channel data type names set to default n * 9 matrix')

        self.channel_units = ['NO_DATA'] * 9
        logger_clear.debug('BChannel units set to default n * 9 matrix')

        self.YaxisLabel = 'NO_DATA'
        logger_clear.debug('YaxisLabel set to NO_DATA')

        self.XaxisLabel = 'NO_DATA'
        logger_clear.debug('XaxisLabel set to NO_DATA')

        self.ObservationNotes = None
        logger_clear.debug('Observation notes set to None')

        self.ObservatoryName = None
        self.ObservatorDescription = None
        self.ObservatoryEmail = None
        self.ObservatoryTelephone = None
        self.ObservatoryUrl = None
        self.ObservatoryCountry = None
        self.ObservatoryTimezone = None
        self.ObservatoryDatum = None
        self.ObservatoryMagLatitude = None
        self.ObservatoryMagLongitude = None
        self.ObservatoryMagModel = None
        self.ObservatoryLatitude = None
        self.ObservatoryLongitude = None
        self.ObservatoryHasl = None

        self.ObserverName = None
        self.ObserverDescription = None
        self.ObserverContactEmail = None
        self.ObserverContactTelephone = None
        self.ObserverContactUrl = None
        self.ObserverCountry = None
        self.ObserverNotes = None

        self.ObservationNotes = None

        self.instrument_number_of_channels = None

        self.metadata.clear()



    def metadata_creator(self, source):

        self.metadata.clear()

        # Ok we need access to the application configuration to

        if source == 'Controller':

            ObservatoryName = self.application_configuration.get('ObservatoryMetadata', 'name')
            ObservatoryDescription = self.application_configuration.get('ObservatoryMetadata', 'description')
            ObservatoryEmail = self.application_configuration.get('ObservatoryMetadata', 'contact_email')
            ObservatoryTelephone = self.application_configuration.get('ObservatoryMetadata', 'contact_telephone')
            ObservatoryUrl = self.application_configuration.get('ObservatoryMetadata', 'contact_url')
            ObservatoryCountry = self.application_configuration.get('ObservatoryMetadata', 'country')
            ObservatoryTimezone = self.application_configuration.get('ObservatoryMetadata', 'timezone')
            ObservatoryDatum = self.application_configuration.get('ObservatoryMetadata', 'geodetic_datum')
            ObservatoryMaglat = self.application_configuration.get('ObservatoryMetadata', 'geomagnetic_latitude')
            ObservatoryMaglon = self.application_configuration.get('ObservatoryMetadata', 'geomagnetic_longitude')
            ObservatoryMagmodel = self.application_configuration.get('ObservatoryMetadata', 'geomagnetic_model')
            ObservatoryLat = self.application_configuration.get('ObservatoryMetadata', 'latitude')
            ObservatoryLon = self.application_configuration.get('ObservatoryMetadata', 'longitude')
            ObservatoryHasl = self.application_configuration.get('ObservatoryMetadata', 'hasl')

            ObserverName = self.application_configuration.get('ObserverMetadata', 'name')
            ObserverDescription = self.application_configuration.get('ObserverMetadata', 'description')
            ObserverEmail = self.application_configuration.get('ObserverMetadata', 'contact_email')
            ObserverTelephone = self.application_configuration.get('ObserverMetadata', 'contact_telephone')
            ObserverUrl = self.application_configuration.get('ObserverMetadata', 'contact_url')
            ObserverCountry = self.application_configuration.get('ObserverMetadata', 'country')
            ObserverNotes = self.application_configuration.get('ObserverMetadata', 'notes')

            ObservationTitle = self.instrument.instrument_description
            ObservationCount = self.instrument.instrument_number_of_channels
            ObservationXlabel = self.instrument.XaxisLabel
            ObservationYlabel = self.instrument.YaxisLabel
            ObservationNotes = self.ObservationNotes

            channel_names = self.instrument.channel_names
            channel_colours = self.instrument.channel_colours
            channel_data_types = self.instrument.channel_datatypenames
            channel_units = self.instrument.channel_units

        elif source == 'CSV':

            ObservatoryName = self.ObservatoryName
            ObservatoryDescription = self.ObservatorDescription
            ObservatoryEmail = self.ObservatoryEmail
            ObservatoryTelephone = self.ObservatoryTelephone
            ObservatoryUrl = self.ObservatoryUrl
            ObservatoryCountry = self.ObservatoryCountry
            ObservatoryTimezone = self.ObservatoryTimezone
            ObservatoryDatum = self.ObservatoryDatum
            ObservatoryMaglat = self.ObservatoryMagLatitude
            ObservatoryMaglon = self.ObservatoryMagLongitude
            ObservatoryMagmodel = self.ObservatoryMagModel
            ObservatoryLat = self.ObservatoryLatitude
            ObservatoryLon = self.ObservatoryLongitude
            ObservatoryHasl = self.ObservatoryHasl

            ObserverName = self.ObserverName
            ObserverDescription = self.ObserverDescription
            ObserverEmail = self.ObserverContactEmail
            ObserverTelephone = self.ObserverContactTelephone
            ObserverUrl = self.ObserverContactUrl
            ObserverCountry = self.ObserverCountry
            ObserverNotes = self.ObserverNotes

            ObservationTitle = self.instrument_identifier
            ObservationCount = self.instrument_number_of_channels
            ObservationXlabel = self.XaxisLabel
            ObservationYlabel = self.YaxisLabel
            ObservationNotes = self.ObservationNotes

            channel_names = self.channel_names
            channel_colours = self.channel_colours
            channel_data_types = self.channel_datatypenames
            channel_units = self.channel_units

        else:

            return None

        source = self.instrument

    # Observatory Metadata.

        if ObservatoryName is not None:

            meta_data_a[1] = ObservatoryName

            self.metadata.append(meta_data_a)

        if ObservatoryDescription is not None:

            meta_data_b[1] = ObservatoryDescription

            self.metadata.append(meta_data_b)

        if ObservatoryEmail is not None:

            meta_data_c[1] = ObservatoryEmail

            self.metadata.append(meta_data_c)

        if ObservatoryTelephone is not None:

            meta_data_d[1] = ObservatoryTelephone

            self.metadata.append(meta_data_d)

        if ObservatoryUrl is not None:

            meta_data_e[1] = ObservatoryUrl

            self.metadata.append(meta_data_e)

        if ObservatoryCountry is not None:

            meta_data_f[1] = ObservatoryCountry

            self.metadata.append(meta_data_f)

        if ObservatoryTimezone is not None:

            if ObservatoryTimezone == 'UTC' or ObservatoryTimezone == 'utc':
                ObservatoryTimezone = 'GMT+00:00'

            meta_data_g[1] = ObservatoryTimezone

            self.metadata.append(meta_data_g)

        if ObservatoryDatum is not None:

            meta_data_h[1] = ObservatoryDatum

            self.metadata.append(meta_data_h)

        if ObservatoryMaglat is not None:

            meta_data_i[1] = ObservatoryMaglat

            self.metadata.append(meta_data_i)

        if ObservatoryMaglon is not None:

            meta_data_j[1] = ObservatoryMaglon

            self.metadata.append(meta_data_j)

        if ObservatoryMagmodel is not None:

            meta_data_k[1] = ObservatoryMagmodel

            self.metadata.append(meta_data_k)

        if ObservatoryLat is not None:

            meta_data_l[1] = ObservatoryLat

            self.metadata.append(meta_data_l)

        if ObservatoryLon is not None:

            meta_data_m[1] = ObservatoryLon

            self.metadata.append(meta_data_m)

        if ObservatoryHasl is not None:

            meta_data_n[1] = ObservatoryHasl

            self.metadata.append(meta_data_n)

    # Observer Metadata

        if ObserverName is not None:

            meta_data_aa[1] = ObserverName

            self.metadata.append(meta_data_aa)

        if ObserverDescription is not None:

            meta_data_ab[1] = ObserverDescription

            self.metadata.append(meta_data_ab)

        if ObserverEmail is not None:

            meta_data_ac[1] = ObserverEmail

            self.metadata.append(meta_data_ac)

        if ObserverTelephone is not None:

            meta_data_ad[1] = ObserverTelephone

            self.metadata.append(meta_data_ad)

        if ObserverUrl is not None:

            meta_data_ae[1] = ObserverUrl

            self.metadata.append(meta_data_ae)

        if ObserverCountry is not None:

            meta_data_af[1] = ObserverCountry

            self.metadata.append(meta_data_af)

        if ObserverNotes is not None:

            meta_data_ag[1] = ObserverNotes

            self.metadata.append(meta_data_ag)

    # Observation Metadata

        if ObservationTitle is not None:

            meta_data_ba[1] = ObservationTitle

            self.metadata.append(meta_data_ba)

        if ObservationCount is not None:

            meta_data_bb[1] = ObservationCount

            self.metadata.append(meta_data_bb)

        if ObservationXlabel is not None:

            meta_data_bc[1] = ObservationXlabel

            self.metadata.append(meta_data_bc)

        if ObservationYlabel is not None:

            meta_data_bd[1] = ObservationYlabel

            self.metadata.append(meta_data_bd)

        if ObservationNotes is not None:

            meta_data_be[1] = ObservationNotes

            self.metadata.append(meta_data_be)

        if ObservationCount is not None:

            count = ObservationCount

        elif self.data_store.channel_count is not None:

            count = self.data_store.channel_count

        else:

            return None

        for i in range(int(count)):

            channel_name_idx0 = 'Observation.Channel.Name.' + str(i - 1)
            channel_colour_idx0 = 'Observation.Channel.Colour.' + str(i - 1)
            channel_datatype_idx0 = 'Observation.Channel.DataType.' + str(i - 1)
            channel_unit_idx0 = 'Observation.Channel.Units.' + str(i - 1)

            channel_name_idx1 = channel_names[i]
            channel_datatype_idx1 = channel_data_types[i]
            channel_unit_idx1 = channel_units[i]

            rgbcolour = utilities.hex2rgb(channel_colours[i])

            red = str(rgbcolour[0]).zfill(3)
            grn = str(rgbcolour[1]).zfill(3)
            blu = str(rgbcolour[2]).zfill(3)

            channel_colour_idx1 = 'r=' + red + ' g=' + grn + ' b=' +blu

            if i == 0:

                self.metadata.append(['Observation.Channel.Name.Temperature', channel_name_idx1, 'String',
                                      'Dimensionless', 'The name of the channel'])

                self.metadata.append(['Observation.Channel.Colour.Temperature', channel_colour_idx1,
                                      'ColourData,Dimensionless', 'The Colour of the channel graph'])

                self.metadata.append(['Observation.Channel.DataType.Temperature', channel_datatype_idx1, 'DataType',
                                      'Dimensionless', 'The DataType of the channel'])

                self.metadata.append(['Observation.Channel.Units.Temperature', channel_unit_idx1, 'Units',
                                      'Dimensionless', 'The Units of the channel'])

            else:

                self.metadata.append([channel_name_idx0, channel_name_idx1, 'String', 'Dimensionless',
                                      'The name of the channel'])

                self.metadata.append([channel_colour_idx0, channel_colour_idx1, 'ColourData','Dimensionless',
                                      'The Colour of the channel graph'])

                self.metadata.append([channel_datatype_idx0, channel_datatype_idx1, 'DataType', 'Dimensionless',
                                      'The DataType of the channel'])

                self.metadata.append([channel_unit_idx0, channel_unit_idx1, 'Units', 'Dimensionless',
                                      'The Units of the channel'])

        if len(self.metadata) != 0:

            return self.metadata

        else:

            return None

    def meta_parser(self, data):

        logger_meta_parser = logging.getLogger('StaribusMetaDataDeconstructor.meta_parser')

        if re.match('^Observatory\.Name$', data[0]):
            logger_meta_parser.debug('Observatory name set to : %s' % str(data[1]))
            self.ObservatoryName = data[1]

        if re.match('^Observatory\.Description$', data[0]):
            logger_meta_parser.debug('Observatory description set to : %s' % str(data[1]))
            self.ObservatoryDescription = data[1]

        if re.match('^Observatory\.Contact\.Email$', data[0]):
            logger_meta_parser.debug('Observatory contact email set to : %s' % str(data[1]))
            self.ObservatoryEmail = data[1]

        if re.match('^Observatory\.Contact\.Telephone$', data[0]):
            logger_meta_parser.debug('Observatory contact telephone set to : %s' % str(data[1]))
            self.ObservatoryTelephone = data[1]

        if re.match('^Observatory\.Contact\.URL$', data[0]):
            logger_meta_parser.debug('Observatory contact URL set to : %s' % str(data[1]))
            self.ObservatoryUrl = data[1]

        if re.match('^Observatory\.Country$', data[0]):
            logger_meta_parser.debug('Observatory country set to : %s' % str(data[1]))
            self.ObservatoryCountry = data[1]

        if re.match('^Observatory\.TimeZone$', data[0]):
            logger_meta_parser.debug('Observatory timezone set to : %s' % str(data[1]))
            self.ObservatoryTimezone = data[1]

        if re.match('^Observatory\.GeodeticDatum$', data[0]):
            logger_meta_parser.debug('Observatory geodetic datum set to : %s' % str(data[1]))
            self.ObservatoryDatum = data[1]

        if re.match('^Observatory\.GeomagneticLatitude$', data[0]):
            logger_meta_parser.debug('Observatory geomagnetic latitude set to : %s' % str(data[1]))
            self.ObservatoryMagLatitude = data[1]

        if re.match('^Observatory\.GeomagneticLongitude$', data[0]):
            logger_meta_parser.debug('Observatory geomagnetic longitude set to : %s' % str(data[1]))
            self.ObservatoryMagLongitude = data[1]

        if re.match('^Observatory\.GeomagneticModel$', data[0]):
            logger_meta_parser.debug('Observatory geomagnetic model set to : %s' % str(data[1]))
            self.ObservatoryMagModel = data[1]

        if re.match('^Observatory\.Latitude$', data[0]):
            logger_meta_parser.debug('Observatory latitude set to : %s' % str(data[1]))
            self.ObservatoryLatitude = data[1]

        if re.match('^Observatory\.Longitude$', data[0]):
            logger_meta_parser.debug('Observatory longitude set to : %s' % str(data[1]))
            self.ObservatoryLongitude = data[1]

        if re.match('^Observatory\.HASL$', data[0]):
            logger_meta_parser.debug('Observatory HASL set to : %s' % str(data[1]))
            self.ObservatoryHasl = data[1]

        if re.match('^Observation\.Channel\.Count$', data[0]):
            logger_meta_parser.debug('Channel count set to : %s' % str(data[1]) )
            self.instrument_number_of_channels = data[1]


        if re.match('^Observer\.Name$', data[0]):
            logger_meta_parser.debug('Observer name set to : %s' % str(data[1]))
            self.ObserverName = data[1]

        if re.match('^Observer\.Description$', data[0]):
            logger_meta_parser.debug('Observer description set to : %s' % str(data[1]))
            self.ObserverDescription = data[1]

        if re.match('^Observer\.Contact\.Email$', data[0]):
            logger_meta_parser.debug('Observer contact email set to : %s' % str(data[1]))
            self.ObserverEmail = data[1]

        if re.match('^Observer\.Contact\.Telephone$', data[0]):
            logger_meta_parser.debug('Observer contact telephone set to : %s' % str(data[1]))
            self.ObserverTelephone = data[1]

        if re.match('^Observer\.Contact\.URL$', data[0]):
            logger_meta_parser.debug('Observer contact URL set to : %s' % str(data[1]))
            self.ObserverUrl = data[1]

        if re.match('^Observer\.Country$', data[0]):
            logger_meta_parser.debug('Observer country set to : %s' % str(data[1]))
            self.ObserverCountry = data[1]

        if re.match('^Observation\.Title$', data[0]):
            logger_meta_parser.debug('Observation title set to : %s' % str(data[1]))
            self.instrument_identifier = data[1]

        if re.match('^Observation\.Axis\.Label\.X$', data[0]):
            logger_meta_parser.debug('X Axis label set to : %s' % str(data[1]))
            self.XaxisLabel = data[1]

        if re.match('^Observation\.Axis\.Label\.Y\.0$', data[0]):
            logger_meta_parser.debug('Y Axis label set to : %s' % str(data[1]))
            self.YaxisLabel = data[1]

        if re.match('^Observation\.Notes$', data[0]):
            logger_meta_parser.debug('Observation notes set to : %s' % str(data[1]))
            self.ObservationNotes = data[1]

        # Channel 1 is the temperature while the data channels start from channel 2 but are referenced in metadata as
        # Channels 0 - 8

        if re.match('^Observation\.Channel\.Name\.Temperature$', data[0]):
            logger_meta_parser.debug('Channel temperature name set to : %s' % data[1])
            self.channel_names[0] = data[1]

        if re.match('^Observation\.Channel\.Colour\.Temperature$', data[0]):
            logger_meta_parser.debug('Channel temperature colour found : %s' % data[1])
            hex_colour = colour_setter(data[1])

            if hex_colour is not None:
                self.channel_colours[0] = hex_colour
                logger_meta_parser.debug('Channel temperature colour set to : %s' % hex_colour)

        if re.match('^Observation\.Channel\.DataType\.Temperature$', data[0]):
            logger_meta_parser.debug('Channel temperature datatype set to : %s' % data[1])
            self.channel_datatypenames[0] = data[1]

        if re.match('^Observation\.Channel\.Units\.Temperature$', data[0]):
            logger_meta_parser.debug('Channel temperature units set to : %s' % data[1])
            self.channel_units[0] = data[1]

        if re.match('^Observation\.Channel\.Name\.0$', data[0]):
            logger_meta_parser.debug('Channel name 0 set to : %s' % data[1])
            self.channel_names[1] = data[1]

        if re.match('^Observation\.Channel\.Colour\.0$', data[0]):
            logger_meta_parser.debug('Channel 0 colour found : %s' % data[1])
            hex_colour = colour_setter(data[1])

            if hex_colour is not None:
                self.channel_colours[1] = hex_colour
                logger_meta_parser.debug('Channel 0 colour set to : %s' % hex_colour)

        if re.match('^Observation\.Channel\.DataType\.0$', data[0]):
            logger_meta_parser.debug('Channel 0 datatype set to : %s' % data[1])
            self.channel_datatypenames[1] = data[1]

        if re.match('^Observation\.Channel\.Units\.0$', data[0]):
            logger_meta_parser.debug('Channel 0 units set to : %s' % data[1])
            self.channel_units[1] = data[1]

        if re.match('^Observation\.Channel\.Name\.1$', data[0]):
            logger_meta_parser.debug('Channel name 1 set to : %s' % data[1])
            self.channel_names[2] = data[1]

        if re.match('^Observation\.Channel\.Colour\.1$', data[0]):
            logger_meta_parser.debug('Channel 1 colour found : %s' % data[1])
            hex_colour = colour_setter(data[1])

            if hex_colour is not None:
                self.channel_colours.insert(2, hex_colour)
                logger_meta_parser.debug('Channel 1 colour set to : %s' % hex_colour)

        if re.match('^Observation\.Channel\.DataType\.1$', data[0]):
            logger_meta_parser.debug('Channel 1 datatype set to : %s' % data[1])
            self.channel_datatypenames[2] = data[1]

        if re.match('^Observation\.Channel\.Units\.1$', data[0]):
            logger_meta_parser.debug('Channel 1 units set to : %s' % data[1])
            self.channel_units[2] = data[1]

        if re.match('^Observation\.Channel\.Name\.2$', data[0]):
            logger_meta_parser.debug('Channel name 2 set to : %s' % data[1])
            self.channel_names[3] = data[1]

        if re.match('^Observation\.Channel\.Colour\.2$', data[0]):
            logger_meta_parser.debug('Channel 2 colour found : %s' % data[1])
            hex_colour = colour_setter(data[1])

            if hex_colour is not None:
                self.channel_colours[3] = hex_colour
                logger_meta_parser.debug('Channel 2 colour set to : %s' % hex_colour)

        if re.match('^Observation\.Channel\.DataType\.2$', data[0]):
            logger_meta_parser.debug('Channel 2 datatype set to : %s' % data[1])
            self.channel_datatypenames[3] = data[1]

        if re.match('^Observation\.Channel\.Units\.2$', data[0]):
            logger_meta_parser.debug('Channel 2 units set to : %s' % data[1])
            self.channel_units[3] = data[1]

        if re.match('^Observation\.Channel\.Name\.3$', data[0]):
            logger_meta_parser.debug('Channel name 3 set to : %s' % data[1])
            self.channel_names[4] = data[1]

        if re.match('^Observation\.Channel\.Colour\.3$', data[0]):
            logger_meta_parser.debug('Channel 3 colour found : %s' % data[1])
            hex_colour = colour_setter(data[1])

            if hex_colour is not None:
                self.channel_colours[4] = hex_colour
                logger_meta_parser.debug('Channel 3 colour set to : %s' % hex_colour)

        if re.match('^Observation\.Channel\.DataType\.3$', data[0]):
            logger_meta_parser.debug('Channel 3 datatype set to : %s' % data[1])
            self.channel_datatypenames[4] = data[1]

        if re.match('^Observation\.Channel\.Units\.3$', data[0]):
            logger_meta_parser.debug('Channel 3 units set to : %s' % data[1])
            self.channel_units[4] = data[1]

        if re.match('^Observation\.Channel\.Name\.4$', data[0]):
            logger_meta_parser.debug('Channel name 4 set to : %s' % data[1])
            self.channel_names[5] = data[1]

        if re.match('^Observation\.Channel\.Colour\.4$', data[0]):
            logger_meta_parser.debug('Channel 4 colour found : %s' % data[1])
            hex_colour = colour_setter(data[1])

            if hex_colour is not None:
                self.channel_colours[5] = hex_colour
                logger_meta_parser.debug('Channel 4 colour set to : %s' % hex_colour)

        if re.match('^Observation\.Channel\.DataType\.4$', data[0]):
            logger_meta_parser.debug('Channel 4 datatype set to : %s' % data[1])
            self.channel_datatypenames[5] = data[1]

        if re.match('^Observation\.Channel\.Units\.4$', data[0]):
            logger_meta_parser.debug('Channel 4 units set to : %s' % data[1])
            self.channel_units[5] = data[1]

        if re.match('^Observation\.Channel\.Name\.5$', data[0]):
            logger_meta_parser.debug('Channel name 5 set to : %s' % data[1])
            self.channel_names[6] = data[1]

        if re.match('^Observation\.Channel\.Colour\.5$', data[0]):
            logger_meta_parser.debug('Channel 5 colour found : %s' % data[1])
            hex_colour = colour_setter(data[1])

            if hex_colour is not None:
                self.channel_colours[6] = hex_colour
                logger_meta_parser.debug('Channel 5 colour set to : %s' % hex_colour)

        if re.match('^Observation\.Channel\.DataType\.5$', data[0]):
            logger_meta_parser.debug('Channel 5 datatype set to : %s' % data[1])
            self.channel_datatypenames[6] = data[1]

        if re.match('^Observation\.Channel\.Units\.5$', data[0]):
            logger_meta_parser.debug('Channel 5 units set to : %s' % data[1])
            self.channel_units[6] = data[1]

        if re.match('^Observation\.Channel\.Name\.6$', data[0]):
            logger_meta_parser.debug('Channel name 6 set to : %s' % data[1])
            self.channel_names[7] = data[1]

        if re.match('^Observation\.Channel\.Colour\.6$', data[0]):
            logger_meta_parser.debug('Channel 6 colour found : %s' % data[1])
            hex_colour = colour_setter(data[1])

            if hex_colour is not None:
                self.channel_colours[7] = hex_colour
                logger_meta_parser.debug('Channel 6 colour set to : %s' % hex_colour)

        if re.match('^Observation\.Channel\.DataType\.6$', data[0]):
            logger_meta_parser.debug('Channel 6 datatype set to : %s' % data[1])
            self.channel_datatypenames[7] = data[1]

        if re.match('^Observation\.Channel\.Units\.6$', data[0]):
            logger_meta_parser.debug('Channel 6 units set to : %s' % data[1])
            self.channel_units[7] = data[1]

        if re.match('^Observation\.Channel\.Name\.7$', data[0]):
            logger_meta_parser.debug('Channel name 7 set to : %s' % data[1])
            self.channel_names[8] = data[1]

        if re.match('^Observation\.Channel\.Colour\.7$', data[0]):
            logger_meta_parser.debug('Channel 7 colour found : %s' % data[1])
            hex_colour = colour_setter(data[1])

            if hex_colour is not None:
                self.channel_colours[8] = hex_colour
                logger_meta_parser.debug('Channel 7 colour set to : %s' % hex_colour)

        if re.match('^Observation\.Channel\.DataType\.7$', data[0]):
            logger_meta_parser.debug('Channel 7 datatype set to : %s' % data[1])
            self.channel_datatypenames[8] = data[1]

        if re.match('^Observation\.Channel\.Units\.7$', data[0]):
            logger_meta_parser.debug('Channel 7 units set to : %s' % data[1])
            self.channel_units[8] = data[1]

        if re.match('^Observation\.Channel\.Name\.8$', data[0]):
            logger_meta_parser.debug('Channel name 8 set to : %s' % data[1])
            self.channel_names[9] = data[1]

        if re.match('^Observation\.Channel\.Colour\.8$', data[0]):
            logger_meta_parser.debug('Channel 8 colour found : %s' % data[1])
            hex_colour = colour_setter(data[1])

            if hex_colour is not None:
                self.channel_colours[9] = hex_colour
                logger_meta_parser.debug('Channel 8 colour set to : %s' % hex_colour)

        if re.match('^Observation\.Channel\.DataType\.8$', data[0]):
            logger_meta_parser.debug('Channel 8 datatype set to : %s' % data[1])
            self.channel_datatypenames[9] = data[1]

        if re.match('^Observation\.Channel\.Units\.8$', data[0]):
            logger_meta_parser.debug('Channel 8 units set to : %s' % data[1])
            self.channel_units[9] = data[1]
