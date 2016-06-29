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
#import datetime

#import numpy as np
from PyQt4 import QtGui, QtCore

from ui import Ui_DataViewerDialog


class RawDataViewer(QtGui.QDialog, Ui_DataViewerDialog):
    def __init__(self, data_store, instrument):
        QtGui.QDialog.__init__(self)
        self.setupUi(self)
        self.data_store = data_store
        self.metadata = None
        self.instrument = instrument

        # Style sheets

        if sys.platform.startswith('darwin'):

            self.autowidthfixer = 42

            with open('css/macStyle.css', 'r') as style:

                self.setStyleSheet(style.read())

        elif sys.platform.startswith('win32'):

            self.autowidthfixer = 25

            with open('css/winStyle.css', 'r') as style:

                self.setStyleSheet(style.read())

        elif sys.platform.startswith('linux'):

            self.autowidthfixer = 25

            with open('css/nixStyle.css', 'r') as style:

                self.setStyleSheet(style.read())

    # Take a look at this stackoverflow post at sometime regards copying a row and headers.
    # http://stackoverflow.com/questions/24971305/copy-pyqt-table-selection-including-column-and-row-headers

    def load(self, type, metadata):

        self.metadata = metadata

        if type == 'processed':

            self.setWindowTitle('Processed Data Viewer')

            data = self.data_store.ProcessedData

        else:

            self.setWindowTitle('Raw Data Viewer')

            data = self.data_store.RawData


        # QTableWidget Header list

        headers = ['Date','Time']

        # First get the current channel labels and channel count from metadata based on source.

        if self.data_store.DataSource == 'Controller':
            channel_labels = self.instrument.channel_names
            channel_count = int(self.instrument.instrument_number_of_channels)
        else:
            channel_labels = self.metadata.channel_names
            channel_count = int(self.metadata.instrument_number_of_channels)

        # Clear the current contents.
        self.DataViewTableWidget.clear()

        # Set the row count based on data.
        self.DataViewTableWidget.setRowCount(len(data))

        # Set the column count based on channel count + 1
        self.DataViewTableWidget.setColumnCount(int(channel_count + 2))

        # Insert into the headers list the channel labels.
        for i in range(channel_count):

            headers.insert((channel_count + 2), channel_labels[i])

        # Set the header labels.

        self.DataViewTableWidget.setHorizontalHeaderLabels(headers)

        insert_data = []

        counter = 0

        # I've left the below commented section for reference, it was an attempt to speed up the loading of the data
        # viewer however it came out as being ~ 20s slower. :-(

        # for (x, y), value in np.ndenumerate(data):
        #     if isinstance(value, datetime.datetime):
        #         date, time = value.strftime('%Y-%m-%d,%H:%M:%S').split(',')
        #
        #         self.DataViewTableWidget.setItem(x, y, QtGui.QTableWidgetItem(date))
        #
        #         y += 1
        #
        #         self.DataViewTableWidget.setItem(x, y, QtGui.QTableWidgetItem(time))
        #
        #     y += 1
        #
        #     self.DataViewTableWidget.setItem(x, y, QtGui.QTableWidgetItem(str(value)))


        for x in data.tolist():

            insert_data.clear()

            date, time = x[0].strftime('%Y-%m-%d,%H:%M:%S').split(',')

            insert_data.insert(0, date)
            insert_data.insert(1, time)

            for y in x[1:]:

                insert_data.insert((x.index(y) + 2), y)

            for n in range(len(insert_data)):

                self.DataViewTableWidget.setItem(counter, n, QtGui.QTableWidgetItem(str(insert_data[n])))

            counter += 1

        self.resize(self.sizeHint())

    # This piece of code is courtesy of Stephen Terry
    # http://stackoverflow.com/questions/7189305/set-optimal-size-of-a-dialog-window-containing-a-tablewidget

    def sizeHint(self):
        width = 0
        for i in range(self.DataViewTableWidget.columnCount()):
            width += self.DataViewTableWidget.columnWidth(i)

        width += self.DataViewTableWidget.verticalHeader().sizeHint().width()

        width += self.DataViewTableWidget.verticalScrollBar().sizeHint().width()
        width += self.DataViewTableWidget.frameWidth() * self.autowidthfixer  # this was originally 2 had to make 42 to work on mac?

        return QtCore.QSize(width, self.height())