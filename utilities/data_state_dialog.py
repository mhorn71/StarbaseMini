__author__ = 'mark'
# StarbaseMini Staribus/Starinet Client for the British Astronomical Association Staribus Protocol
# Copyright (C) 2016  Mark Horn
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

from PyQt4 import QtGui


def data_state_check(data_store, type):

    '''
    requires type which can be, 'exit, 'standard', 'instrument'
    :return: True is it's safe to destroy any unsaved data, else False.
    '''

    if type == 'exit':

        submessage = '\n\nAre you sure you want to exit?'

    elif type == 'instrument':

        submessage = ''

    else:

        submessage = '\n\nAre you sure you want to continue this will overwrite the unsaved data?'

    if data_store.data_state()[0] is False:

        message = ('WARNING:  ' + data_store.data_state()[1] + submessage)
        header = ''

        result = QtGui.QMessageBox.question(None,
                                            header,
                                            message,
                                            QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)

        if result == QtGui.QMessageBox.Yes:

            return True

        else:

            return False

    else:

        return True

