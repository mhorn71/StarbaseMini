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
import time

from PyQt4 import QtGui, QtCore

from itertools import zip_longest

import matplotlib as mpl

if sys.platform.startswith('linux'):
    mpl.use("Qt4Agg")

from matplotlib.figure import Figure

from matplotlib.backends.backend_qt4agg import (
    FigureCanvasQTAgg as FigureCanvas, NavigationToolbar2QT)

from matplotlib.font_manager import FontProperties

# http://stackoverflow.com/questions/12695678/how-to-modify-the-navigation-toolbar-easily-in-a-matplotlib-figure-window
# Thanks to torfbolt and MadeOfAir.


class NavigationToolbar(NavigationToolbar2QT):
    # only display the buttons we need
    toolitems = [t for t in NavigationToolbar2QT.toolitems if
                 t[0] in ('Home', 'Back', 'Forward', 'Pan', 'Zoom', 'Save')]

    def __init__(self, *args, **kwargs):
        super(NavigationToolbar, self).__init__(*args, **kwargs)
        self.layout().takeAt(6)


class Chart:

    # I got the how to do this from the following website and I thank the author for the information.
    # http://blog.rcnelson.com/building-a-matplotlib-gui-with-qt-designer-part-1/

    ''' Developer Note: Add generic container widget called mplwindow, drop any widget within mplwindow and layout
    vertical then delete the temporary widget. Set the vertical layout name to mplvl
    '''

    # TODO almost a complete rewrite we need to take into account Raw and Processed Data plus Controller or CSV Source.

    def __init__(self, ui):
        '''

        :param ui: The UI to which we need for displaying the chart.
        :param datatranslator: The data translator for access to the imported data.
        :param metadata: The metadata we found when doing a csv import
        :param instrument: The instrument configuration which includes the base metadata as set by the instrument xml
        :param config: The application config parser.
        :return:
        '''
        ##initialise logger

        logger = logging.getLogger('graphics.Chart.init')
        self.ui = ui
        self.data_store = None
        self.data_source = None
        self.instrument = None
        self.metadata = None
        self.application_configuration = None
        self.run_once = False

        mpl.rcParams['font.monospace'] = 'Courier New'
        mpl.rcParams['savefig.bbox'] = 'tight'
        mpl.rcParams['axes.linewidth'] = 0.5
        mpl.rcParams['axes.facecolor'] = "#FDFDF0"
        mpl.rcParams['figure.max_open_warning'] = 2
        mpl.rcParams['legend.framealpha'] = 0.5
        mpl.rcParams['legend.fancybox'] = True
        mpl.rcParams['lines.markersize'] = 5
        mpl.rcParams['figure.autolayout'] = True
        mpl.rcParams['ytick.labelsize'] = 'small'
        mpl.rcParams['xtick.labelsize'] = 'small'

        self.fig = Figure()
        self.ax1f1 = self.fig.add_subplot(111)
        self.canvas = FigureCanvas(self.fig)

        if mpl.get_backend().lower() in ['agg', 'macosx']:
            self.fig.set_tight_layout(True)
        else:
            self.fig.tight_layout()

        logger.info('Initialised charting.')

    def chart_instrument_setup(self, datastore, instrument, metadata, application_configuration, datasource):
        self.data_store = datastore
        self.data_source = datasource
        self.instrument = instrument
        self.metadata = metadata
        self.application_configuration = application_configuration

        mpl.rcParams['savefig.directory'] = self.application_configuration.get('Application', 'instrument_data_path')

    def add_data(self, type):

        logger = logging.getLogger('graphics.Chart.add_data')

        # Clear the current chart if present.

        if self.ax1f1 is not None:

            self.ax1f1.clear()

        # print('Data source : %s' % str(self.data_store.DataSource))

        # Set labels and ranges from metadata depending on data source.

        if self.data_store.DataSource == 'Controller':

            title = self.instrument.instrument_identifier
            channel_names = self.instrument.channel_names
            channel_colours = self.instrument.channel_colours
            channel_units = self.instrument.channel_units
            y_axis_label = self.instrument.YaxisLabel
            x_axis_label = self.instrument.XaxisLabel
            y_axis_range = self.instrument.YaxisRange

        elif self.data_store.DataSource == 'CSV':

            title = self.metadata.instrument_identifier
            channel_names = self.metadata.channel_names
            channel_colours = self.metadata.channel_colours
            channel_units = self.metadata.channel_units
            y_axis_label = self.metadata.YaxisLabel
            x_axis_label = self.metadata.XaxisLabel
            y_axis_range = None

        else:

            return 'PREMATURE_TERINATION', 'Unknown data source : %s' % str(self.data_source)

        # set labels and title.

        self.ax1f1.set_title(title)
        self.ax1f1.set_xlabel(x_axis_label)
        self.ax1f1.set_ylabel(y_axis_label)
        self.ax1f1.grid(True)

        # set y axis range if set.

        if y_axis_range is not None:

            axis_range = y_axis_range.split(',')

            yrange_start = int(axis_range[0])

            yrange_stop = int(axis_range[1])

            self.ax1f1.set_ylim(yrange_start, yrange_stop)

        try:

            number_of_channels = int(self.data_store.channel_count)
            logger.debug('add_data to chart channel count : ' + str(number_of_channels))

        except AttributeError as msg:

            logger.critical('Channel count not found : %s' % str(msg))

            return 'PREMATURE_TERMINATION', 'Channel count : %s' % str(msg)

        #  Set what type the data is raw, rawcsv, processed.

        if type == 'raw':

            print('Length of data : %s' % str(len(self.data_store.RawData)))

            data = self.data_store.RawData

        elif type == 'rawCsv':

            print('Length of data : %s' % str(len(self.data_store.RawDataCsv)))

            data = self.data_store.RawDataCsv

        elif type == 'processed':

            print('Length of data : %s' % str(len(self.data_store.ProcessedData)))

            data = self.data_store.ProcessedData

        epoch = [n[0] for n in data]

        channels = []

        for i in range(number_of_channels):

            channels.append([n[i + 1] for n in data])

        for i in range(0, number_of_channels):

            self.ax1f1.plot(epoch, channels[i], channel_colours[i], label=channel_names[i])

        self.add_mpl()

        return 'SUCCESS', None

    def add_mpl(self):

        # Something to beware of I'm not sure what will happen if and Index X axis is used.

        hfmt = mpl.dates.DateFormatter('%H:%M:%S\n%Y-%m-%d')

        self.ax1f1.xaxis.set_major_formatter(hfmt)

        self.ax1f1.fmt_xdata = mpl.dates.DateFormatter('%Y-%m-%d %H:%M:%S')

        if self.run_once is False:

            # set the mplwindow widget background to a gray otherwise splash page disfigures the toolbar look.

            self.ui.mplwindow.setStyleSheet('QWidget{ background-color: #EDEDED; }')

            self.ui.mplvl.addWidget(self.canvas)

            toolbar = NavigationToolbar(self.canvas, self.ui.mplwindow, coordinates=True)

            self.ui.mplvl.addWidget(toolbar)

            self.run_once = True

        else:

            self.canvas.draw()