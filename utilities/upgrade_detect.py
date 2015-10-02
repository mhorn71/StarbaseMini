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
from functools import partial
import logging
import xml.etree.ElementTree as eTree
import re
from PyQt4 import QtGui

xml_url = 'http://ukraa.com/ftpupload/starbasemini_version.xml'

def detect_upgrade(current_version):
    try:
        xml_str  = urllib.request.urlopen(xml_url)
    except (urllib.error.HTTPError, urllib.error.URLError) as msg:
        print('XML Not found')
    else:
        xmldom = eTree.parse(xml_str)  # Open and parse xml document.
        revision = xmldom.findtext('revision')

        if revision != current_version:

            message = 'There is a new version of StarbaseMini available\ndo you wish to download version ' + revision
            result = QtGui.QMessageBox.question(None,
                                                "StarbaseMini Upgrade",
                                                message,
                                                QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)

            if result == QtGui.QMessageBox.Yes:
                if sys.platform.startswith('darwin'):
                    minifile = xmldom.findtext('mac')
                    md5hash = xmldom.findtext('machash')
                    status = downloader(minifile, md5hash)
                elif sys.platform.startswith('win32'):
                    minifile = xmldom.findtext('windows')
                    md5hash = xmldom.findtext('winhash')
                    status = downloader(minifile, md5hash)
                elif sys.platform.startswith('linux'):
                    if os.uname()[4].startswith("arm"):
                        minifile = xmldom.findtext('arm')
                        md5hash = xmldom.findtext('armhash')
                        status = downloader(minifile, md5hash)
                    else:
                        minifile = xmldom.findtext('linux')
                        md5hash = xmldom.findtext('linhash')
                        status = downloader(minifile, md5hash)

def downloader(minifile, md5hash):
    home = os.path.expanduser("~")

    if not os.path.isdir(home):
        raise FileNotFoundError("Fatal error unable to detect user home!!\nContact developer for help.")
    else:
        home += os.path.sep + '.starbasemini' + os.path.sep

        in_file = 'http://ukraa.com/ftpupload/' + minifile
        out_file = home + minifile

        try:
            urllib.request.urlretrieve (in_file, out_file)
        except urllib.error.URLError:
            print('Download Failed')
        else:
            if md5sum(out_file) == md5hash:
                print('We matched checked sums')
            else:
                print(md5sum(out_file))
                if os.path.isfile(out_file):
                    os.unlink(out_file)
                print('We didn\'t match check sums')

def md5sum(filename):
    # This code was copied verbatim from
    # http://stackoverflow.com/questions/7829499/using-hashlib-to-compute-md5-digest-of-a-file-in-python-3
    with open(filename, mode='rb') as f:
        d = hashlib.md5()
        for buf in iter(partial(f.read, 1024), b''):
            d.update(buf)
    return d.hexdigest()
