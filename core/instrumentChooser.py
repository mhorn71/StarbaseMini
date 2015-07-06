__author__ = 'mark'
import sys
import logging
import core.utilities as utils

def selectedInstrument(parent):

    logger = logging.getLogger('instrumentChooser')
    instrument = parent.config.get('Application', 'instrument_type')

    # To add a new instrument type add it below, make sure all names match.

    if instrument == 'Staribus4ChLogger':
        logger.debug('Found %s in application configuration' % instrument)

        return 'instruments/staribus-4ch-logger.xml'

    else:

        logger.critical('Unable to find instrument : %s' % instrument)
        utils.exit_message('Fatal Error - Unable to find instrument defined in configuration.')
        sys.exit(1)
