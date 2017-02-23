__author__ = 'mark'
# StarbaseMini Staribus/Starinet Client for the British Astronomical Association Staribus Protocol
# Copyright (C) 2017  Mark Horn
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

import datetime
import logging

from ui import Ui_RunningAverageDialog

from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSlot

import numpy as np


class NonlinearStaticRemover(QtWidgets.QDialog, Ui_RunningAverageDialog):
    def __init__(self, datastore):
        QtWidgets.QDialog.__init__(self)
        self.setupUi(self)
        self.datastore = datastore

        self.setWindowTitle('Non-Linear Static Remover')

        self.apply = self.buttonBox.button(QtWidgets.QDialogButtonBox.Apply)
        self.apply.clicked.connect(self.on_accepted_clicked)

        self.spinBox.setRange(2, 10)

        self.spinBox.setValue(4)

        self.response_message = 'ABORT', None

    def on_accepted_clicked(self):

        logger = logging.getLogger('filters.RunningAverage.on_accepted_clicked')

        # shape format number of samples in row, number of elements in array

        if len(self.datastore.RawData) != 0:

            logger.debug(self.datastore.RawData.shape)

            self.average()

        else:

            self.response_message = 'PREMATURE_TERMINATION', 'NO_DATA.'
            self.hide()

    def average(self):

        logger = logging.getLogger('filters.RunningAverage.average')

        # 'Average over N sequential samples'

        average_over_n_samples = int(self.spinBox.text())

        logger.debug('average_over_n_samples : %s' % str(average_over_n_samples))

        # Get shape of numpy array.

        number_of_rows, number_of_cols = self.datastore.RawData.shape

        logger.debug('number_of_rows : %s' % str(number_of_rows))
        logger.debug('number_of_cols : %s' % str(number_of_cols))

        # Convert numpy array to list

        datalist = self.datastore.RawData.tolist()

        # Create new data lists

        preprocessed_data_columns = [[] for i in range(number_of_cols)]
        processed_data_columns = []
        processed_data_list = []

        # Create lists of each column of data for processing.
        for row in range(number_of_rows):

            for col in range(number_of_cols):

                # check to see if field is a datetime object and if not make sure col data is a float.

                if type(datalist[row][col]) is datetime.datetime:

                    preprocessed_data_columns[col].append(datalist[row][col])

                else:

                    preprocessed_data_columns[col].append(float(datalist[row][col]))

        # Average each column and store result in processed_data_column
        for x in range(number_of_cols):

            if type(preprocessed_data_columns[x][0]) is datetime.datetime:

                processed_data_columns.append([preprocessed_data_columns[x][i] for i in range(0, len(preprocessed_data_columns[x]), 1)
                                               if i + average_over_n_samples <= len(preprocessed_data_columns[x])])

            else:

                processed_data_columns.append([np.amin(preprocessed_data_columns[x][i:i + average_over_n_samples]) for i in range(0, len(preprocessed_data_columns[x]), 1)
                                               if i + average_over_n_samples <= len(preprocessed_data_columns[x])])


        # check each individual list in processed_data_columns is not zero and are the same length

        if not all(len(i) == len(processed_data_columns[0]) for i in processed_data_columns) or \
                        len(processed_data_columns[0]) == 0:

            self.response_message = 'PREMATURE_TERMINATION', 'NO_DATA.'
            self.hide()

        else:

            length_of_processed_data_columns = len(processed_data_columns[0])

            # Now recreate data lists from individual column lists.

            for i in range(length_of_processed_data_columns):

                temp_list = []

                for n in range(number_of_cols):
                    temp_list.append(processed_data_columns[n][i])

                processed_data_list.append(temp_list)

            self.datastore.ProcessedDataSaved = False

            self.datastore.ProcessedData = np.array(processed_data_list)

            self.response_message = 'SUCCESS', None

            self.hide()


    @pyqtSlot()
    def on_rejected_clicked(self, event):

        self.response_message = 'ABORT', None