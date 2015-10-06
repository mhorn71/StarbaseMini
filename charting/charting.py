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

    def __init__(self, ui, datatranslator, metadata, instrument, config):
        '''

        :param ui: The UI to which we need for displaying the chart.
        :param datatranslator: The data translator for access to the imported data.
        :param metadata: The metadata we found when doing a csv import
        :param instrument: The instrument configuration which includes the base metadata as set by the instrument xml
        :param config: The application config parser.
        :return:
        '''
        ##initialise logger
        self.logger = logging.getLogger('graphics.chart')
        self.ui = ui
        self.datatranslator = datatranslator
        self.metadata = metadata
        self.instrument = instrument
        self.config = config
        self.attributes = None
        self.run_once = False
        self.count = 0  # Just a generic counter for testing purposes.
        self.channel_count = 0

        # Decimate attributes etc...
        self.timestamp = []
        self.decimate_array = []

        mpl.rcParams['font.monospace'] = 'Courier New'
        mpl.rcParams['savefig.directory'] = self.config.get('Application', 'instrument_data_path')
        mpl.rcParams['savefig.bbox'] = 'tight'
        mpl.rcParams['axes.linewidth'] = 0.5
        mpl.rcParams['axes.facecolor'] = "#FDFDF0"
        mpl.rcParams['figure.max_open_warning'] = 2
        mpl.rcParams['legend.framealpha'] = 0.5
        mpl.rcParams['legend.fancybox'] = True
        mpl.rcParams['lines.markersize'] = 5

        self.fig = Figure()
        self.ax1f1 = self.fig.add_subplot(111)
        self.canvas = FigureCanvas(self.fig)

        if mpl.get_backend().lower() in ['agg', 'macosx']:
            self.fig.set_tight_layout(True)
        else:
            self.fig.tight_layout()

        self.logger.info('Initialised charting.')

    def clear(self):
        self.ax1f1.clear()
        del self.timestamp[:]
        del self.decimate_array[:]

    def add_metadata(self, data_type):
        '''
        adds the title, axis labels, channel names etc .....
        :param type: data or csv
        :return: True or False.
        '''
        data_type = data_type.lower()
        if data_type == 'data':
            self.attributes = self.instrument
        elif data_type == 'csv':
            self.attributes = self.metadata
        else:
            self.logger.critical('Unknown data type : %s' % data_type)
            return False

        self.set_scale()

        try:
            if self.attributes.XaxisLabel is not None:
                self.ax1f1.set_xlabel(self.attributes.XaxisLabel)
            else:
                self.ax1f1.set_xlabel('NODATA')

            if self.attributes.YaxisLabel is not None:
                self.ax1f1.set_ylabel(self.attributes.YaxisLabel)
            else:
                self.ax1f1.set_ylabel('NODATA')

            if self.attributes.instrument_identifier is not None:
                self.ax1f1.set_title(self.attributes.instrument_identifier)
            else:
                self.ax1f1.set_title('NODATA')

            self.ax1f1.grid(True)
        except AttributeError as msg:
            self.logger.critical(str(msg))
            return False
        else:
            return True

    def set_scale(self):
        try:
            if self.attributes.YaxisRange is not None:
                axis_range = self.attributes.YaxisRange.split(',')
                yrange_start = int(axis_range[0])
                yrange_stop = int(axis_range[1])
                self.ax1f1.set_ylim(yrange_start, yrange_stop)
        except AttributeError:
            self.logger.warning('No axes scale found defaulting to autoscale.')

    def add_mpl(self):

        # Something to beware of I'm not sure what will happen if and Index X axis is used.
        hfmt = mpl.dates.DateFormatter('%H:%M:%S\n%Y-%m-%d')
        self.ax1f1.xaxis.set_major_formatter(hfmt)
        self.ax1f1.fmt_xdata = mpl.dates.DateFormatter('%Y-%m-%d %H:%M:%S')

        if self.run_once is False:
            # set the mplwindow widget background to a gray otherwise splash page disfigures the toolbar look.
            self.ui.mplwindow.setStyleSheet('QWidget{ background-color: #EDEDED; }')

            self.ui.mplvl.addWidget(self.canvas)

            toolbar = NavigationToolbar(self.canvas,
                                        self.ui.mplwindow, coordinates=True)
            self.ui.mplvl.addWidget(toolbar)
            self.run_once = True
        else:
            self.canvas.draw()

    def add_data(self, number_of_channels):

        try:
            number_of_channels = int(number_of_channels)
        except AttributeError as msg:
            self.logger.critical('Channel count not found : %s' % str(msg))
            return 'PREMATURE_TERMINATION', str(msg)

        self.channel_count = number_of_channels

        try:
            for i in range(number_of_channels):
                self.ax1f1.plot(self.datatranslator.datetime, self.datatranslator.data_array[i],
                                self.attributes.channel_colours[i], label=self.attributes.channel_names[i])
        except IndexError as msg:
            self.logger.critical('Channel count doesn\'t match data : %s' % str(msg))
            return 'PREMATURE_TERMINATION', str(msg)

        self.add_mpl()

        return 'SUCCESS', None

    def decimate_data(self, number_of_channels):

        try:
            number_of_channels = int(number_of_channels)
        except AttributeError as msg:
            self.logger.critical('Channel count not found : %s' % str(msg))
            return 'PREMATURE_TERMINATION', str(msg)

        self.channel_count = number_of_channels

        self.logger.debug('Datetime Original Length : %s' % str(len(self.datatranslator.datetime)))

        args = [iter(self.datatranslator.datetime)] * 4
        x = zip_longest(fillvalue=None, *args)

        for i in x:
            self.timestamp.append(i[0])

        self.logger.debug('Datetime Decimate Length : %s' % str(len(self.timestamp)))

        try:
            for i in range(number_of_channels):
                tmp_list = []

                args = [iter(self.datatranslator.data_array[i])] * 4
                x = zip_longest(fillvalue=None, *args)

                for n in x:
                    tmp_list.append(n[0])

                self.decimate_array.append(tmp_list)

                self.logger.debug('Decimate Array Length : ' + str(len(self.decimate_array)))
                self.logger.debug('Channel : ' + str(i) + ' - ' + 'Original Length : ' + str(len(self.datatranslator.data_array[i])))
                self.logger.debug('Channel : ' + str(i) + ' - ' + 'Decimate Length : ' + str(len(tmp_list)))

        except IndexError as msg:
            self.logger.critical('Channel count doesn\'t match data : %s' % str(msg))
            return 'PREMATURE_TERMINATION', str(msg)

        try:
            for i in range(number_of_channels):
                self.ax1f1.plot(self.timestamp, self.decimate_array[i],
                                self.attributes.channel_colours[i], label=self.attributes.channel_names[i])
        except IndexError as msg:
            self.logger.critical('Channel count doesn\'t match data : %s' % str(msg))
            return 'PREMATURE_TERMINATION', str(msg)

        hfmt = mpl.dates.DateFormatter('%H:%M:%S\n%Y-%m-%d')
        self.ax1f1.xaxis.set_major_formatter(hfmt)
        self.ax1f1.fmt_xdata = mpl.dates.DateFormatter('%Y-%m-%d %H:%M:%S')

        self.canvas.draw()

    def channel_control(self, channel, state):

        if state is False:
            self.ax1f1.lines[channel].set_visible(False)
        else:
            self.ax1f1.lines[channel].set_visible(True)

        self.canvas.draw()

    def channel_autoscale(self, state):
        if state is False:
            self.ax1f1.autoscale(False)
            self.set_scale()
        else:
            self.ax1f1.autoscale(True)

        self.canvas.draw()

    def chart_legend(self, state):

        fontP = FontProperties()
        fontP.set_size(self.config.get('Legend', 'font'))

        if state is True:
            self.ax1f1.legend(prop=fontP, loc=self.config.get('Legend', 'location'),
                              ncol=int(self.config.get('Legend', 'columns'))).set_visible(True)

            # # # set the linewidth of each legend object
            for legend_handle in self.ax1f1.legend(prop=fontP, loc=self.config.get('Legend', 'location'),
                                                   ncol=int(self.config.get('Legend', 'columns'))).legendHandles:
                legend_handle.set_linewidth(10.0)

        elif state is False:
            self.ax1f1.legend().set_visible(False)

        self.canvas.draw()

