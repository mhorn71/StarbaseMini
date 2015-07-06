__author__ = 'mark'
import logging

from core.xmlLoad import Instrument
from core.instrumentChooser import selectedInstrument

logger = logging.getLogger('starinetConnector')

def connector(self):
    logger.info('StarinetConnector')
