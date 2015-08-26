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
import matplotlib.dates as dates

from matplotlib.backends.backend_qt4agg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar)

import logging
import sys


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
        self.instrument_name = self.instrument.instrument_identifier
        self.number_of_channels = self.instrument.instrument_number_of_channels
        self.xlabel = self.instrument.XaxisLabel
        self.ylabel = self.instrument.YaxisLabel

        range = self.instrument.YaxisRange.split(',')
        self.yRangeStart = range[0]
        self.yRangeStop = range[1]
        self.run_once = False
        self.count = 0  # Just a generic counter for testing purposes.

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

        mpl.rcParams['figure.autolayout'] = True
        mpl.rcParams['savefig.directory'] = self.config.get('Application', 'instrument_data_path')
        mpl.rcParams['axes.linewidth'] = 0.5
        mpl.rcParams['axes.facecolor'] = "#FDFDF0"
        mpl.rcParams['figure.max_open_warning'] = 2

        self.fig = Figure()
        self.logger.info('Charting initialised.')
        self.ax1f1 = self.fig.add_subplot(111)
        self.canvas = FigureCanvas(self.fig)

        self.line1 = None
        self.line2 = None
        self.line3 = None
        self.line4 = None
        self.line5 = None
        self.line6 = None
        self.line7 = None
        self.line8 = None
        self.line9 = None

    def add_metadata(self, type):
        '''
        adds the title, axis labels, channel names etc .....
        :param type: data or csv
        :return: True or False.
        '''
        type = type.lower()
        if type == 'data':
            metadata = self.instrument
        elif type == 'csv':
            metadata = self.metadata
        else:
            # todo logger bits.
            print('Type unknown')
            return False

        self.instrument_name = self.instrument.instrument_identifier
        self.number_of_channels = self.instrument.instrument_number_of_channels
        self.xlabel = self.instrument.XaxisLabel
        self.ylabel = self.instrument.YaxisLabel

        range = self.instrument.YaxisRange.split(',')
        self.yRangeStart = range[0]
        self.yRangeStop = range[1]

        if self.number_of_channels == '2':
            self.channel1_label = metadata.channel_names[0]
            self.channel1_colour
            self.channel2_label = metadata.channel_names[1]
            self.channel2_colour
        elif self.number_of_channels == '3':
            self.channel1_label = metadata.channel_names[0]
            self.channel1_colour
            self.channel2_label = metadata.channel_names[1]
            self.channel2_colour
            self.channel3_label = metadata.channel_names[2]
            self.channel3_colour
        elif self.number_of_channels == '4':
            self.channel1_label = metadata.channel_names[0]
            self.channel1_colour
            self.channel2_label = metadata.channel_names[1]
            self.channel2_colour
            self.channel3_label = metadata.channel_names[2]
            self.channel3_colour
            self.channel4_label = metadata.channel_names[3]
            self.channel4_colour
        elif self.number_of_channels == '5':
            self.channel1_label = metadata.channel_names[0]
            self.channel1_colour
            self.channel2_label = metadata.channel_names[1]
            self.channel1_colour
            self.channel3_label = metadata.channel_names[2]
            self.channel1_colour
            self.channel4_label = metadata.channel_names[3]
            self.channel1_colour
            self.channel5_label = metadata.channel_names[4]
            self.channel1_colour
        elif self.number_of_channels == '6':
            self.channel1_label = metadata.channel_names[0]
            self.channel1_colour
            self.channel2_label = metadata.channel_names[1]
            self.channel1_colour
            self.channel3_label = metadata.channel_names[2]
            self.channel1_colour
            self.channel4_label = metadata.channel_names[3]
            self.channel1_colour
            self.channel5_label = metadata.channel_names[4]
            self.channel1_colour
            self.channel6_label = metadata.channel_names[5]
            self.channel1_colour
        elif self.number_of_channels == '7':
            self.channel1_label = metadata.channel_names[0]
            self.channel1_colour
            self.channel2_label = metadata.channel_names[1]
            self.channel1_colour
            self.channel3_label = metadata.channel_names[2]
            self.channel1_colour
            self.channel4_label = metadata.channel_names[3]
            self.channel1_colour
            self.channel5_label = metadata.channel_names[4]
            self.channel1_colour
            self.channel6_label = metadata.channel_names[5]
            self.channel1_colour
            self.channel7_label = metadata.channel_names[6]
            self.channel1_colour
        elif self.number_of_channels == '8':
            self.channel1_label = metadata.channel_names[0]
            self.channel1_colour
            self.channel2_label = metadata.channel_names[1]
            self.channel1_colour
            self.channel3_label = metadata.channel_names[2]
            self.channel1_colour
            self.channel4_label = metadata.channel_names[3]
            self.channel1_colour
            self.channel5_label = metadata.channel_names[4]
            self.channel1_colour
            self.channel6_label = metadata.channel_names[5]
            self.channel1_colour
            self.channel7_label = metadata.channel_names[6]
            self.channel1_colour
            self.channel8_label = metadata.channel_names[7]
            self.channel1_colour
        elif self.number_of_channels == '9':
            self.channel1_label = metadata.channel_names[0]
            self.channel1_colour
            self.channel2_label = metadata.channel_names[1]
            self.channel1_colour
            self.channel3_label = metadata.channel_names[2]
            self.channel1_colour
            self.channel4_label = metadata.channel_names[3]
            self.channel1_colour
            self.channel5_label = metadata.channel_names[4]
            self.channel1_colour
            self.channel6_label = metadata.channel_names[5]
            self.channel1_colour
            self.channel7_label = metadata.channel_names[6]
            self.channel1_colour
            self.channel8_label = metadata.channel_names[7]
            self.channel1_colour
            self.channel9_label = metadata.channel_names[8]
            self.channel1_colour

    def add_mpl(self):

        if self.run_once is False:
            # set the mplwindow widget background to a gray otherwise splash page disfigured in toolbar.
            self.ui.mplwindow.setStyleSheet('QWidget{background-color: #EDEDED}')

            self.ui.mplvl.addWidget(self.canvas)

            toolbar = NavigationToolbar(self.canvas,
                                        self.ui.mplwindow, coordinates=True)
            self.ui.mplvl.addWidget(toolbar)
            self.run_once = True

    def add_data(self):

        self.clear()

        if self.number_of_channels == 2:
            self.ax1f1.plot(self.datatranslator.datetime, self.datatranslator.channel_1, self.channel0_colour, label=self.channel0_label)
            self.ax1f1.plot(self.datatranslator.datetime, self.datatranslator.channel_2, self.channel1_colour, label=self.channel1_label)
        elif self.number_of_channels == 3:
            self.ax1f1.plot(self.datatranslator.datetime, self.datatranslator.channel_1, self.channel0_colour, label=self.channel0_label)
            self.ax1f1.plot(self.datatranslator.datetime, self.datatranslator.channel_2, self.channel1_colour, label=self.channel1_label)
            self.ax1f1.plot(self.datatranslator.datetime, self.datatranslator.channel_3, self.channel2_colour, label=self.channel2_label)
        elif self.number_of_channels == 4:
            self.ax1f1.plot(self.datatranslator.datetime, self.datatranslator.channel_1, self.channel0_colour, label=self.channel0_label)
            self.ax1f1.plot(self.datatranslator.datetime, self.datatranslator.channel_2, self.channel1_colour, label=self.channel1_label)
            self.ax1f1.plot(self.datatranslator.datetime, self.datatranslator.channel_3, self.channel2_colour, label=self.channel2_label)
            self.ax1f1.plot(self.datatranslator.datetime, self.datatranslator.channel_4, self.channel3_colour, label=self.channel3_label)
        elif self.number_of_channels == 5:
            self.ax1f1.plot(self.datatranslator.datetime, self.datatranslator.channel_1, self.channel0_colour, label=self.channel0_label)
            self.ax1f1.plot(self.datatranslator.datetime, self.datatranslator.channel_2, self.channel1_colour, label=self.channel1_label)
            self.ax1f1.plot(self.datatranslator.datetime, self.datatranslator.channel_3, self.channel2_colour, label=self.channel2_label)
            self.ax1f1.plot(self.datatranslator.datetime, self.datatranslator.channel_4, self.channel3_colour, label=self.channel3_label)
            self.ax1f1.plot(self.datatranslator.datetime, self.datatranslator.channel_5, self.channel4_colour, label=self.channel4_label)
        elif self.number_of_channels == 6:
            self.ax1f1.plot(self.datatranslator.datetime, self.datatranslator.channel_1, self.channel0_colour, label=self.channel0_label)
            self.ax1f1.plot(self.datatranslator.datetime, self.datatranslator.channel_2, self.channel1_colour, label=self.channel1_label)
            self.ax1f1.plot(self.datatranslator.datetime, self.datatranslator.channel_3, self.channel2_colour, label=self.channel2_label)
            self.ax1f1.plot(self.datatranslator.datetime, self.datatranslator.channel_4, self.channel3_colour, label=self.channel3_label)
            self.ax1f1.plot(self.datatranslator.datetime, self.datatranslator.channel_5, self.channel4_colour, label=self.channel4_label)
            self.ax1f1.plot(self.datatranslator.datetime, self.datatranslator.channel_6, self.channel5_colour, label=self.channel5_label)
        elif self.number_of_channels == 7:
            self.ax1f1.plot(self.datatranslator.datetime, self.datatranslator.channel_1, self.channel0_colour, label=self.channel0_label)
            self.ax1f1.plot(self.datatranslator.datetime, self.datatranslator.channel_2, self.channel1_colour, label=self.channel1_label)
            self.ax1f1.plot(self.datatranslator.datetime, self.datatranslator.channel_3, self.channel2_colour, label=self.channel2_label)
            self.ax1f1.plot(self.datatranslator.datetime, self.datatranslator.channel_4, self.channel3_colour, label=self.channel3_label)
            self.ax1f1.plot(self.datatranslator.datetime, self.datatranslator.channel_5, self.channel4_colour, label=self.channel4_label)
            self.ax1f1.plot(self.datatranslator.datetime, self.datatranslator.channel_6, self.channel5_colour, label=self.channel5_label)
            self.ax1f1.plot(self.datatranslator.datetime, self.datatranslator.channel_7, self.channel7_colour, label=self.channel6_label)
        elif self.number_of_channels == 8:
            self.ax1f1.plot(self.datatranslator.datetime, self.datatranslator.channel_1, self.channel0_colour, label=self.channel0_label)
            self.ax1f1.plot(self.datatranslator.datetime, self.datatranslator.channel_2, self.channel1_colour, label=self.channel1_label)
            self.ax1f1.plot(self.datatranslator.datetime, self.datatranslator.channel_3, self.channel2_colour, label=self.channel2_label)
            self.ax1f1.plot(self.datatranslator.datetime, self.datatranslator.channel_4, self.channel3_colour, label=self.channel3_label)
            self.ax1f1.plot(self.datatranslator.datetime, self.datatranslator.channel_5, self.channel4_colour, label=self.channel4_label)
            self.ax1f1.plot(self.datatranslator.datetime, self.datatranslator.channel_6, self.channel5_colour, label=self.channel5_label)
            self.ax1f1.plot(self.datatranslator.datetime, self.datatranslator.channel_7, self.channel6_colour, label=self.channel6_label)
            self.ax1f1.plot(self.datatranslator.datetime, self.datatranslator.channel_8, self.channel7_colour, label=self.channel7_label)
        elif self.number_of_channels == 9:
            self.ax1f1.plot(self.datatranslator.datetime, self.datatranslator.channel_1, self.channel0_colour, label=self.channel0_label)
            self.ax1f1.plot(self.datatranslator.datetime, self.datatranslator.channel_2, self.channel1_colour, label=self.channel1_label)
            self.ax1f1.plot(self.datatranslator.datetime, self.datatranslator.channel_3, self.channel2_colour, label=self.channel2_label)
            self.ax1f1.plot(self.datatranslator.datetime, self.datatranslator.channel_4, self.channel3_colour, label=self.channel3_label)
            self.ax1f1.plot(self.datatranslator.datetime, self.datatranslator.channel_5, self.channel4_colour, label=self.channel4_label)
            self.ax1f1.plot(self.datatranslator.datetime, self.datatranslator.channel_6, self.channel5_colour, label=self.channel5_label)
            self.ax1f1.plot(self.datatranslator.datetime, self.datatranslator.channel_7, self.channel6_colour, label=self.channel6_label)
            self.ax1f1.plot(self.datatranslator.datetime, self.datatranslator.channel_8, self.channel7_colour, label=self.channel7_label)
            self.ax1f1.plot(self.datatranslator.datetime, self.datatranslator.channel_9, self.channel8_colour, label=self.channel8_label)
        else:
            self.logger.critical('INVALID_XML Number of channels outside of scope.')
            return 'INVALID_XML', None

        # Set the X axis tick format and X axis toolbar reading.
        if sys.platform.startswith('win'):
            # You can't have a newline in the date time string on Windows so we do it the horrid way of autofmt_xdate.
            self.ax1f1.xaxis.set_major_formatter(dates.DateFormatter('%d-%b %H:%M:%S'))
            self.fig.autofmt_xdate()
        else:
            self.ax1f1.xaxis.set_major_formatter(dates.DateFormatter('%H:%M:%S%n%d-%b'))

        self.ax1f1.fmt_xdata = dates.DateFormatter('%Y-%m-%d %H:%M:%S')

        if self.config.get('chart_metadata', 'show_label') == 'y':
            self.ax1f1.legend(loc='upper right')

        self.canvas.draw()

        return 'SUCCESS', None

    def clear(self):
        self.ax1f1.clear()
        self.ax1f1.set_ylim(self.yRangeStart, self.yRangeStop)
        self.ax1f1.set_xlabel(self.xlabel)
        self.ax1f1.set_ylabel(self.ylabel)
        self.ax1f1.set_title(self.instrument_name)
        self.ax1f1.grid(True)
        #self.fig.autofmt_xdate()

