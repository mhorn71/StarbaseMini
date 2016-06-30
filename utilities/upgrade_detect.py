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
import urllib
import hashlib
import socket
from functools import partial
import logging
import xml.etree.ElementTree as eTree

from PyQt5 import QtWidgets, QtCore


##  Base url is now starbasemini_version_2.xml


class Upgrader:
    def __init__(self, parent=None):
        self.baseurl = 'http://ukraa.com/ftpupload/'

        self.xml_url = self.baseurl + 'starbasemini_version_2.xml'

        self.logger = logging.getLogger('utilities.upgrade_detect')

    def Is64Windows(self):
        return 'PROGRAMFILES(X86)' in os.environ

    def GetProgramFiles32(self):
        if self.Is64Windows():
            return True
        else:
            return False

    def detect_upgrade(self, current_version):

        socket.setdefaulttimeout(2)

        try:
            xml_str = urllib.request.urlopen(self.xml_url, timeout=2)
        except (urllib.error.HTTPError, urllib.error.URLError, ConnectionResetError, socket.timeout) as msg:
            self.logger.warning('Unable to download upgrade information from : ' + self.xml_url)
            return 'ABORT', 'Unable to download upgrade information from : ' + self.xml_url
        else:
            xmldom = eTree.parse(xml_str)  # Open and parse xml document.
            revision = xmldom.findtext('revision')

            if revision != current_version:

                message = 'There is a new version of StarbaseMini available do you wish to download : \n\nVersion ' + revision + \
                          '\n\nPlease wait for download to complete.'
                result = QtWidgets.QMessageBox.question(None,
                                                    "StarbaseMini Upgrade",
                                                    message,
                                                    QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)

                if result == QtWidgets.QMessageBox.Yes:
                    if sys.platform.startswith('darwin'):
                        minifile = xmldom.findtext('mac')
                        md5hash = xmldom.findtext('machash')
                        status = self.downloader(minifile, md5hash)
                    elif sys.platform.startswith('win32'):
                        if self.GetProgramFiles32():
                            minifile = xmldom.findtext('windows64')
                            md5hash = xmldom.findtext('win64hash')
                            status = self.downloader(minifile, md5hash)
                        else:
                            minifile = xmldom.findtext('windows32')
                            md5hash = xmldom.findtext('win32hash')
                            status = self.downloader(minifile, md5hash)
                    elif sys.platform.startswith('linux'):
                        if os.uname()[4].startswith('arm'):
                            minifile = xmldom.findtext('arm')
                            md5hash = xmldom.findtext('armhash')
                            status = self.downloader(minifile, md5hash)
                        else:
                            minifile = xmldom.findtext('linux')
                            md5hash = xmldom.findtext('linhash')
                            status = self.downloader(minifile, md5hash)

                    return status
                else:
                    return 'ABORT', 'Upgrade download cancelled.'
            else:
                return None

    def downloader(self, minifile, md5hash):

        socket.setdefaulttimeout(2)

        in_file = self.baseurl + minifile

        fname = QtWidgets.QFileDialog.getExistingDirectory(None, 'Save Download To', os.path.expanduser("~"),
                                                       QtWidgets.QFileDialog.ShowDirsOnly)

        if len(fname) == 0:
            return 'ABORT', 'Upgrade downloaded cancelled.'

        out_file = fname + os.path.sep + minifile

        if os.path.isfile(out_file):
            os.unlink(out_file)

        try:
            urllib.request.urlretrieve(in_file, out_file)
        except urllib.error.URLError as msg:

            self.logger.warning('Unable to download upgrade : %s' % (str(in_file), str(msg)))

            return 'ABORT', 'Unable to retrieve upgrade.'
        else:
            if self.md5sum(out_file) == md5hash:
                QtWidgets.QMessageBox.information(None, 'Upgrade Instructions', 'To upgrade close application and uninstall, '
                                                                            'then reinstall with the downloaded upgrade '
                                                                            'file.  Your settings will be preserved.')

                return 'SUCCESS', 'Upgrade file downloaded to - ' + out_file
            else:
                self.logger.debug("Checksum : %s for file : %s" % str(self.md5sum(out_file)), out_file)
                if os.path.isfile(out_file):
                    os.unlink(out_file)
                return 'ABORT', 'Upgrade file checksum failed check.'

    def md5sum(self, filename):
        # This code was copied verbatim from
        # http://stackoverflow.com/questions/7829499/using-hashlib-to-compute-md5-digest-of-a-file-in-python-3
        with open(filename, mode='rb') as f:
            d = hashlib.md5()
            for buf in iter(partial(f.read, 1024), b''):
                d.update(buf)
        return d.hexdigest()