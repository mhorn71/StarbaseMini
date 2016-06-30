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
import sys

from PyQt5 import QtWidgets

from ui import Ui_Dialog

class ReleaseNote(QtWidgets.QDialog, Ui_Dialog):

    def __init__(self):
        QtWidgets.QDialog.__init__(self)
        self.setupUi(self)

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

        if os.path.isfile("ReleaseNotes"):
            file = open('ReleaseNotes', 'r')
            text = file.read()
            file.close()
        else:
            text = "No release notes found!!"

        self.releasenotesText.setText(text)