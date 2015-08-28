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


import matplotlib as mpl

from matplotlib.figure import Figure

from matplotlib.backends.backend_qt4agg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar)

import logging


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

        mpl.rcParams['figure.autolayout'] = True
        mpl.rcParams['savefig.directory'] = self.config.get('Application', 'instrument_data_path')
        mpl.rcParams['axes.linewidth'] = 0.5
        mpl.rcParams['axes.facecolor'] = "#FDFDF0"
        mpl.rcParams['figure.max_open_warning'] = 2

        self.fig = Figure()
        self.logger.info('Charting initialised.')
        self.ax1f1 = self.fig.add_subplot(111)
        self.canvas = FigureCanvas(self.fig)

        # Standard Chart Colours are from
        # http://tableaufriction.blogspot.ro/2012/11/finally-you-can-use-tableau-data-colors.html

        self.default1_label = 'Celsius'
        self.default2_label = 'Channel 0'
        self.default3_label = 'Channel 1'
        self.default4_label = 'Channel 2'
        self.default5_label = 'Channel 3'
        self.default6_label = 'Channel 4'
        self.default7_label = 'channel 5'
        self.default8_label = 'channel 6'
        self.default9_label = 'channel 7'

        self.default1_colour = '#D62728'
        self.default2_colour = '#1F77B4'
        self.default3_colour = '#FF7F0E'
        self.default4_colour = '#2CA02C'
        self.default5_colour = '#9467BD'
        self.default6_colour = '#8C564B'
        self.default7_colour = '#E377C2'
        self.default8_colour = '#BCBD22'
        self.default9_colour = '#17BECF'

    def clear(self):
        self.ax1f1.clear()

    def add_metadata(self, type):
        '''
        adds the title, axis labels, channel names etc .....
        :param type: data or csv
        :return: True or False.
        '''
        type = type.lower()
        if type == 'data':
            self.attributes = self.instrument
        elif type == 'csv':
            self.attributes = self.metadata
        else:
            # todo logger bits.
            print('Type unknown')
            return False

        try:
            if self.attributes.YaxisRange is not None:
                axis_range = self.attributes.YaxisRange.split(',')
                yrange_start = int(axis_range[0])
                yrange_stop = int(axis_range[1])
                self.ax1f1.set_ylim(yrange_start, yrange_stop)
        except AttributeError:
            pass

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
            # todo add logger bits
            return False
        else:
            return True

    def add_mpl(self):

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

    def add_data(self):

        try:
            number_of_channels = int(self.attributes.instrument_number_of_channels)
        except AttributeError as msg:
            # todo add logger bits
            return 'PREMATURE_TERMINATION', str(msg)

        try:
            for i in range(number_of_channels):
                self.ax1f1.plot(self.datatranslator.datetime, self.datatranslator.data_array[i],
                                self.attributes.channel_colours[i], label=self.attributes.channel_names[i])
        except IndexError as msg:
            # todo add logger bits
            return 'PREMATURE_TERMINATION', str(msg)

        self.add_mpl()

        return 'SUCCESS', None

    def channel_control(self, channel, state):

        if state is False:
            self.ax1f1.lines[channel].set_visible(False)
        else:
            self.ax1f1.lines[channel].set_visible(True)

        self.add_mpl()

