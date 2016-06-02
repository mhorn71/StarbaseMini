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

import configparser
from os import path, makedirs
import config_utilities


class ConfigLoader:
    def __init__(self):
        '''
        :return: ConfigLoader Instance.
        :raises: FileNotFoundError, OSError,

            gives access to configuration file home and name via config_home

        Notes:  Release updates.

            To added a new configuration section/s do the following. 1.) Added section and default attributes to
            check_conf_exists.  Next increase self.version by 1 below and in check_conf_exists.  Next add additional
            section to release_update file.
        '''
        # Some basic attributes.

        self.config_file = 'starbaseMini.conf'
        self.user_instruments = 'instruments' + path.sep + 'instruments.xml'
        self.logger = None
        self.config = configparser.RawConfigParser()

        self.version = 6
        self.current_version = 0

        if path.isfile('user_home.txt'):
            try:
                file = open('user_home.txt', 'r')
            except IOError:
                raise FileNotFoundError("Fatal error unable to open user_home.txt!!\nContact developer for help.")
            else:
                # This looks a little weird as we strip the path sep and then added it back this is so we don't end
                # up with a double seperater
                self.user_home = file.read()
                self.user_home.strip(path.sep)
                self.user_home = self.user_home + path.sep
                file.close()
        else:
            self.user_home = path.expanduser("~")

        if not path.isdir(self.user_home):
            raise FileNotFoundError("Fatal error unable to detect user home!!\nContact developer for help.")

        self.user_home += path.sep + '.starbasemini' + path.sep

        if not path.isdir(self.user_home):
            try:
                makedirs(self.user_home)
            except OSError as msg:
                raise OSError(msg)
            else:
                self.config_home = self.user_home
        else:
            self.config_home = self.user_home

        self.conf_file = self.config_home + self.config_file

        self.check_conf_exists()

        self.updater = config_utilities.Updater(self.config_home)

    def check_conf_exists(self):
        '''
        :raises: IOError in the event it can't find or write to configuration file.
        '''
        
        self.conf_file = self.config_home + self.config_file

        if not path.exists(self.conf_file):
            try:
                open(self.conf_file, 'a').close()
            except IOError as msg:
                raise IOError(msg)
            else:
                self.config.read(self.conf_file)

                # Add Application Release Number
                self.config.add_section('Release')
                self.config.set('Release', 'version', '6')

                # Add Application Data Save Path
                self.config.add_section('Application')
                self.config.set('Application', 'instrument_data_path', '')
                self.config.set('Application', 'instrument_identifier', 'Staribus 4 Channel Logger')
                self.config.set('Application', 'instrument_autodetect', 'True')
                self.config.set('Application', 'instrument_upgrade', 'True')

                # Add StarinetConnector section.
                self.config.add_section('StarinetRelay')
                self.config.set('StarinetRelay', 'active', 'False')
                self.config.set('StarinetRelay', 'address', '0.0.0.0')
                self.config.set('StarinetRelay', 'starinet_port', '1205')

                # Add Chart legend attributes section
                self.config.add_section('Legend')
                self.config.set('Legend', 'location', 'best')
                self.config.set('Legend', 'columns', '1')
                self.config.set('Legend', 'font', 'medium')

                # Add ObservatoryMetadata section.
                self.config.add_section('ObservatoryMetadata')
                self.config.set('ObservatoryMetadata', 'name', 'Wards Hill Observatory')
                self.config.set('ObservatoryMetadata', 'description', 'Radio Telescope')
                self.config.set('ObservatoryMetadata', 'contact_email', 'someone@wardshillobservatory.com')
                self.config.set('ObservatoryMetadata', 'contact_telephone', '+44 123 1234567')
                self.config.set('ObservatoryMetadata', 'contact_url', 'http://wardshillobservatory.co.uk')
                self.config.set('ObservatoryMetadata', 'country', 'GB')
                self.config.set('ObservatoryMetadata', 'timezone', 'GMT+00:00')
                self.config.set('ObservatoryMetadata', 'geodetic_datum', 'WGS84')
                self.config.set('ObservatoryMetadata', 'geomagnetic_latitude', '+00:00:00.000')
                self.config.set('ObservatoryMetadata', 'geomagnetic_longitude', '+000:00:00.000')
                self.config.set('ObservatoryMetadata', 'geomagnetic_model', 'IGRF-11')
                self.config.set('ObservatoryMetadata', 'latitude', '+00:00:00.000')
                self.config.set('ObservatoryMetadata', 'longitude', '+000:00:00.000')
                self.config.set('ObservatoryMetadata', 'hasl', '32.0')

                # Add ObserverMetadata section.
                self.config.add_section('ObserverMetadata')
                self.config.set('ObserverMetadata', 'name', 'Oculo Gyric')
                self.config.set('ObserverMetadata', 'description', 'The really observant Observer')
                self.config.set('ObserverMetadata', 'contact_email', 'Oculo@gyric.com')
                self.config.set('ObserverMetadata', 'contact_telephone', '+44 123 1234567')
                self.config.set('ObserverMetadata', 'contact_url', 'http://github.com/mhorn71/StarbaseMini')
                self.config.set('ObserverMetadata', 'country', 'GB')
                self.config.set('ObserverMetadata', 'notes', 'The Observer Notes')

                # Add Logging sections.
                self.config.add_section('loggers')
                self.config.set('loggers', 'keys', 'root')

                self.config.add_section('logger_root')
                self.config.set('logger_root', 'handlers', 'hand0')
                self.config.set('logger_root', 'level', 'INFO')

                self.config.add_section('handlers')
                self.config.set('handlers', 'keys', 'hand0')

                self.config.add_section('handler_hand0')
                self.config.set('handler_hand0', 'class', 'handlers.RotatingFileHandler')
                logfile = self.config_home + 'starbaseMini.log'
                args = (logfile, 'a', 2000000, 6, 'utf8')
                self.config.set('handler_hand0', 'args', args)
                self.config.set('handler_hand0', 'formatter', 'mine')

                self.config.add_section('formatters')
                self.config.set('formatters', 'keys', 'mine')

                self.config.add_section('formatter_mine')
                self.config.set('formatter_mine', 'format', '%(asctime)s [%(name)s] - %(levelname)s - %(message)s')

                try:
                    with open(self.conf_file, 'wt') as conffile:
                        self.config.write(conffile)
                        conffile.close()
                except IOError as msg:
                    raise IOError(msg)

    def release_update(self):
        try:
            self.current_version = int(self.get('Release', 'version'))
        except (configparser.NoSectionError, ValueError):
            try:
                open(self.conf_file, 'a').close()
            except IOError as msg:
                raise IOError(msg)
            else:
                self.config.read(self.conf_file)
                # Add Application Release Number
                self.config.add_section('Release')
                self.config.set('Release', 'version', '1')
                try:
                    with open(self.conf_file, 'wt') as conffile:
                        self.config.write(conffile)
                        conffile.close()
                except IOError as msg:
                    raise IOError(msg)
        else:
            if self.current_version == self.version:
                pass
            else:
                self.config.read(self.conf_file)
                for i in range((self.current_version + 1), (self.version + 1)):
                    self.updater.update(self.config, i, self.config_home)
                    self.config.set('Release', 'version', str(i))

                try:
                    with open(self.conf_file, 'wt') as conffile:
                        self.config.write(conffile)
                        conffile.close()
                except IOError as msg:
                    raise IOError(msg)

    def get(self, section, option):

        '''
        Example :

            get('StaribusPort', 'port')

        :param section: Configuration Section
        :param option: Section Parameter
        :return: Parameter Value or None
        :raises: ValueError
        '''
        
        self.config.read(self.conf_file)
        try:
            get_response = self.config.get(section, option)
        except (configparser.NoSectionError, KeyError, ValueError, configparser.NoOptionError) as msg:
            raise ValueError(msg)
        else:
            if len(get_response) == 0:
                return None
            else:
                return get_response

    def set(self, section, option, value):

        '''
        Example :

            set('StaribusPort', 'port', 'COM1')

        :param section: Configuration Section
        :param option: Section Parameter
        :param value: Parameter Value
        :raises: ValueError, IOError
        '''

        self.config.read(self.conf_file)

        try:
            self.config.set(section, option, value)

            with open(self.conf_file, 'wt') as configfile:

                self.config.write(configfile)
                configfile.close()

        except configparser.NoSectionError as msg:
            raise ValueError(msg)
        except configparser.NoOptionError as msg:
            raise ValueError(msg)
        except IOError as msg:
            raise IOError(msg)

    def rm_section(self, section):
        '''
            Example :

                rm_section('StaribusPort')

            :param section: Configuration Section
            :raises: ValueError, IOError
            '''

        self.config.read(self.conf_file)

        try:
            self.config.remove_section(section)

            with open(self.conf_file, 'wt') as configfile:

                self.config.write(configfile)
                configfile.close()

        except configparser.NoSectionError as msg:
            raise ValueError(msg)
        except configparser.NoOptionError as msg:
            raise ValueError(msg)
        except IOError as msg:
            raise IOError(msg)

    def rm_option(self, section, option):
        '''
            Example :

                rm_option('StaribusPort', 'port')

            :param section: Configuration Section
            :param option: Section Parameter
            :raises: ValueError, IOError
            '''

        self.config.read(self.conf_file)

        try:
            self.config.remove_option(section, option)

            with open(self.conf_file, 'wt') as configfile:

                self.config.write(configfile)
                configfile.close()

        except configparser.NoSectionError as msg:
            raise ValueError(msg)
        except configparser.NoOptionError as msg:
            raise ValueError(msg)
        except IOError as msg:
            raise IOError(msg)

    def check_state(self):
        return True


if __name__ == '__main__':
    x = ConfigLoader()
