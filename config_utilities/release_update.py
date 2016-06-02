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
import logging
import os


class Updater():
    def __init__(self, config_home):
        self.config_home = config_home

        upgradelog = config_home + 'upgrade.log'

        self.logger_update = logging.getLogger('Upgrade')
        handler = logging.FileHandler(upgradelog, mode='a', encoding=None, delay=False)
        formatter = logging.Formatter('%(asctime)s [%(name)s] - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger_update.addHandler(handler)
        self.logger_update.setLevel(logging.DEBUG)

    def update(self, config_object, version, config_home):

        if version == 2:
            self.logger_update.info('Upgrading configuration to version 2')

            config_object.add_section('Legend')
            self.logger_update.info("Added section 'legend' to starbaseMini.conf")

            config_object.set('Legend', 'location', 'best')
            self.logger_update.info("Added option 'location' to 'legend' set to 'best'")

            config_object.set('Legend', 'columns', '1')
            self.logger_update.info("Added option 'columns' to 'legend' set to '1'")

            config_object.set('Legend', 'font', 'medium')
            self.logger_update.info("Added option 'font' to 'legend' set to 'medium'")

        if version == 3:
            self.logger_update.info('Upgrading configuration to version 3')

            config_object.set('ObservatoryMetadata', 'timezone', 'GMT+00:00')

            self.logger_update.info("Updating section option 'ObservatoryMetadata' - 'timezone' set to 'GMT+00:00'")

        if version == 4:

            self.logger_update.info('Upgrading configuration to version 4')

            config_object.remove_section('StaribusPort')

            self.logger_update.info("Removed configuration section 'StaribusPort'")

            config_object.remove_option('Application','instrument_autodetect')

            self.logger_update.info("Removed configuration 'instrument_autodetect'")

            instruments_local = config_home + 'instruments' + os.path.sep

            self.logger_update.info("Instruments path set to - " + instruments_local)

            instrument_local_base = config_home

            self.logger_update.info('Instrument base path set to - ' + instrument_local_base)

            try:
                if os.path.exists(instruments_local):

                    self.logger_update.info('Instruments path exists')

                    for name in os.listdir(instruments_local):

                        if os.path.isfile(instruments_local + name):
                            self.logger_update.info('Instrument XML file found')

                            os.rename(instruments_local + name, instrument_local_base + name + '.revision_bak')

                            self.logger_update.info('Renaming file - ' + name + ' to ' + name + '.revision_bak')

            except (OSError, IOError) as msg:

                self.logger_update.critical(msg)

        if version == 5:

            self.logger_update.info('Upgrading configuration to version 5')

            config_object.set('Application', 'instrument_upgrade', 'True')

            self.logger_update.info("Added option 'instrument_upgrade' to 'Application' set to 'True'")

        if version == 6:

            self.logger_update.info('Upgrading configuration to version 6')

            instruments_local = config_home + 'instruments' + os.path.sep

            self.logger_update.info('Instruments path set to - ' + instruments_local)

            instrument_local_base = config_home

            self.logger_update.info('Instrument base path set to - ' + instrument_local_base)

            try:
                if os.path.exists(instruments_local):

                    self.logger_update.info('Instruments path exists')

                    for name in os.listdir(instruments_local):

                        if os.path.isfile(instruments_local + name):

                            sequence = 0

                            if os.path.isfile(instrument_local_base + name + '.revision_bak'):

                                while os.path.isfile(instrument_local_base + name + '.' + str(sequence) + '.revision_bak'):

                                    sequence += 1

                                else:

                                    os.rename(instruments_local + name, instrument_local_base + name + '.' + str(sequence) +
                                              '.revision_bak')

                                    self.logger_update.info('Renaming file - ' + name + ' to ' + name + '.' + str(sequence) +
                                                     '.revision_bak')

                            else:

                                os.rename(instruments_local + name, instrument_local_base + name + '.revision_bak')

                                self.logger_update.info('Renaming file - ' + name + ' to ' + name + '.revision_bak')

            except (OSError, IOError) as msg:

                self.logger_update.critical(msg)

            config_object.remove_section('Staribus2Starinet')

            self.logger_update.info("Removed configuration section 'Staribus2Starinet'")


