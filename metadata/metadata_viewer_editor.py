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
import sys

from PyQt4 import QtGui, QtCore

from ui import Ui_MetadataDialog


class MetadataViewerEditor(QtGui.QDialog, Ui_MetadataDialog):
    def __init__(self, data_store):
        QtGui.QDialog.__init__(self)
        self.setupUi(self)

        # Style sheets
        stylebool = False

        if sys.platform.startswith('darwin'):
            stylesheet = 'css/macStyle.css'
            stylebool = True
        elif sys.platform.startswith('win32'):
            stylesheet = 'css/winStyle.css'
            stylebool = True
        elif sys.platform.startswith('linux'):
            stylesheet = 'css/nixStyle.css'
            stylebool = True

        if stylebool:
            with open(stylesheet, 'r') as style:
                self.setStyleSheet(style.read())

        self.data_store = data_store

        self.observation_note = None

        self.response_message = 'ABORT', None

        self.metadataEdit.setReadOnly(True)
        self.metadataNotesEdit.setFocus()

        self.buttonBox.button(QtGui.QDialogButtonBox.Save).clicked.connect(self.save_called)
        self.buttonBox.button(QtGui.QDialogButtonBox.Close).clicked.connect(lambda: self.close())

        # Observer.Notes,The Observer Notes,String,Dimensionless,The Observer Notes

    def clear(self):

        logger = logging.getLogger('metadata.MetadataViewerEditor.clear')
        
        logger.debug('Reset defaults.')

        self.observation_note = None

        self.response_message = 'ABORT', None

    def update_ui(self):

        self.metadataEdit.clear()
        self.metadataNotesEdit.clear()

        # Check to see if we've imported metadata and if so display it.

        if len(self.data_store.MetadataCsv) == 0:

            self.metadataEdit.setText("No data available, this box is only populated when source data is from csv file.")

        else:

            for line in self.data_store.MetadataCsv:

                metadata = line.split(',')

                data = metadata[0] + ' -- ' + metadata[1] + '\n'

                if metadata[0] == 'Observation.Notes':

                    self.metadataNotesEdit.append(metadata[1])

                    self.observation_note = metadata[1]

                else:

                    self.metadataEdit.append(data)

    def save_called(self):

        logger = logging.getLogger('metadata.MetadataViewerEditor.save_called.')

        if self.data_store.DataSource == 'Controller':

            if len(self.metadataNotesEdit.toPlainText()) != 0:

                self.data_store.ObserverationNoteMetadata = ('Observation.Notes,' + self.metadataNotesEdit.toPlainText() +
                                                             ',String,Dimensionless,The Observation Notes')

                self.response_message = 'SUCCESS', None

            else:

                self.data_store.ObserverationNoteMetadata = None

                self.response_message = 'SUCCESS', None

        elif self.data_store.DataSource == 'CSV':

            trip = True
            observation_note_present = False
            observation_note_index = 0

            for line in self.data_store.MetadataCsv:

                if line.startswith('Observation.Notes'):

                    logger.debug("Line starts with Obs Note")

                    observation_note_present = True
                    observation_note_index = self.data_store.MetadataCsv.index(line)

            if observation_note_present:

                logger.debug('Observation note present true')

                if len(self.metadataNotesEdit.toPlainText()) == 0:

                    logger.debug('Metadata notes is zero length')

                    logger.debug('Deleting data at index %s' % str(observation_note_index))

                    logger.debug('Deleting data : %s' % str(self.data_store.MetadataCsv[observation_note_index]))

                    self.data_store.MetadataCsv.pop(observation_note_index)

                    logger.debug('Setting trip to False')

                    trip = False

                    self.response_message = 'SUCCESS', None

                else:

                    logger.debug('Metadata notes is not zero length')

                    data = ('Observation.Notes,' + self.metadataNotesEdit.toPlainText() +
                            ',String,Dimensionless,The Observation Notes')

                    logger.debug('Inserting metddata data at index : %s' % str(observation_note_index))

                    logger.debug('Inserting metadata data : %s' % str(data))

                    self.data_store.MetadataCsv[observation_note_index] = data

                    logger.debug('Setting trip to False')

                    trip = False

                    self.response_message = 'SUCCESS', None

            if trip:

                logger.debug('No observation note found in MetadataCsv')

                logger.debug("trip is True")

                if len(self.metadataNotesEdit.toPlainText()) != 0:

                    logger.debug('Metadata notes is not zero length')

                    data = ('Observation.Notes,' + self.metadataNotesEdit.toPlainText() +
                            ',String,Dimensionless,The Observation Notes')

                    logger.debug('Appending data to MetadataCsv : %s' % str(data))

                    self.data_store.MetadataCsv.append(data)

                    self.response_message = 'SUCCESS', None

                else:

                    logger.debug('Nothing to do.')

                    self.response_message = 'SUCCESS', None

        else:

            self.response_message = 'PREMATURE_TERMINATION', 'No data to save observation note to.'

        self.hide()

    def closeEvent(self, event):

        if self.observation_note is not None:

            if self.observation_note != self.metadataNotesEdit.toPlainText():

                result = QtGui.QMessageBox.warning(None,
                                                   None,
                                                   "<br>Metadata has changed!<br>Save changes?",
                                                   QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)

                if result == QtGui.QMessageBox.Yes:
                    self.save_called()
                else:
                    self.response_message = 'ABORT', None
                    self.hide()

        else:
            self.hide()