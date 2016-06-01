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

import constants

class MetadataViewerEditor(QtGui.QDialog, Ui_MetadataDialog):
    def __init__(self, metadata, data_store):
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

        self.metadata = metadata

        self.observation_note = None

        self.response_message = 'ABORT', None

        self.metadataEdit.setReadOnly(True)
        self.metadataNotesEdit.setFocus()

        self.buttonBox.button(QtGui.QDialogButtonBox.Save).clicked.connect(self.save_called)
        self.buttonBox.button(QtGui.QDialogButtonBox.Close).clicked.connect(lambda: self.close())

        self.metadataNotesEdit.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp(constants.observer_notes)))
        self.metadataNotesEdit.textChanged.connect(self.parameter_check_state)
        self.metadataNotesEdit.textChanged.emit(self.metadataNotesEdit.text())

        # Observer.Notes,The Observer Notes,String,Dimensionless,The Observer Notes

    def clear(self):

        logger = logging.getLogger('metadata.MetadataViewerEditor.clear')
        
        logger.debug('Reset defaults.')

        self.observation_note = None

        self.response_message = 'ABORT', None

        # Parameter check state changes the colour of the line edit boxes depending on contents.

    def parameter_check_state(self, *args, **kwargs):

        # This bit is a bit of bodge as parameter check state will trigger when loading and raise
        # AttributeError so we just ignore it, not ideal!

        try:
            sender = self.sender()
            validator = sender.validator()
            state = validator.validate(sender.text(), 0)[0]
        except AttributeError:
            pass

        if state == QtGui.QValidator.Acceptable and len(sender.text()) == 0:

            # white
            sender.setStyleSheet('QLineEdit { background-color: #FFFFFF }')

        elif state == QtGui.QValidator.Acceptable:

            # green
            sender.setStyleSheet('QLineEdit { background-color: #c4df9b }')

        elif state == QtGui.QValidator.Intermediate and len(sender.text()) == 0:

            # red
            sender.setStyleSheet('QLineEdit { background-color: #f6989d }')

        elif state == QtGui.QValidator.Intermediate:

            # yellow
            sender.setStyleSheet('QLineEdit { background-color: #fff79a }')

        else:
            sender.setStyleSheet('QLineEdit { background-color: #f6989d')


    def update_ui(self):

        self.metadataEdit.clear()
        self.metadataNotesEdit.clear()

        data = ''

        self.buttonBox.button(QtGui.QDialogButtonBox.Save).setEnabled(False)
        self.metadataNotesEdit.setEnabled(False)

        metadata = self.metadata.metadata_creator(self.data_store.DataSource)

        if metadata is None:

            self.metadataEdit.setText('No metadata to display.')

        else:

            self.buttonBox.button(QtGui.QDialogButtonBox.Save).setEnabled(True)
            self.metadataNotesEdit.setEnabled(True)

            for i in metadata:

                if i[0].startswith('Observation.Notes'):

                    self.metadataNotesEdit.setText(str(i[1]))

                else:

                    data += i[0] + ' :: ' + i[1] + '\n'

            self.metadataEdit.setText(data)

    def save_called(self):

        logger = logging.getLogger('metadata.MetadataViewerEditor.save_called.')

        if len(self.metadataNotesEdit.text()) != 0:

            if self.metadata.ObservationNotes != self.metadataNotesEdit.text():

                self.data_store.ObservationNotesChanged = True

            self.metadata.ObservationNotes = self.metadataNotesEdit.text()

            logger.debug('Setting observation notes set to : %s' % self.metadataNotesEdit.text())

            self.response_message = 'SUCCESS', 'Metadata saved.'

        else:

            self.response_message = 'PREMATURE_TERMINATION', 'No data to save observation note to.'

        self.hide()

    def closeEvent(self, event):

        if self.metadata.ObservationNotes is None:

            obs_notes = ''

        else:

            obs_notes = self.metadata.ObservationNotes

        if obs_notes != self.metadataNotesEdit.text():

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