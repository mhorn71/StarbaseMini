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

import os
import logging
import sys

upgradelog = os.path.expanduser('~') + os.path.sep + '.starbasemini' + os.path.sep + 'upgrade.log'

logging.basicConfig(filename=upgradelog,level=logging.INFO)

def update(config_object, version):

    if version == 2:
        logging.info('Upgrading configuration to version 2')

        config_object.add_section('Legend')
        logging.info('Added section \'legend\' to starbaseMini.conf')

        config_object.set('Legend', 'location', 'best')
        logging.info('Added option \'location\' to \'legend\' set to \'best\'')

        config_object.set('Legend', 'columns', '1')
        logging.info('Added option \'columns\' to \'legend\' set to \'1\'')

        config_object.set('Legend', 'font', 'medium')
        logging.info('Added option \'font\' to \'legend\' set to \'medium\'')

    if version == 3:

        logging.info('Upgrading configuration to version 3')

        config_object.set('ObservatoryMetadata', 'timezone', 'GMT+00:00')

        logging.info('Updating section option \'ObservatoryMetadata\' - \'timezone\' set to \'GMT+00:00\'')

    if version == 4:

        logging.info('Upgrading configuration to version 4')

        config_object.remove_section('StaribusPort')
        logging.info('Removing section \'StaribusPort\'')

        config_object.remove_option('Application','instrument_autodetect')
        logging.info('Removing option \'instrument_autodetect\'')

        instruments_local = os.path.expanduser('~') + os.path.sep + '.starbasemini' + os.path.sep + \
                            'instruments' + os.path.sep

        logging.info('Instruments path set to - ' + instruments_local)

        instrument_local_base = os.path.expanduser('~') + os.path.sep + '.starbasemini' + os.path.sep

        logging.info('Instrument base path set to - ' + instrument_local_base)

        try:
            if os.path.exists(instruments_local):
                logging.info('Instruments path exists')
                for name in os.listdir(instruments_local):
                    if os.path.isfile(instruments_local + name):
                        logging.info('Instrument XML file found')
                        os.rename(instruments_local + name, instrument_local_base + name + '.revison3bak')
                        logging.info('Renaming file - ' + name + ' to ' + name + '.revison3bak')
        except (OSError, IOError) as msg:
            logging.critical(msg)