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

import sys
import os
import logging.config
import logging
import datetime
import re

from PyQt4 import QtGui, QtCore

try:
    from PyQt4.QtCore import QString
except ImportError:
    QString = str

from ui import Ui_MainWindow
import utilities
import xml_utilities
import config_utilities
import starinet_connector as starinet_relay
import interpreter
import constants
import datatranslators
import metadata
import charting
import instrument_attrib
import datastore
import core
import filters
import data_viewer

version = '3.0.1'


class Main(QtGui.QMainWindow):
    def __init__(self, parent=None):

        # Initialise UI

        QtGui.QMainWindow.__init__(self, parent)

        self.ui = Ui_MainWindow()

        self.setWindowModality(QtCore.Qt.WindowModal)

        self.ui.setupUi(self)

        # Set application icon

        self.setWindowIcon(QtGui.QIcon('images/starbase.png'))

        # Style sheets

        if sys.platform.startswith('darwin'):

            with open('css/macStyle.css', 'r') as style:

                self.setStyleSheet(style.read())

        elif sys.platform.startswith('win32'):

            with open('css/winStyle.css', 'r') as style:

                self.setStyleSheet(style.read())

        elif sys.platform.startswith('linux'):

            with open('css/nixStyle.css', 'r') as style:

                self.setStyleSheet(style.read())

        # Initialise the application configuration loader class.

        try:

            self.application_configuration = config_utilities.ConfigLoader()

        except FileNotFoundError:

            print("CRITICAL ERROR unable to determine users home folder.")
            print("Please create a file called user_home.txt in the application root folder")
            print("with one line with the full application path.")
            print("Example:  C:\\Users\\mark")

            sys.exit(1)

        # Check the application configuration looks sane.

        if not self.application_configuration.check_state():

            print("CRITICAL ERROR .starbasemini/starbaseMini.conf is not valid.")

            sys.exit(1)

        # Initialise logging

        logging.config.fileConfig(self.application_configuration.conf_file, disable_existing_loggers=False)

        logger = logging.getLogger('StarbaseMini.init')

        # A header so we can easily see when the application was started.

        logger.info('**************************** APPLICATION STARTUP ****************************')

        # Try to update application configuration is need.

        try:

            self.application_configuration.release_update()

        except IOError as msg:

            logger.warning('Unable to update application configuration : %s' % str(msg))

        # Get the current application background colour and set self.background_colour

        colour = self.palette().color(QtGui.QPalette.Background)

        self.background_colour = utilities.rgb2hex((colour.red(), colour.green(), colour.blue()))

        # Initialise datastore class.

        self.data_store = datastore.DataStore()

        # Initialise instruments class, this so we can read the instruments.xml files if present.

        self.instruments = xml_utilities.Instruments()

        # Initialise instrument class

        self.instrument = xml_utilities.Instrument()

        # Initialise release notes dialog class

        self.release_note_dialog = utilities.ReleaseNote()

        # Initialise the configuration tool class

        self.configuration_tool_dialog = config_utilities.ConfigManager()

        # Initialise the instrument attributes dialog

        self.instrument_attributes_dialog = instrument_attrib.InstrumentAttrib()

        # Initialise data translator classes

        self.instrument_datatranslator = None  # We set this class later once we know what instrument is enabled.

        self.csv_datatranslator = None

        self.metadata = None

        # Initialise metadata dialog class

        self.metadata_viewer_editor_dialog = metadata.MetadataViewerEditor(self.data_store)

        # Initialise data viewer dialog class

        self.data_viewer = data_viewer.DataViewer(self.data_store, self.instrument)

        # Initialise command interpreter class

        self.command_interpreter = interpreter.CommandInterpreter(self.data_store)

        # Initialise segment time series class and run the setup.

        self.segmenter = core.SegmentTimeSeries(self.data_store)

        # Initialise mpl chart class

        self.chart = charting.Chart(self.ui)

        # Menu items

        self.ui.actionExit.triggered.connect(self.close)

        self.ui.actionConfiguration.triggered.connect(self.configuration_triggered)

        self.ui.actionInstrument_Attrib.triggered.connect(self.instrument_attrib_triggered)

        self.ui.actionAbout.triggered.connect(self.help_about_triggered)

        self.ui.actionReleaseNotes.triggered.connect(self.release_notes_triggered)

        self.ui.actionOpen.triggered.connect(self.open_csv_file)

        self.ui.actionSave_RawData.triggered.connect(lambda: self.save_data('raw'))

        self.ui.actionSave_Processed_Data.triggered.connect(lambda: self.save_data('processed'))

        self.ui.SegmentRawDataDay.triggered.connect(lambda: self.segment_data('day', 'raw'))

        self.ui.SegmentRawDataWeek.triggered.connect(lambda: self.segment_data('week', 'raw'))

        self.ui.SegmentProcessDataDay.triggered.connect(lambda: self.segment_data('day', 'processed'))

        self.ui.SegmentProcessDataWeek.triggered.connect(lambda: self.segment_data('week', 'processed'))

        self.ui.actionMetadata.triggered.connect(self.metadata_viewer_editor)

        self.ui.actionProcessed_Data.triggered.connect(lambda: self.dataview('processed'))
        self.ui.actionRaw_Data.triggered.connect(lambda: self.dataview('raw'))

        self.ui.actionNon_Linear_Static_Remover.triggered.connect(lambda: self.filter_data('NonLinearStaticRemover'))
        self.ui.actionPeak_Extractor.triggered.connect(lambda: self.filter_data('PeakExtractor'))
        self.ui.actionRunning_Average.triggered.connect(lambda: self.filter_data('RunningAverage'))
        self.ui.actionWeighted_Running_Average.triggered.connect(lambda: self.filter_data('WeightedRunningAverage'))

        self.ui.toolBox.currentChanged.connect(lambda: self.toolbox_icon_control(self.ui.toolBox.currentIndex()))
        self.toolbox_icon_control(self.ui.toolBox.currentIndex())

        # Run once trip

        self.run_once = True

        # Store the previous set instrument menu item in case we don't change and need to set to original selection.

        self.previous_instrument_menu_item = None

        # The state of the Starinet Relay

        self.starinet_relay_state = False

        # The Data source can be instrument or csv

        self.data_source = 'instrument'

        # Staribus serial port state.
        self.serial_port_state = True

        # Setup status message window, QTableWidget

        self.statusMessageIndex = 0  # A simple counter for the status message method.

        headers = ['DateTime', 'Identifier', 'Status', 'Units', 'ResponseValue']

        self.ui.statusMessage.setHorizontalHeaderLabels(headers)

        self.ui.statusMessage.setColumnWidth(0, 115)  # Datetime Column

        self.ui.statusMessage.setColumnWidth(1, 175)  # Ident Column

        self.ui.statusMessage.setColumnWidth(2, 182)  # Status Column

        self.ui.statusMessage.setColumnWidth(3, 56)  # Units Column

        self.ui.statusMessage.verticalHeader().setDefaultSectionSize(20)  # Sets the height of the rows.

        self.ui.statusMessage.horizontalHeader().setStretchLastSection(True)  # Expands section to widget width.

        # Button connectors

        self.ui.executeButton.clicked.connect(self.execute_triggered)

        self.ui.channel0Button.clicked.connect(lambda: self.channel_triggered(0, self.ui.channel0Button.isChecked()))
        self.ui.channel1Button.clicked.connect(lambda: self.channel_triggered(1, self.ui.channel1Button.isChecked()))
        self.ui.channel2Button.clicked.connect(lambda: self.channel_triggered(2, self.ui.channel2Button.isChecked()))
        self.ui.channel3Button.clicked.connect(lambda: self.channel_triggered(3, self.ui.channel3Button.isChecked()))
        self.ui.channel4Button.clicked.connect(lambda: self.channel_triggered(4, self.ui.channel4Button.isChecked()))
        self.ui.channel5Button.clicked.connect(lambda: self.channel_triggered(5, self.ui.channel5Button.isChecked()))
        self.ui.channel6Button.clicked.connect(lambda: self.channel_triggered(6, self.ui.channel6Button.isChecked()))
        self.ui.channel7Button.clicked.connect(lambda: self.channel_triggered(7, self.ui.channel7Button.isChecked()))
        self.ui.channel8Button.clicked.connect(lambda: self.channel_triggered(8, self.ui.channel8Button.isChecked()))

        # Hide the channel selection buttons.

        self.ui.channel0Button.setVisible(False)
        self.ui.channel0colour.setVisible(False)
        self.ui.channel1Button.setVisible(False)
        self.ui.channel1colour.setVisible(False)
        self.ui.channel2Button.setVisible(False)
        self.ui.channel2colour.setVisible(False)
        self.ui.channel3Button.setVisible(False)
        self.ui.channel3colour.setVisible(False)
        self.ui.channel4Button.setVisible(False)
        self.ui.channel4colour.setVisible(False)
        self.ui.channel5Button.setVisible(False)
        self.ui.channel5colour.setVisible(False)
        self.ui.channel6Button.setVisible(False)
        self.ui.channel6colour.setVisible(False)
        self.ui.channel7Button.setVisible(False)
        self.ui.channel7colour.setVisible(False)
        self.ui.channel8Button.setVisible(False)
        self.ui.channel8colour.setVisible(False)

        # Module, Command and Choices ComboBox Triggers.

        self.ui.moduleCombobox.blockSignals(True)

        self.ui.commandCombobox.blockSignals(True)

        self.ui.commandParameter.blockSignals(True)

        self.ui.moduleCombobox.currentIndexChanged.connect(self.populate_ui_command)

        self.ui.commandCombobox.currentIndexChanged.connect(self.command_parameter_populate)

        # Parameter entry emit and connect signals

        self.ui.commandParameter.textChanged.connect(self.parameter_check_state)

        self.ui.commandParameter.textChanged.emit(self.ui.commandParameter.text())

        # Chart show legend state change.

        self.ui.showLegend.stateChanged.connect(self.chart_show_legend_triggered)

        # Instrument Name and File lists
        self.instrument_names = []

        self.instrument_filenames = []

        # lets find instruments the configured instruments and xml locations.
        self.find_instrument_names_filenames_xml()

        # A single shot time to check for application upgrade.

        if self.application_configuration.get('Application', 'instrument_upgrade') == 'True':

            QtCore.QTimer.singleShot(200, self.updateCaption)

    #  Find instrument xml either default or user defined in base and local locations.

    def find_instrument_names_filenames_xml(self):

        logger = logging.getLogger('StarbaseMini.find_instrument_names_filenames_xml')

        # Check to see if relay is running and if it is report Restart required and do nothing.

        if self.starinet_relay_state:

            logger.debug('Starinet relay is running, applications requires restart.')

            self.status_message('system', 'PREMATURE_TERMINATION',
                                    'Starinet Relay is running please restart the application.', None)

        else:

            # First make sure the Instrument Name and File lists are blank

            self.instrument_names.clear()

            self.instrument_filenames.clear()

            # local = xml held in the user home folder under .starbasemini/instruments
            # base = xml held in the application root folder under instrumetns.

            # Load base instruments/instruments.xml first

            instrument_name_file_list = []

            if os.path.isfile('instruments' + os.path.sep + 'instruments.xml'):

                try:

                    self.instruments.load_xml('instruments' + os.path.sep + 'instruments.xml')

                except FileNotFoundError:

                    logger.warning('No instruments.xml found in instruments!!')

                else:

                    logger.info('Found xml file : instruments' + os.path.sep + 'instruments.xml')

                    # Get names of instruments from instruments.xml

                    try:

                        instrument_names = self.instruments.get_names()

                    except (AttributeError, IndexError):

                        pass

                    else:

                        # Get the filename of the instrument

                        for name in instrument_names:

                            try:

                                instrument_filename = self.instruments.get_filename(name)

                            except AttributeError:

                                pass

                            else:

                                # Append the instrument name, filname, and location

                                instrument_name_file_list.append((name, instrument_filename, 'base'))

            # Now we check to see if there is an instruments.xml in the .starbase/instruments folder

            if os.path.isfile(self.application_configuration.user_home + 'instruments' + os.path.sep +
                                      'instruments.xml'):

                try:

                    self.instruments.load_xml(self.application_configuration.user_home + 'instruments' +
                                              os.path.sep + 'instruments.xml')

                except FileNotFoundError:

                    logger.warning('No instruments.xml found in .starbasemini' + os.path.sep + 'instruments folder!!')

                else:

                    logger.info('Found xml file : %s' % str(self.application_configuration.user_home +
                                                            'instruments' + os.path.sep + 'instruments.xml'))

                    # Get names of instruments from instruments.xml

                    try:
                        instrument_names = self.instruments.get_names()

                    except (AttributeError, IndexError):

                        pass

                    else:

                        for name, file, local in instrument_name_file_list:

                            # If the name is unique then remove it from the instrument_names list.

                            if name in instrument_names:

                                instrument_names.remove(name)

                        # for each name in the list get the file name and then append details and location to
                        # instrument_name_file_list

                        for name in instrument_names:

                            try:

                                instrument_filename = self.instruments.get_filename(name)

                            except AttributeError:

                                pass

                            else:

                                # Append the instrument name, filname, and location

                                instrument_name_file_list.append((name, instrument_filename, 'local'))

            # Make sure the instrument_name_file_list is zero length.

            if len(instrument_name_file_list) == 0:

                logger.critical('No instruments in either base' + os.path.sep + 'instruments or .'
                                'starbasemini' + os.path.sep + 'instruments so we have to exit.')

                sys.exit(1)

            # Next we need to check to see if any of the base installed instruments have been updated and the xml stored
            # in .starbasemini/instruments.

            for name, file, local in instrument_name_file_list:

                if local == 'base':

                    # Next check to see if the default file has been modified and update the path if it has.

                    if os.path.isfile(self.application_configuration.user_home + 'instruments' + os.path.sep + file):

                        self.instrument_names.append(name)

                        self.instrument_filenames.append(self.application_configuration.user_home + 'instruments' +
                                                         os.path.sep + file)

                    else:

                        self.instrument_names.append(name)

                        self.instrument_filenames.append('instruments' + os.path.sep + file)

                elif local == 'local':

                    self.instrument_names.append(name)

                    self.instrument_filenames.append(self.application_configuration.user_home + 'instruments' + os.path.sep
                                                     + file)

            # Populate the instrument menu items.

            if self.run_once:  # This get set to false once we've initialised the first instrument xml.

                self.instrument_menu_setup()

            # Now we need to call the instrument loader for the instrument that is set.

            self.instrument_xml_loader()

    def instrument_menu_setup(self):

        action = QtGui.QActionGroup(self.ui.menuInstrument, exclusive=True)

        for item in self.instrument_names:

            ag = QtGui.QAction(item, action, checkable=True)

            if self.application_configuration.get('Application', 'instrument_identifier') == item:

                ag.setChecked(True)

                self.previous_instrument_menu_item = item

            self.ui.menuInstrument.addAction(ag)

            self.connect(ag, QtCore.SIGNAL('triggered()'), lambda item=item: self.instrument_selection(item))

    def instrument_selection(self, item):

        logger = logging.getLogger('StarbaseMini.instrument_selection')

        logger.debug("Datastore length : %s" % str(len(self.data_store.RawData)))
        logger.debug("Datastore RawDataSaved : %s" % str(self.data_store.RawDataSaved))

        if self.data_store.data_state()[0] is False:

            message = 'WARNING:  You have unsaved data.\n\nIf you change the instrument, ' + \
                      'you will be able to save the unsaved data!\n\nDo you want to change instruments?'

            header = ''

            result = QtGui.QMessageBox.warning(None,
                                               header,
                                               message,
                                               QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)

            if result == QtGui.QMessageBox.Yes:

                self.data_store.clear()

                self.instrument_selection(item)


            else:
                for action in self.ui.menuInstrument.actions():
                    if action.text() == self.previous_instrument_menu_item:
                        action.setChecked(True)

        else:

            if self.starinet_relay_state:

                logger.debug('instrument_selection Starinet Relay State : True')

                logger.debug('Starinet relay is running, applications requires restart.')

                self.status_message('system', 'PREMATURE_TERMINATION',
                                    'Starinet Relay is running please restart the application.', None)

            else:

                logger.debug('instrument_selection Starinet Relay State : False')

                self.previous_instrument_menu_item = item

                try:

                    self.application_configuration.set('Application', 'instrument_identifier', item)

                except (IOError, ValueError) as msg:

                    logger.debug('Unable to set instrument identifier :%s' % str(msg))

                    # Reset the menu check tick back at the original menu item.

                    for action in self.ui.menuInstrument.actions():

                        if action.text() == self.previous_instrument_menu_item:

                            action.setChecked(True)

                    self.status_message('system', 'ABORT', 'Unable to set instrument - ' + str(msg), None)

                else:

                    if not self.instrument_xml_loader():

                        # Reset the menu check tick back to the original menu item.

                        for action in self.ui.menuInstrument.actions():

                            if action.text() == self.previous_instrument_menu_item:

                                action.setChecked(True)

                        self.status_message('system', 'ABORT', 'Unable to set instrument', None)

                        self.disable_control_panel()

    def instrument_xml_loader(self):

        logger = logging.getLogger('StarbaseMini.instrument_xml_loader')

        # First lets make sure the instrument class is in a consistent state.

        self.instrument.clear_instrument()

        try:

            instrument_index = self.instrument_names.index(self.application_configuration.get(
                                                           'Application', 'instrument_identifier'))

        except (IndexError, ValueError) as msg:

            # If we fail to load the instrument xml for the set instrument and this is out first run we bail.

            if self.run_once:

                logger.critical('Unable to load instrument XML : %s' % str(msg))

                missing_instrument = self.application_configuration.get('Application', 'instrument_identifier')

                # As instrument is missing we'll set the Staribus 4 channel logger

                logger.info('Setting default configuration - Staribus 4 Channel Logger')

                self.status_message('system',
                                    'WARNING', 'Unable to load %s loading Staribus 4 Channel logger instead!!' %
                                    missing_instrument, None)

                self.application_configuration.set('Application', 'instrument_identifier', 'Staribus 4 Channel Logger')

                self.disable_control_panel()

                logger.info('Attempting start up again.')

                self.instrument_xml_loader()


            else:

                logger.critical('Unable to load instrument XML : %s' % str(msg))

                sys.exit(1)
        else:

            self.setWindowTitle('StarbaseMini -- Version %s -- %s' %
                                (version, self.application_configuration.get('Application', 'instrument_identifier')))

            try:

                # Now try and load the instrument XML

                self.instrument.load_xml(self.instrument_filenames[instrument_index])

                logger.info('Attempting to load instrument.xml file : %s' %
                            str(self.instrument_filenames[instrument_index]))

            except (FileNotFoundError, AttributeError, ValueError, IndexError, LookupError) as msg:

                # If we fail to load the instrument xml for the set instrument and this is out first run we bail.

                if self.run_once:

                    sys.exit(1)

                else:

                    self.status_message('system', 'ABORT', 'Unable to load instrument', None)

                    logger.critical('Unable to load instrument XML : %s' % msg)

                    self.disable_control_panel()
            else:
                # We've now appear to have a valid application configuration and instrument.xml

                # Now we see if we can load the datatranslator and if we can run the application state control

                if self.instrument_datatranslator_class_loader():

                    self.application_state_control()

                    self.ui.actionOpen.setEnabled(True)

                    self.ui.actionSave_RawData.setEnabled(True)

                    self.ui.actionSave_Processed_Data.setEnabled(True)

                    self.ui.actionDay.setEnabled(True)

                    self.ui.actionWeek.setEnabled(True)

                else:

                    self.ui.actionOpen.setEnabled(False)

                    self.ui.actionSave_RawData.setEnabled(False)

                    self.ui.actionSave_Processed_Data.setEnabled(False)

                    self.ui.actionDay.setEnabled(False)

                    self.ui.actionWeek.setEnabled(False)

                    self.disable_control_panel()

                    self.status_message('system', 'INVALID_XML', 'Unable to load data translator!!', None)

                self.run_once = False

                return True

    def application_state_control(self):

        # Reset serial port state to True

        self.serial_port_state = True

        logger = logging.getLogger('StarbaseMini.application_state_control')

        if self.run_once:

            self.status_message('system', 'INFO', 'Application started.', None)
            self.status_message('system', 'INFO', self.instrument.instrument_identifier + ' started.', None)

        else:

            self.status_message('system', 'INFO', 'Instrument changed to : ' + self.instrument.instrument_identifier,
                                None)

        # Try to close any open streams.

        self.command_interpreter.close()

        logger.debug('Command interpreter closed.')

        # We check for two states Relay or Standard Instrument.  Staribus to Starinet Converter is run from Interpreter.

        # See if we're acting as relay

        if self.application_configuration.get('StarinetRelay', 'active') == 'True':

            logger.debug('Starinet Relay Active : True')

            logger.info('########## Initialising Starinet Relay - Disabling UI control panel ##########')

            self.disable_control_panel()

            logger.debug('Control panel disabled.')

            # Check instrument type

            if self.instrument.instrument_staribus_address == '000':  # Looks like we have Starinet then relay is False

                logger.debug('Staribus address : %s' % self.instrument.instrument_staribus_address)

                logger.warning('Starinet relay enabled but Starinet instrument selected.')

                self.status_message('system', 'PREMATURE_TERMINATION', 'Starinet relay enabled but Starinet instrument '
                                                                       'selected.', None)

                self.disable_control_panel()

                logger.debug('Control panel disabled.')

            else:  # Looks like we have a Staribus instrument now auto detect instrument or try to open port.

                logger.debug('Staribus address : %s' % self.instrument.instrument_staribus_address)

                # First check the configuration looks sane.

                if not utilities.check_ip(self.application_configuration.get('StarinetRelay', 'address')):

                    logger.debug('Starinet address not valid : %s' % str(self.application_configuration.get('StarinetRelay',
                                                                                                     'address')))

                    self.status_message('system', 'PREMATURE_TERMINATION', 'Starinet Relay IP address invalid')

                    self.disable_control_panel()

                    logger.debug('Control panel disabled.')

                elif not utilities.check_starinet_port(self.application_configuration.get('StarinetRelay',
                                                                                          'starinet_port')):

                    logger.debug('Starinet port not valid : %s' % str(self.application_configuration.get('StarinetRelay',
                                                                                                  'starinet_port')))

                    self.status_message('system', 'PREMATURE_TERMINATION', 'Starinet Relay IP address invalid')

                    self.disable_control_panel()

                    logger.debug('Control panel disabled.')

                else:

                    logger.debug('Starinet address and port valid')

                    if self.instrument.instrument_staribus_autodetect == 'True':

                        logger.debug('Attempt instrument autodetect is True')

                        if self.instrument_autodetector():

                            logger.debug('Instrument autodetect returned True')

                            self.starinet_relay_state = True

                            logger.debug('Starinet Relay Active : True')

                            logger.info('########## Valid Starinet relay configuration found. ##########')
                            logger.info('Starting startinet relay')

                            self.setWindowTitle('StarbaseMini -- Version %s -- %s' % (
                                version, self.application_configuration.get('Application', 'instrument_identifier') +
                                ' Starinet Relay'))

                            starinet_relay.StarinetConnectorStart(self.application_configuration.get('StarinetRelay',
                                                                  'address'),
                                                                  self.application_configuration.get('StarinetRelay',
                                                                                                     'starinet_port'),
                                                                  self.instrument.instrument_staribus_port,
                                                                  self.instrument.instrument_staribus_baudrate,
                                                                  self.instrument.instrument_staribus_timeout)

                        else:

                            logger.debug('Instrument autodetect returned False')

                            logger.warning('Instrument autodetect true - No instrument or port found.')

                            self.status_message('system', 'PREMATURE_TERMINATION',
                                                'Starinet Relay instrument autodetect true - No instrument or port found.', None)

                            self.disable_control_panel()

                            logger.debug('Control panel disabled.')

                    else:

                        # Auto detect instrument on serial port wasn't true so lets see if
                        # we can open the configured serial port.

                        logger.debug('Checking to see if we can open configured serial port')

                        if utilities.check_serial_port(self.instrument.instrument_staribus_port):

                            logger.debug('We appear to be able to open serial port : %s' %
                                  str(self.instrument.instrument_staribus_port))

                            self.starinet_relay_state = True

                            logger.debug('Starinet Relay Active : True')

                            logger.info('########## Valid Starinet relay configuration found. ##########')
                            logger.info('Starting startinet relay')

                            self.setWindowTitle('StarbaseMini -- Version %s -- %s' % (
                                version, self.application_configuration.get('Application', 'instrument_identifier') +
                                ' Starinet Relay'))

                            starinet_relay.StarinetConnectorStart(self.application_configuration.get('StarinetRelay',
                                                                                                     'address'),
                                                                  self.application_configuration.get('StarinetRelay',
                                                                                                     'starinet_port'),
                                                                  self.instrument.instrument_staribus_port,
                                                                  self.instrument.instrument_staribus_baudrate,
                                                                  self.instrument.instrument_staribus_timeout)
                        else:

                            logger.debug('Unable to open configured serial port.')

                            logger.warning('No serial port found unable to start Starinet Relay.')

                            self.status_message('system', 'PREMATURE_TERMINATION',
                                                'Unable to initialise Starinet Relay no serial port(s) found.', None)

                            self.setWindowTitle('StarbaseMini -- Version %s -- %s' % (
                                version, self.application_configuration.get('Application', 'instrument_identifier') +
                                ' Starinet Relay'))

                            self.disable_control_panel()

                            logger.debug('Control panel disabled.')
        else:

            logger.debug('Starinet Relay Active : False')

            # Now we check to see if the configuration we have makes sense.

            # Check if Staribus to Starinet converter is enabled and if is have we a staribus instrument

            if self.instrument.instrument_staribus2starinet == 'True' and \
                    self.instrument.instrument_staribus_address == '000':

                logger.warning('Staribus to Starinet converter enabled but Starinet instrument selected')

                self.status_message('system', 'PREMATURE_TERMINATION',
                                    'Staribus to Starinet converter enabled however a Starinet instrument is enabled.',
                                    None)

                self.disable_control_panel()

                logger.debug('Control panel disabled.')

            # If we have Staribus to Starinet converter enabled is the configuration sane.

            elif self.instrument.instrument_staribus2starinet == 'True':

                logger.info('Staribus to Starinet converter found.')

                if not utilities.check_ip(self.instrument.instrument_starinet_address):

                    logger.warning('Starinet converter IP address invalid')

                    self.status_message('system', 'PREMATURE_TERMINATION', 'Starinet converter IP address invalid.',
                                        None)

                    self.disable_control_panel()

                    logger.debug('Control panel disabled.')

                elif not utilities.check_starinet_port(self.instrument.instrument_starinet_port):

                    logger.warning('Starinet converter port invalid')

                    self.status_message('system', 'PREMATURE_TERMINATION', 'Starinet converter port invalid.',
                                        None)

                    self.disable_control_panel()

                    logger.debug('Control panel disabled.')

                else:

                    logger.info('########## Valid Staribus to Starinet configuration found. ##########')

                    # At this point we make the assumption the application and instrument configuration are valid.

                    # load interpreter_class_loader

                    self.interpreter_class_loader()

                    logger.debug('Interpreter class loader called.')

            # If we have a Starinet instrument is the configuration sane

            elif self.instrument.instrument_staribus_address == '000':

                logger.info('Starinet instrument configuration found.')

                if not utilities.check_ip(self.instrument.instrument_starinet_address):

                    logger.warning('Starinet IP address invalid')

                    self.status_message('system', 'PREMATURE_TERMINATION', 'Starinet IP address invalid.', None)

                    self.disable_control_panel()

                    logger.debug('Control panel disabled.')

                elif not utilities.check_starinet_port(self.instrument.instrument_starinet_port):

                    logger.warning('Starinet port invalid')

                    self.status_message('system', 'PREMATURE_TERMINATION', 'Starinet port invalid.', None)

                    self.disable_control_panel()

                    logger.debug('Control panel disabled.')

                else:

                    logger.info('########## Valid Starinet configuration found. ##########')

                    # At this point we make the assumption the application and instrument configuration are valid.

                    # load interpreter_class_loader

                    self.interpreter_class_loader()

                    logger.debug('Interpreter class loader called.')

            # Instrument appears to be Staribus check configuration is sane.

            elif int(self.instrument.instrument_staribus_address) > 0:

                logger.info('Staribus configuration found.')

                if self.instrument.instrument_staribus_autodetect == 'True':

                    logger.info('Instrument autodetect is True')

                    if not self.instrument_autodetector():

                        logger.warning('Unable to detect instrument port')

                        self.status_message('system', 'PREMATURE_TERMINATION', 'Unable to detect instrument port.',
                                            None)

                        self.disable_control_panel()

                        logger.debug('Control panel disabled.')

                    else:

                        logger.info('########## Valid Staribus configuration found. ##########')

                        # At this point we make the assumption the application and instrument configuration are valid.

                        # load interpreter_class_loader

                        self.interpreter_class_loader()

                        logger.debug('Interpreter class loader called.')

                else:

                    logger.info('Checking serial port : %s' % self.instrument.instrument_staribus_port)

                    if not utilities.check_serial_port(self.instrument.instrument_staribus_port):

                        logger.warning('Unable to open port %s' % self.instrument.instrument_staribus_port)

                        self.status_message('system', 'PREMATURE_TERMINATION', 'Unable to open port %s' %
                                            self.instrument.instrument_staribus_port, None)

                        self.serial_port_state = False

                        # load interpreter_class_loader

                        self.interpreter_class_loader()

                        logger.debug('Interpreter class loader called.')

                        self.disable_control_panel()

                        logger.debug('Control panel disabled.')

                    else:

                        logger.info('########## Valid Staribus configuration found. ##########')

                        # At this point we make the assumption the application and instrument configuration are valid.

                        # load interpreter_class_loader

                        self.interpreter_class_loader()

                        logger.debug('Interpreter class loader called.')

            else:

                logger.critical('Unable to determine instrument configuration')

                self.status_message('system', 'Unable to determine instrument configuration.', None)

                self.disable_control_panel()

                logger.debug('Control panel disabled.')

            # Chart loader

    def instrument_datatranslator_class_loader(self):

        logger = logging.getLogger('StarbaseMini.instrument_datatranslator_class_loader')

        # Initialise datatranslator, added new datatranslators here.

        if not re.match(constants.datatranslator, self.instrument.instrument_datatranslator):

            logger.critical('Unable to locate Instrument DataTranslator')

            self.status_message('system', 'CRITICAL_ERROR', 'Unable to locate Instrument DataTranslator', None)

            return False

        else:

            if self.instrument.instrument_datatranslator == 'StaribusBlock':

                logger.info('Initialising StaribusBlock datatranslator')

                self.instrument_datatranslator = datatranslators.StaribusBlocks.StaribusBlockParser()

                logger.info('Initialising StaribusBlock csv_datatranslator')

                self.csv_datatranslator = datatranslators.StaribusBlocks.CsvParser(self.data_store)

                logger.info('Initialising StaribusBlock metadata')

                self.metadata =  datatranslators.StaribusBlocks.StaribusMetaData(self)

                logger.info('Initialising StaribusBlock data segmenter')

                self.segmenter.data_setup(self.application_configuration.user_home,
                                          self.application_configuration.get('Application', 'instrument_data_path'),
                                          self.metadata)

                # Make sure the datatranslator is reset to default values,

                self.instrument_datatranslator.clear()

                # Tell the data store about the data translator so we can parse data blocks.

                self.data_store.block_parser = self.instrument_datatranslator

                return True

    def interpreter_class_loader(self):

        # First we clear the module and command combo boxes

        self.ui.commandCombobox.clear()
        self.ui.moduleCombobox.clear()

        # Now we enable both the command and module combo boxes.

        self.ui.commandCombobox.setEnabled(True)
        self.ui.moduleCombobox.setEnabled(True)

        # If we've got this far we might as well load the instrument control panel components.

        self.populate_ui_module()

        self.populate_ui_command()

        logger = logging.getLogger('StarbaseMini.interpreter_class_loader')

        logger.info('Closing any open streams.')

        self.command_interpreter.close()

        logger.info('Starting command interpreter.')

        try:

            self.command_interpreter.start(self, self.serial_port_state, self.metadata)

        except IOError:

            logger.critical('Unable to initiate command interpreter')

            self.status_message('system', 'ABORT', 'Unable to initiate command interpreter', None)

            self.disable_control_panel()

        else:

            self.chart_class_loader()

    def chart_class_loader(self):

        logger = logging.getLogger('StarbaseMini.chart_class_loader')

        try:

            self.chart.chart_instrument_setup(self.data_store, self.instrument,
                                              self.metadata, self.application_configuration, self.data_source)
        except Exception as msg:

            logger.critical('Unable to setup chart attributes : %s' % str(msg))

            self.status_message('system', 'CRITICAL_ERROR', str(msg), None)

            self.disable_control_panel()

        else:

            logger.info('Chart attributes setup for data source instrument')

    def instrument_autodetector(self):

        logger = logging.getLogger('StarbaseMini.instrument_autodetector')

        logger.info('Instrument autodetect is True.')

        ports = utilities.serial_port_scanner()

        logger.debug('Serial ports found : %s' % str(ports))

        if ports is None:

            logger.debug('Serial ports is none')

            logger.warning('No serial ports found to scan for instrument.')

            return False

        else:

            instrument_port = utilities.check_serial_port_staribus_instrument(
                self.instrument.instrument_staribus_address, ports, self.instrument.instrument_staribus_baudrate)

            if instrument_port is None:

                logger.warning('Staribus instrument not found for address %s' %
                               self.instrument.instrument_staribus_address)

                return False

            elif len(instrument_port) > 1:

                logger.warning('Multiple Staribus instruments found defaulting to first.')

                self.status_message('system', 'WARNING',
                                    'Multiple Staribus instruments found defaulting to first.', None)

                logger.info('Setting serial port to %s' % instrument_port[0])

                self.instrument.instrument_staribus_port = instrument_port[0]

                return True

            else:

                self.status_message('system', 'INFO', ('%s instrument found.' %
                                                       self.instrument.instrument_identifier), None)

                logger.info('Setting serial port to %s' % instrument_port[0])

                self.instrument.instrument_staribus_port = instrument_port[0]

                return True

    def populate_ui_module(self):

        logger = logging.getLogger('StarbaseMini.populate_ui_module')

        logger.debug('Blocking module combobox signals.')

        self.ui.moduleCombobox.blockSignals(True)

        # Populate module combo box

        try:

            logger.info('Populating module combobox')

            index = 0

            for plugin in self.instrument.module_list:

                logger.debug('Populate module combobox with : %s' % str(plugin))

                logger.debug(str(plugin))

                self.ui.moduleCombobox.addItem(plugin[0], plugin[2])

                self.ui.moduleCombobox.setItemData(index, plugin[1], QtCore.Qt.ToolTipRole)

                index += 1

        except KeyError as msg:

            logger.critical('Populate UI Module KeyError. %s' % str(msg))

            self.status_message('system', 'ERROR', ('Populate UI Module KeyError. %s' % str(msg)), None)

            self.disable_control_panel()

        else:

            logger.debug('Module combobox populated')

            self.ui.moduleCombobox.blockSignals(False)

            self.ui.commandCombobox.setFocus()

            logger.debug('Unblocked module combobox signals.')

    def populate_ui_command(self):

        logger = logging.getLogger('StarbaseMini.populate_ui_command')

        logger.debug('Blocking command combobox signals.')

        self.ui.commandCombobox.blockSignals(True)

        # Populate command combo box

        try:

            plugin_index = self.ui.moduleCombobox.currentIndex()

            logger.debug('Populating command combobox for module : %s' % self.ui.moduleCombobox.currentText())

            logger.debug('Command Base : %s' % str(plugin_index))

            self.ui.commandCombobox.clear()

            index = 0

            for cmd in self.instrument.command_list[plugin_index]:

                logger.debug('Populate command combobox with : %s' % str(cmd))

                self.ui.commandCombobox.addItem(cmd[0], cmd[2])

                self.ui.commandCombobox.setItemData(index, cmd[1], QtCore.Qt.ToolTipRole)

                index += 1

        except KeyError as msg:

            logger.critical('Populate UI Command KeyError : %s' % str(msg))

            self.status_message('system', 'ERROR', ('Populate UI Command KeyError : %s' % str(msg)), None)

            self.disable_control_panel()

        else:

            self.ui.commandCombobox.blockSignals(False)

            self.command_parameter_populate()

            logger.debug('Unblocked command combobox signals.')

    # Get the command parameters for the current set command.

    def command_parameter_populate(self):

        logger = logging.getLogger('StarbaseMini.command_parameter_populate')

        logger.debug('Blocking command parameter line edit signals.')

        self.ui.commandParameter.blockSignals(True)

        self.ui.commandParameter.clear()

        try:

            for command in self.instrument.command_dict[self.ui.moduleCombobox.itemData(
                    self.ui.moduleCombobox.currentIndex())]:

                for key in command.keys():

                    if key == self.ui.commandCombobox.itemData(self.ui.commandCombobox.currentIndex()):

                        try:

                            # Check if command has choices.

                            if command[key]['Parameters']['Choices'] == 'None':

                                logger.debug('%s %s', self.ui.commandCombobox.currentText(), 'Parameters Choices : None')

                                self.ui.choicesComboBox.clear()

                                self.ui.choicesComboBox.setEnabled(False)

                                self.ui.executeButton.setEnabled(True)

                            else:

                                self.ui.choicesComboBox.clear()

                                self.ui.choicesComboBox.setEnabled(True)

                                self.ui.choicesComboBox.setFocus()

                                self.ui.executeButton.setEnabled(True)

                                # Split the choices up into list.

                                choices = command[key]['Parameters']['Choices'].split(',')

                                logger.debug('%s %s %s', self.ui.commandCombobox.currentText(), 'Parameters Choices :',
                                             str(choices))

                                # Add choices to combobox.
                                self.ui.choicesComboBox.addItems(choices)

                                # Add choices tool tips to combo box.
                                for i in range(len(choices)):

                                    self.ui.choicesComboBox.setItemData(i, (command[key]['Parameters']['Tooltip']),
                                                                        QtCore.Qt.ToolTipRole)

                            # Check if command has parameters.

                            if command[key]['Parameters']['Regex'] == 'None':

                                logger.debug('%s %s', self.ui.commandCombobox.currentText(), 'Parameters Regex : None')

                                self.ui.commandParameter.clear()

                                self.ui.commandParameter.setEnabled(False)

                                self.ui.commandParameter.setStyleSheet('QLineEdit { background-color: %s }' %
                                                                       self.background_colour)

                            else:

                                self.ui.commandParameter.setStyleSheet('QLineEdit { background-color: #FFFFFF }')

                                self.ui.commandParameter.setEnabled(True)

                                self.ui.commandParameter.setFocus()

                                logger.debug('Unblocking command parameter line edit signals.')

                                self.ui.commandParameter.blockSignals(False)

                                self.ui.executeButton.setEnabled(False)

                                self.ui.commandParameter.setToolTip(command[key]['Parameters']['Tooltip'])

                                self.parameter_regex = command[key]['Parameters']['Regex']

                                logger.debug('%s %s %s', self.ui.commandCombobox.currentText(),
                                             'Parameters Regex :', self.parameter_regex)

                                self.ui.commandParameter.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp(
                                                                      self.parameter_regex)))

                                # We set and then clear text to the commandParameter QLineEdit so we emit a signal
                                # and call the parameter state check.

                                self.ui.commandParameter.setText(' ')

                                self.ui.commandParameter.clear()

                        except KeyError as msg:

                            logger.critical('ERROR : Command Parameter Populate KeyError : %s' % str(msg))

                            self.status_message('system', 'ERROR', ('Command Parameter KeyError : %s' % str(msg)), None)

        except KeyError:

            pass

    def parameter_check_state(self, *args, **kwargs):

        sender = self.sender()

        validator = sender.validator()

        state = validator.validate(sender.text(), 0)[0]

        if state == QtGui.QValidator.Acceptable and len(sender.text()) == 0:

            sender.setStyleSheet('QLineEdit { background-color: #f6989d }')  # red

            self.ui.executeButton.setEnabled(False)

        elif state == QtGui.QValidator.Acceptable:

            sender.setStyleSheet('QLineEdit { background-color: #c4df9b }')  # green

            self.ui.executeButton.setEnabled(True)

        elif state == QtGui.QValidator.Intermediate and len(sender.text()) == 0:

            sender.setStyleSheet('QLineEdit { background-color: #f6989d }')  # red

            self.ui.executeButton.setEnabled(False)

        elif state == QtGui.QValidator.Intermediate:

            sender.setStyleSheet('QLineEdit { background-color: #fff79a }')  # yellow

            self.ui.executeButton.setEnabled(False)


    def execute_triggered(self):

        logger = logging.getLogger('StarbaseMini.execute_triggered')

        logger.debug('Module : %s' % self.ui.moduleCombobox.itemData(self.ui.moduleCombobox.currentIndex()))
        logger.debug('Command : %s' % self.ui.commandCombobox.itemData(self.ui.commandCombobox.currentIndex()))
        logger.debug('Choice : %s' % self.ui.choicesComboBox.currentText())
        logger.debug('Parameter : %s' % self.ui.commandParameter.text())

        self.ui.executeButton.blockSignals(True)

        # Interpreter_reponse will always return a tuple consisting of command identification, status, data, units

        interpreter_response = self.command_interpreter.process_command(self.ui.moduleCombobox.itemData(
                                                                        self.ui.moduleCombobox.currentIndex()),
                                                                        self.ui.commandCombobox.itemData(
                                                                        self.ui.commandCombobox.currentIndex()),
                                                                        self.ui.choicesComboBox.currentText(),
                                                                        self.ui.commandParameter.text())


        # If interpreter_response data store parameter is not None then we'll send the status back after we attempt
        # to process the data otherwise we call statusMessage now.

        if self.data_store.RawDataBlocksAvailable:  # Do we have data to translate?  True or False

            # Create the data store arrays

            if self.data_store.create_arrays():

                self.status_message(interpreter_response[0], interpreter_response[1], interpreter_response[2],
                                    interpreter_response[3])

                # Set RawDataBlocksAvailable back to False

                self.data_store.RawDataBlocksAvailable = False

                response = self.chart.add_data('raw')

                if response[0] != 'SUCCESS':
                    self.status_message(interpreter_response[0], response[1], 'Plotting error!!', None)
                else:
                    self.chart_control_panel(self.instrument)

            else:

                self.status_message(interpreter_response[0], 'PREMATURE_TERMINATION', 'Unable to parse data!', None)


        else:

            self.status_message(interpreter_response[0], interpreter_response[1], interpreter_response[2], interpreter_response[3])

        self.ui.executeButton.blockSignals(False)

    def open_csv_file(self):

        logger = logging.getLogger('StarbaseMini.open_csv_file')

        if not utilities.data_state_check(self.data_store, 'standard'):

            self.status_message('openCsv', 'ABORT', self.data_store.data_state()[1], None)

        else:

            # Reset the data store.

            self.data_store.clear()

            # Now get the path and filename of the CSV file we want to open.

            response = core.importer(self.application_configuration.user_home, self.application_configuration.get('Application', 'instrument_data_path'))

            # If response[0] starts with Success we run the csv_parse

            if response[0].startswith('SUCCESS'):

                response = self.csv_datatranslator.parse(response[1], self.metadata)

                # self.data_store.print_state()

                # if response[0] starts with success we see if we can run the metadata deconstructor.

                try:
                    if response[0].startswith('SUCCESS'):

                        # Create the data store arrays

                        if self.data_store.create_arrays():

                            self.status_message('openCSV', response[0], response[1], None)

                            logger.debug('openCSV calling add_data')

                            response = self.chart.add_data('rawCsv')

                            if response[0] != 'SUCCESS':
                                self.status_message('openCSV', response[1], 'Plotting error!!', None)
                            else:
                                self.chart_control_panel(self.metadata)

                        else:

                            self.status_message('openCSV', 'PREMATURE_TERMINATON', 'Unable to parse data!', None)

                    else:

                        self.status_message('openCSV', response[0], response[1], None)

                except TypeError:

                    self.status_message('openCSV', 'PREMATURE_TERMINATON', 'No data!', None)

            else:

                self.status_message('openCSV', 'ABORT', None, None)

    def save_data(self, data_style_type):

        save_data_identifity = 'save' + data_style_type.title() + 'Data'

        response = core.exporter(data_style_type, self.metadata, self.data_store,
                                 self.application_configuration.user_home,
                                 self.application_configuration.get('Application', 'instrument_data_path'))

        self.status_message(save_data_identifity, response[0], response[1], None)

    def segment_data(self, period, data_style_type):

        segment_data_identifer = 'segment' + data_style_type.title() + 'Data(' + str(period) + ')'

        response = self.segmenter.segment_timeseries(data_style_type, period)

        self.status_message(segment_data_identifer, response[0], response[1], None)

    def filter_data(self, filter_):

        filter_indentifer = 'filter(' + filter_ + ')'

        if filter_ == 'NonLinearStaticRemover':

            response = filters.NonLinearStaticRemover.non_linear_static_remover(self.data_store)

        elif filter_ == 'PeakExtractor':

            response = filters.PeakExtractor.peak_extractor(self.data_store)

        elif filter_ == 'RunningAverage':

            response = filters.RunningAverage.running_average(self.data_store)

        elif filter_ == 'WeightedRunningAverage':

            response = filters.WeightedRunningAverage.weighted_running_average(self.data_store)

        else:

            response = 'PREMATURE_TERMINATION', 'Unknown filter type'

        # TODO if response is success then run chart routine.

        self.status_message(filter_indentifer, response[0], response[1], None)


    ############################  BELOW MIGHT GET CHANGED IT'S FROM STARBASEMINI II ##############################


    def channel_triggered(self, channel, state):

        if state:
            self.chart.channel_control(channel, True)
        else:
            self.chart.channel_control(channel, False)

    def chart_control_panel(self, translated):

        self.ui.showLegend.setEnabled(True)

        self.ui.channel0Button.setVisible(False)
        self.ui.channel0colour.setVisible(False)
        self.ui.channel1Button.setVisible(False)
        self.ui.channel1colour.setVisible(False)
        self.ui.channel2Button.setVisible(False)
        self.ui.channel2colour.setVisible(False)
        self.ui.channel3Button.setVisible(False)
        self.ui.channel3colour.setVisible(False)
        self.ui.channel4Button.setVisible(False)
        self.ui.channel4colour.setVisible(False)
        self.ui.channel5Button.setVisible(False)
        self.ui.channel5colour.setVisible(False)
        self.ui.channel6Button.setVisible(False)
        self.ui.channel6colour.setVisible(False)
        self.ui.channel7Button.setVisible(False)
        self.ui.channel7colour.setVisible(False)
        self.ui.channel8Button.setVisible(False)
        self.ui.channel8colour.setVisible(False)

        if self.data_store.channel_count == 1:
            self.ui.channel0Button.setEnabled(True)
            self.ui.channel0Button.setChecked(True)
            self.ui.channel0colour.setStyleSheet('QCheckBox::indicator {background-color: '
                                                 + translated.channel_colours[0] + '; }')
            self.ui.channel0Button.setText(translated.channel_names[0])
            self.ui.channel0Button.setVisible(True)
            self.ui.channel0colour.setVisible(True)
            self.ui.channel1Button.setVisible(False)
            self.ui.channel1colour.setVisible(False)
            self.ui.channel2Button.setVisible(False)
            self.ui.channel2colour.setVisible(False)
            self.ui.channel3Button.setVisible(False)
            self.ui.channel3colour.setVisible(False)
            self.ui.channel4Button.setVisible(False)
            self.ui.channel4colour.setVisible(False)
            self.ui.channel5Button.setVisible(False)
            self.ui.channel5colour.setVisible(False)
            self.ui.channel6Button.setVisible(False)
            self.ui.channel6colour.setVisible(False)
            self.ui.channel7Button.setVisible(False)
            self.ui.channel7colour.setVisible(False)
            self.ui.channel8Button.setVisible(False)
            self.ui.channel8colour.setVisible(False)
        elif self.data_store.channel_count == 2:
            self.ui.channel0Button.setEnabled(True)
            self.ui.channel0Button.setChecked(True)
            self.ui.channel0colour.setStyleSheet('QCheckBox::indicator {background-color: '
                                                 + translated.channel_colours[0] + '; }')
            self.ui.channel1Button.setEnabled(True)
            self.ui.channel1Button.setChecked(True)
            self.ui.channel1colour.setStyleSheet('QCheckBox::indicator {background-color: '
                                                 + translated.channel_colours[1] + '; }')
            self.ui.channel0Button.setText(translated.channel_names[0])
            self.ui.channel1Button.setText(translated.channel_names[1])
            self.ui.channel0Button.setVisible(True)
            self.ui.channel0colour.setVisible(True)
            self.ui.channel1Button.setVisible(True)
            self.ui.channel1colour.setVisible(True)
            self.ui.channel2Button.setVisible(False)
            self.ui.channel2colour.setVisible(False)
            self.ui.channel3Button.setVisible(False)
            self.ui.channel3colour.setVisible(False)
            self.ui.channel4Button.setVisible(False)
            self.ui.channel4colour.setVisible(False)
            self.ui.channel5Button.setVisible(False)
            self.ui.channel5colour.setVisible(False)
            self.ui.channel6Button.setVisible(False)
            self.ui.channel6colour.setVisible(False)
            self.ui.channel7Button.setVisible(False)
            self.ui.channel7colour.setVisible(False)
            self.ui.channel8Button.setVisible(False)
            self.ui.channel8colour.setVisible(False)
        elif self.data_store.channel_count == 3:
            self.ui.channel0Button.setEnabled(True)
            self.ui.channel0Button.setChecked(True)
            self.ui.channel0colour.setStyleSheet('QCheckBox::indicator {background-color: '
                                                 + translated.channel_colours[0] + '; }')
            self.ui.channel1Button.setEnabled(True)
            self.ui.channel1Button.setChecked(True)
            self.ui.channel1colour.setStyleSheet('QCheckBox::indicator {background-color: '
                                                 + translated.channel_colours[1] + '; }')
            self.ui.channel2Button.setEnabled(True)
            self.ui.channel2Button.setChecked(True)
            self.ui.channel2colour.setStyleSheet('QCheckBox::indicator {background-color: '
                                                 + translated.channel_colours[2] + '; }')
            self.ui.channel0Button.setText(translated.channel_names[0])
            self.ui.channel1Button.setText(translated.channel_names[1])
            self.ui.channel2Button.setText(translated.channel_names[2])
            self.ui.channel0Button.setVisible(True)
            self.ui.channel0colour.setVisible(True)
            self.ui.channel1Button.setVisible(True)
            self.ui.channel1colour.setVisible(True)
            self.ui.channel2Button.setVisible(True)
            self.ui.channel2colour.setVisible(True)
            self.ui.channel3Button.setVisible(False)
            self.ui.channel3colour.setVisible(False)
            self.ui.channel4Button.setVisible(False)
            self.ui.channel4colour.setVisible(False)
            self.ui.channel5Button.setVisible(False)
            self.ui.channel5colour.setVisible(False)
            self.ui.channel6Button.setVisible(False)
            self.ui.channel6colour.setVisible(False)
            self.ui.channel7Button.setVisible(False)
            self.ui.channel7colour.setVisible(False)
            self.ui.channel8Button.setVisible(False)
            self.ui.channel8colour.setVisible(False)
        elif self.data_store.channel_count == 4:
            self.ui.channel0Button.setEnabled(True)
            self.ui.channel0Button.setChecked(True)
            self.ui.channel0colour.setStyleSheet('QCheckBox::indicator {background-color: '
                                                 + translated.channel_colours[0] + '; }')
            self.ui.channel1Button.setEnabled(True)
            self.ui.channel1Button.setChecked(True)
            self.ui.channel1colour.setStyleSheet('QCheckBox::indicator {background-color: '
                                                 + translated.channel_colours[1] + '; }')
            self.ui.channel2Button.setEnabled(True)
            self.ui.channel2Button.setChecked(True)
            self.ui.channel2colour.setStyleSheet('QCheckBox::indicator {background-color: '
                                                 + translated.channel_colours[2] + '; }')
            self.ui.channel3Button.setEnabled(True)
            self.ui.channel3Button.setChecked(True)
            self.ui.channel3colour.setStyleSheet('QCheckBox::indicator {background-color: '
                                                 + translated.channel_colours[3] + '; }')
            self.ui.channel0Button.setText(translated.channel_names[0])
            self.ui.channel1Button.setText(translated.channel_names[1])
            self.ui.channel2Button.setText(translated.channel_names[2])
            self.ui.channel3Button.setText(translated.channel_names[3])
            self.ui.channel4Button.setVisible(False)
            self.ui.channel4colour.setVisible(False)
            self.ui.channel5Button.setVisible(False)
            self.ui.channel5colour.setVisible(False)
            self.ui.channel6Button.setVisible(False)
            self.ui.channel6colour.setVisible(False)
            self.ui.channel7Button.setVisible(False)
            self.ui.channel7colour.setVisible(False)
            self.ui.channel8Button.setVisible(False)
            self.ui.channel8colour.setVisible(False)
        elif self.data_store.channel_count == 5:
            self.ui.channel0Button.setEnabled(True)
            self.ui.channel0Button.setChecked(True)
            self.ui.channel0colour.setStyleSheet('QCheckBox::indicator {background-color: '
                                                 + translated.channel_colours[0] + '; }')
            self.ui.channel1Button.setEnabled(True)
            self.ui.channel1Button.setChecked(True)
            self.ui.channel1colour.setStyleSheet('QCheckBox::indicator {background-color: '
                                                 + translated.channel_colours[1] + '; }')
            self.ui.channel2Button.setEnabled(True)
            self.ui.channel2Button.setChecked(True)
            self.ui.channel2colour.setStyleSheet('QCheckBox::indicator {background-color: '
                                                 + translated.channel_colours[2] + '; }')
            self.ui.channel3Button.setEnabled(True)
            self.ui.channel3Button.setChecked(True)
            self.ui.channel3colour.setStyleSheet('QCheckBox::indicator {background-color: '
                                                 + translated.channel_colours[3] + '; }')
            self.ui.channel4Button.setEnabled(True)
            self.ui.channel4Button.setChecked(True)
            self.ui.channel4colour.setStyleSheet('QCheckBox::indicator {background-color: '
                                                 + translated.channel_colours[4] + '; }')
            self.ui.channel0Button.setText(translated.channel_names[0])
            self.ui.channel1Button.setText(translated.channel_names[1])
            self.ui.channel2Button.setText(translated.channel_names[2])
            self.ui.channel3Button.setText(translated.channel_names[3])
            self.ui.channel4Button.setText(translated.channel_names[4])
            self.ui.channel0Button.setVisible(True)
            self.ui.channel0colour.setVisible(True)
            self.ui.channel1Button.setVisible(True)
            self.ui.channel1colour.setVisible(True)
            self.ui.channel2Button.setVisible(True)
            self.ui.channel2colour.setVisible(True)
            self.ui.channel3Button.setVisible(True)
            self.ui.channel3colour.setVisible(True)
            self.ui.channel4Button.setVisible(True)
            self.ui.channel4colour.setVisible(True)
            self.ui.channel5Button.setVisible(False)
            self.ui.channel5colour.setVisible(False)
            self.ui.channel6Button.setVisible(False)
            self.ui.channel6colour.setVisible(False)
            self.ui.channel7Button.setVisible(False)
            self.ui.channel7colour.setVisible(False)
            self.ui.channel8Button.setVisible(False)
            self.ui.channel8colour.setVisible(False)
        elif self.data_store.channel_count == 6:
            self.ui.channel0Button.setEnabled(True)
            self.ui.channel0Button.setChecked(True)
            self.ui.channel0colour.setStyleSheet('QCheckBox::indicator {background-color: '
                                                 + translated.channel_colours[0] + '; }')
            self.ui.channel1Button.setEnabled(True)
            self.ui.channel1Button.setChecked(True)
            self.ui.channel1colour.setStyleSheet('QCheckBox::indicator {background-color: '
                                                 + translated.channel_colours[1] + '; }')
            self.ui.channel2Button.setEnabled(True)
            self.ui.channel2Button.setChecked(True)
            self.ui.channel2colour.setStyleSheet('QCheckBox::indicator {background-color: '
                                                 + translated.channel_colours[2] + '; }')
            self.ui.channel3Button.setEnabled(True)
            self.ui.channel3Button.setChecked(True)
            self.ui.channel3colour.setStyleSheet('QCheckBox::indicator {background-color: '
                                                 + translated.channel_colours[3] + '; }')
            self.ui.channel4Button.setEnabled(True)
            self.ui.channel4Button.setChecked(True)
            self.ui.channel4colour.setStyleSheet('QCheckBox::indicator {background-color: '
                                                 + translated.channel_colours[4] + '; }')
            self.ui.channel5Button.setEnabled(True)
            self.ui.channel5Button.setChecked(True)
            self.ui.channel5colour.setStyleSheet('QCheckBox::indicator {background-color: '
                                                 + translated.channel_colours[5] + '; }')
            self.ui.channel0Button.setText(translated.channel_names[0])
            self.ui.channel1Button.setText(translated.channel_names[1])
            self.ui.channel2Button.setText(translated.channel_names[2])
            self.ui.channel3Button.setText(translated.channel_names[3])
            self.ui.channel4Button.setText(translated.channel_names[4])
            self.ui.channel5Button.setText(translated.channel_names[5])
            self.ui.channel0Button.setVisible(True)
            self.ui.channel0colour.setVisible(True)
            self.ui.channel1Button.setVisible(True)
            self.ui.channel1colour.setVisible(True)
            self.ui.channel2Button.setVisible(True)
            self.ui.channel2colour.setVisible(True)
            self.ui.channel3Button.setVisible(True)
            self.ui.channel3colour.setVisible(True)
            self.ui.channel4Button.setVisible(True)
            self.ui.channel4colour.setVisible(True)
            self.ui.channel5Button.setVisible(True)
            self.ui.channel5colour.setVisible(True)
            self.ui.channel6Button.setVisible(False)
            self.ui.channel6colour.setVisible(False)
            self.ui.channel7Button.setVisible(False)
            self.ui.channel7colour.setVisible(False)
            self.ui.channel8Button.setVisible(False)
            self.ui.channel8colour.setVisible(False)
        elif self.data_store.channel_count == 7:
            self.ui.channel0Button.setEnabled(True)
            self.ui.channel0Button.setChecked(True)
            self.ui.channel0colour.setStyleSheet('QCheckBox::indicator {background-color: '
                                                 + translated.channel_colours[0] + '; }')
            self.ui.channel1Button.setEnabled(True)
            self.ui.channel1Button.setChecked(True)
            self.ui.channel1colour.setStyleSheet('QCheckBox::indicator {background-color: '
                                                 + translated.channel_colours[1] + '; }')
            self.ui.channel2Button.setEnabled(True)
            self.ui.channel2Button.setChecked(True)
            self.ui.channel2colour.setStyleSheet('QCheckBox::indicator {background-color: '
                                                 + translated.channel_colours[2] + '; }')
            self.ui.channel3Button.setEnabled(True)
            self.ui.channel3Button.setChecked(True)
            self.ui.channel3colour.setStyleSheet('QCheckBox::indicator {background-color: '
                                                 + translated.channel_colours[3] + '; }')
            self.ui.channel4Button.setEnabled(True)
            self.ui.channel4Button.setChecked(True)
            self.ui.channel4colour.setStyleSheet('QCheckBox::indicator {background-color: '
                                                 + translated.channel_colours[4] + '; }')
            self.ui.channel5Button.setEnabled(True)
            self.ui.channel5Button.setChecked(True)
            self.ui.channel5colour.setStyleSheet('QCheckBox::indicator {background-color: '
                                                 + translated.channel_colours[5] + '; }')
            self.ui.channel6Button.setEnabled(True)
            self.ui.channel6Button.setChecked(True)
            self.ui.channel6colour.setStyleSheet('QCheckBox::indicator {background-color: '
                                                 + translated.channel_colours[6] + '; }')
            self.ui.channel0Button.setText(translated.channel_names[0])
            self.ui.channel1Button.setText(translated.channel_names[1])
            self.ui.channel2Button.setText(translated.channel_names[2])
            self.ui.channel3Button.setText(translated.channel_names[3])
            self.ui.channel4Button.setText(translated.channel_names[4])
            self.ui.channel5Button.setText(translated.channel_names[5])
            self.ui.channel6Button.setText(translated.channel_names[6])
            self.ui.channel0Button.setVisible(True)
            self.ui.channel0colour.setVisible(True)
            self.ui.channel1Button.setVisible(True)
            self.ui.channel1colour.setVisible(True)
            self.ui.channel2Button.setVisible(True)
            self.ui.channel2colour.setVisible(True)
            self.ui.channel3Button.setVisible(True)
            self.ui.channel3colour.setVisible(True)
            self.ui.channel4Button.setVisible(True)
            self.ui.channel4colour.setVisible(True)
            self.ui.channel5Button.setVisible(True)
            self.ui.channel5colour.setVisible(True)
            self.ui.channel6Button.setVisible(True)
            self.ui.channel6colour.setVisible(True)
            self.ui.channel7Button.setVisible(False)
            self.ui.channel7colour.setVisible(False)
            self.ui.channel8Button.setVisible(False)
            self.ui.channel8colour.setVisible(False)
        elif self.data_store.channel_count == 8:
            self.ui.channel0Button.setEnabled(True)
            self.ui.channel0Button.setChecked(True)
            self.ui.channel0colour.setStyleSheet('QCheckBox::indicator {background-color: '
                                                 + translated.channel_colours[0] + '; }')
            self.ui.channel1Button.setEnabled(True)
            self.ui.channel1Button.setChecked(True)
            self.ui.channel1colour.setStyleSheet('QCheckBox::indicator {background-color: '
                                                 + translated.channel_colours[1] + '; }')
            self.ui.channel2Button.setEnabled(True)
            self.ui.channel2Button.setChecked(True)
            self.ui.channel2colour.setStyleSheet('QCheckBox::indicator {background-color: '
                                                 + translated.channel_colours[2] + '; }')
            self.ui.channel3Button.setEnabled(True)
            self.ui.channel3Button.setChecked(True)
            self.ui.channel3colour.setStyleSheet('QCheckBox::indicator {background-color: '
                                                 + translated.channel_colours[3] + '; }')
            self.ui.channel4Button.setEnabled(True)
            self.ui.channel4Button.setChecked(True)
            self.ui.channel4colour.setStyleSheet('QCheckBox::indicator {background-color: '
                                                 + translated.channel_colours[4] + '; }')
            self.ui.channel5Button.setEnabled(True)
            self.ui.channel5Button.setChecked(True)
            self.ui.channel5colour.setStyleSheet('QCheckBox::indicator {background-color: '
                                                 + translated.channel_colours[5] + '; }')
            self.ui.channel6Button.setEnabled(True)
            self.ui.channel6Button.setChecked(True)
            self.ui.channel6colour.setStyleSheet('QCheckBox::indicator {background-color: '
                                                 + translated.channel_colours[6] + '; }')
            self.ui.channel7Button.setEnabled(True)
            self.ui.channel7Button.setChecked(True)
            self.ui.channel7colour.setStyleSheet('QCheckBox::indicator {background-color: '
                                                 + translated.channel_colours[7] + '; }')
            self.ui.channel0Button.setVisible(True)
            self.ui.channel0colour.setVisible(True)
            self.ui.channel1Button.setVisible(True)
            self.ui.channel1colour.setVisible(True)
            self.ui.channel2Button.setVisible(True)
            self.ui.channel2colour.setVisible(True)
            self.ui.channel3Button.setVisible(True)
            self.ui.channel3colour.setVisible(True)
            self.ui.channel4Button.setVisible(True)
            self.ui.channel4colour.setVisible(True)
            self.ui.channel5Button.setVisible(True)
            self.ui.channel5colour.setVisible(True)
            self.ui.channel6Button.setVisible(True)
            self.ui.channel6colour.setVisible(True)
            self.ui.channel7Button.setVisible(True)
            self.ui.channel7colour.setVisible(True)
            self.ui.channel0Button.setText(translated.channel_names[0])
            self.ui.channel1Button.setText(translated.channel_names[1])
            self.ui.channel2Button.setText(translated.channel_names[2])
            self.ui.channel3Button.setText(translated.channel_names[3])
            self.ui.channel4Button.setText(translated.channel_names[4])
            self.ui.channel5Button.setText(translated.channel_names[5])
            self.ui.channel6Button.setText(translated.channel_names[6])
            self.ui.channel7Button.setText(translated.channel_names[7])
            self.ui.channel8Button.setVisible(False)
            self.ui.channel8colour.setVisible(False)
        elif self.data_store.channel_count == 9:
            self.ui.channel0Button.setEnabled(True)
            self.ui.channel0Button.setChecked(True)
            self.ui.channel0colour.setStyleSheet('QCheckBox::indicator {background-color: '
                                                 + translated.channel_colours[0] + '; }')
            self.ui.channel1Button.setEnabled(True)
            self.ui.channel1Button.setChecked(True)
            self.ui.channel1colour.setStyleSheet('QCheckBox::indicator {background-color: '
                                                 + translated.channel_colours[1] + '; }')
            self.ui.channel2Button.setEnabled(True)
            self.ui.channel2Button.setChecked(True)
            self.ui.channel2colour.setStyleSheet('QCheckBox::indicator {background-color: '
                                                 + translated.channel_colours[2] + '; }')
            self.ui.channel3Button.setEnabled(True)
            self.ui.channel3Button.setChecked(True)
            self.ui.channel3colour.setStyleSheet('QCheckBox::indicator {background-color: '
                                                 + translated.channel_colours[3] + '; }')
            self.ui.channel4Button.setEnabled(True)
            self.ui.channel4Button.setChecked(True)
            self.ui.channel4colour.setStyleSheet('QCheckBox::indicator {background-color: '
                                                 + translated.channel_colours[4] + '; }')
            self.ui.channel5Button.setEnabled(True)
            self.ui.channel5Button.setChecked(True)
            self.ui.channel5colour.setStyleSheet('QCheckBox::indicator {background-color: '
                                                 + translated.channel_colours[5] + '; }')
            self.ui.channel6Button.setEnabled(True)
            self.ui.channel6Button.setChecked(True)
            self.ui.channel6colour.setStyleSheet('QCheckBox::indicator {background-color: '
                                                 + translated.channel_colours[6] + '; }')
            self.ui.channel7Button.setEnabled(True)
            self.ui.channel7Button.setChecked(True)
            self.ui.channel7colour.setStyleSheet('QCheckBox::indicator {background-color: '
                                                 + translated.channel_colours[7] + '; }')
            self.ui.channel8Button.setEnabled(True)
            self.ui.channel8Button.setChecked(True)
            self.ui.channel8colour.setStyleSheet('QCheckBox::indicator {background-color: '
                                                 + translated.channel_colours[8] + '; }')
            self.ui.channel0Button.setText(translated.channel_names[0])
            self.ui.channel1Button.setText(translated.channel_names[1])
            self.ui.channel2Button.setText(translated.channel_names[2])
            self.ui.channel3Button.setText(translated.channel_names[3])
            self.ui.channel4Button.setText(translated.channel_names[4])
            self.ui.channel5Button.setText(translated.channel_names[5])
            self.ui.channel6Button.setText(translated.channel_names[6])
            self.ui.channel7Button.setText(translated.channel_names[7])
            self.ui.channel8Button.setText(translated.channel_names[8])
            self.ui.channel0Button.setVisible(True)
            self.ui.channel0colour.setVisible(True)
            self.ui.channel1Button.setVisible(True)
            self.ui.channel1colour.setVisible(True)
            self.ui.channel2Button.setVisible(True)
            self.ui.channel2colour.setVisible(True)
            self.ui.channel3Button.setVisible(True)
            self.ui.channel3colour.setVisible(True)
            self.ui.channel4Button.setVisible(True)
            self.ui.channel4colour.setVisible(True)
            self.ui.channel5Button.setVisible(True)
            self.ui.channel5colour.setVisible(True)
            self.ui.channel6Button.setVisible(True)
            self.ui.channel6colour.setVisible(True)
            self.ui.channel7Button.setVisible(True)
            self.ui.channel7colour.setVisible(True)
            self.ui.channel8Button.setVisible(True)
            self.ui.channel8colour.setVisible(True)
        else:
            self.status_message('system', 'ERROR', 'Number of channels out of bounds.', None)
            # self.logger.warning('Index Error, Number of channels out of bounds. %s' % number_of_channels)

    # ----------------------------------------
    # Chart show legend method.
    # ----------------------------------------

    def chart_show_legend_triggered(self):
        if self.ui.showLegend.isChecked():
            self.chart.chart_legend(True)
        else:
            self.chart.chart_legend(False)

    def disable_control_panel(self):

        logger = logging.getLogger('StarbaseMini.disable_control_panel')

        logger.info('Instrument control panel disabled.')

        self.ui.commandCombobox.blockSignals(True)

        logger.debug('Blocked command combobox signals')

        self.ui.moduleCombobox.blockSignals(True)

        logger.debug('Blocked module combobox signals')

        self.ui.commandParameter.blockSignals(True)

        logger.debug('Blocked command parameter lineedit signals')

        self.ui.moduleCombobox.setEnabled(False)

        self.ui.commandCombobox.setEnabled(False)

        self.ui.commandParameter.setEnabled(False)

        self.ui.choicesComboBox.setEnabled(False)

        self.ui.executeButton.setEnabled(False)

        self.status_message('system', 'INFO', 'Instrument control panel disabled.', None)

    def status_message(self, ident, status, response_value, units):

        logger = logging.getLogger('StarbaseMini.status_message')

        logger.info('########## ' + str(ident) + ' ' + str(status) + ' ' + str(response_value) + ' ##########')

        dateTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        self.ui.statusMessage.insertRow(self.statusMessageIndex)

        self.ui.statusMessage.setItem(self.statusMessageIndex, 0, QtGui.QTableWidgetItem(dateTime))

        if ident is not None:

            self.ui.statusMessage.setItem(self.statusMessageIndex, 1, QtGui.QTableWidgetItem(ident))

        if status is not None:

            self.ui.statusMessage.setItem(self.statusMessageIndex, 2, QtGui.QTableWidgetItem(status))

        if units is not None:

            self.ui.statusMessage.setItem(self.statusMessageIndex, 3, QtGui.QTableWidgetItem(units))

        if response_value is not None:

            response_value = response_value.replace(constants.RS, '  ')

            self.ui.statusMessage.setItem(self.statusMessageIndex, 4, QtGui.QTableWidgetItem(response_value))

        # Make sure the last item set is visible.
        self.ui.statusMessage.scrollToBottom()

        self.statusMessageIndex += 1

    # Call configuration tool method

    def configuration_triggered(self):

        logger = logging.getLogger('StarbaseMini.configuration_triggered')

        logger.info('Calling configuration tool.')

        self.configuration_tool_dialog.exec_()

        self.status_message('configuration', self.configuration_tool_dialog.response_message[0],
                            self.configuration_tool_dialog.response_message[1], None)

        if self.configuration_tool_dialog.response_message[0] == 'SUCCESS':

            self.find_instrument_names_filenames_xml()

    #  Upgrade checker

    def updateCaption(self):

        self.status_message('system', 'INFO', 'Checking for application upgrade.', None)

        upgrade = utilities.Upgrader()

        message = upgrade.detect_upgrade(version)

        if message is not None:

            self.status_message('system', message[0], message[1], None)

        else:

            self.status_message('system', 'INFO', 'No upgrade currently available.', None)

    def instrument_attrib_triggered(self):

        logger = logging.getLogger('StarbaseMini.instrument_attrib_triggered')

        logger.info('Calling edit instrument attributes.')

        self.instrument_attributes_dialog.reset_dialog()

        self.instrument_attributes_dialog.set(self.instrument,
                                              self.instrument_filenames[self.instrument_names.index(
                                              self.application_configuration.get('Application', 'instrument_identifier'))],
                                              self.application_configuration.user_home)

        self.instrument_attributes_dialog.exec_()

        self.status_message('instrumentAttributes', self.instrument_attributes_dialog.response_message[0],
                            self.instrument_attributes_dialog.response_message[1], None)

        if self.instrument_attributes_dialog.response_message[0] == 'SUCCESS':

            self.find_instrument_names_filenames_xml()

    def closeEvent(self, event):

        if not utilities.data_state_check(self.data_store, 'exit'):

            event.ignore()

        else:

            event.accept()

    def toolbox_icon_control(self, current_index):

        pass

        # # Index 0 is instrument panel and index 1 is chart control panel

        if current_index == 0:
            self.ui.toolBox.setItemIcon(0, QtGui.QIcon(QtGui.QPixmap('icons/on.png')))
            self.ui.toolBox.setItemIcon(1, QtGui.QIcon(QtGui.QPixmap('icons/off.png')))
        elif current_index == 1:
            self.ui.toolBox.setItemIcon(0, QtGui.QIcon(QtGui.QPixmap('icons/off.png')))
            self.ui.toolBox.setItemIcon(1, QtGui.QIcon(QtGui.QPixmap('icons/on.png')))


    def help_about_triggered(self):

        QtGui.QMessageBox.information(None, None,
                                      "<p align='center'>StarbaseMini " + version + "<br><br>(c) 2016 Mark Horn<br>"
                                                                                    "<br>mhorn71@gmail.com</p>")

    def release_notes_triggered(self):

        self.release_note_dialog.exec_()

    def metadata_viewer_editor(self):

        self.metadata_viewer_editor_dialog.clear()

        self.metadata_viewer_editor_dialog.update_ui(self.metadata)

        self.metadata_viewer_editor_dialog.exec_()

        self.status_message('metadata', self.metadata_viewer_editor_dialog.response_message[0],
                            self.metadata_viewer_editor_dialog.response_message[1], None)

    def dataview(self, data_style_type):

        if len(self.data_store.RawData) == 0 and data_style_type == 'raw':
        
            self.status_message('RawDataViewer', 'PREMATURE_TERMINATION', 'No data!', None)
        
        elif len(self.data_store.ProcessedData) == 0 and data_style_type == 'processed':
        
            self.status_message('ProcessedDataViewer', 'PREMATURE_TERMINATION', 'No data!', None)
        
        else:
            
            self.data_viewer.load(data_style_type, self.metadata)
            self.data_viewer.exec_()


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    myapp = Main()
    myapp.showMaximized()
    myapp.show()
    x = app.exec_()
    sys.exit(x)