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

import configparser
import logging
import sys


class Chart:

    # I got the how to do this from the following website and I thank the author for the information.
    # http://blog.rcnelson.com/building-a-matplotlib-gui-with-qt-designer-part-1/

    ''' Developer Note: Add generic container widget called mplwindow, drop any widget within mplwindow and layout
    vertical then delete the temporary widget. Set the vertical layout name to mplvl
    '''

    def __init__(self, parent):
        ##initialise logger
        self.logger = logging.getLogger('graphics.chart')
        self.config = configparser.RawConfigParser()
        self.config.read("client.conf")
        self.parent = parent
        self.instrument_name = self.parent.instrument.Instrument_Name
        self.number_of_channels = self.parent.instrument.Number_of_Channels
        self.xlabel = parent.datastore.XAxis
        self.ylabel = parent.datastore.YAxis
        #self.yRange = parent.datastore.YAxisRange
        rangelist = parent.datastore.YAxisRange.split(',')
        self.yRangeStart = int(rangelist[0].strip())
        self.yRangeStop = int(rangelist[1].strip())
        self.run_once = False
        self.count = 0 # Just a generic counter for testing purposes.

        # Standard Chart Colours are from
        # http://tableaufriction.blogspot.ro/2012/11/finally-you-can-use-tableau-data-colors.html

        self.channel0_label = 'Celsius'
        self.channel1_label = 'Channel 1'
        self.channel2_label = 'Channel 2'
        self.channel3_label = 'Channel 3'
        self.channel4_label = 'Channel 4'
        self.channel5_label = 'Channel 5'
        self.channel6_label = 'channel 6'
        self.channel7_label = 'channel 7'
        self.channel8_label = 'channel 8'
        self.channel0_colour = '#D62728'
        self.channel1_colour = '#1F77B4'
        self.channel2_colour = '#FF7F0E'
        self.channel3_colour = '#2CA02C'
        self.channel4_colour = '#9467BD'
        self.channel5_colour = '#8C564B'
        self.channel6_colour = '#E377C2'
        self.channel7_colour = '#BCBD22'
        self.channel8_colour = '#17BECF'


        mpl.rcParams['figure.autolayout'] = True
        mpl.rcParams['savefig.directory'] = self.config.get('instrument', 'datahome')
        mpl.rcParams['axes.linewidth'] = 0.5
        mpl.rcParams['axes.facecolor'] = "#FDFDF0"
        mpl.rcParams['figure.max_open_warning'] = 2

        self.fig = Figure()
        self.logger.info('Charting initialised.')

    def addmpl(self):

        if self.run_once is False:
            # set the mplwindow widget background to a gray otherwise splash page disfigured in toolbar.
            self.parent.mplwindow.setStyleSheet('QWidget{background-color: #EDEDED}')

            self.ax1f1 = self.fig.add_subplot(111)
            self.canvas = FigureCanvas(self.fig)
            self.parent.mplvl.addWidget(self.canvas)

            self.toolbar = NavigationToolbar(self.canvas,
                self.parent.mplwindow, coordinates=True)
            self.parent.mplvl.addWidget(self.toolbar)
            self.run_once = True

    def addData(self):

        if self.parent.datastore.parse_data() == 'PREMATURE_TERMINATION':
            return 'PREMATURE_TERMINATION'

        self.clear()

        if self.number_of_channels == 2:
            self.ax1f1.plot(self.parent.datastore.sampletime, self.parent.datastore.channel0, self.channel0_colour, label=self.channel0_label)
            self.ax1f1.plot(self.parent.datastore.sampletime, self.parent.datastore.channel1, self.channel1_colour, label=self.channel1_label)
        elif self.number_of_channels == 3:
            self.ax1f1.plot(self.parent.datastore.sampletime, self.parent.datastore.channel0, self.channel0_colour, label=self.channel0_label)
            self.ax1f1.plot(self.parent.datastore.sampletime, self.parent.datastore.channel1, self.channel1_colour, label=self.channel1_label)
            self.ax1f1.plot(self.parent.datastore.sampletime, self.parent.datastore.channel2, self.channel2_colour, label=self.channel2_label)
        elif self.number_of_channels == 4:
            self.ax1f1.plot(self.parent.datastore.sampletime, self.parent.datastore.channel0, self.channel0_colour, label=self.channel0_label)
            self.ax1f1.plot(self.parent.datastore.sampletime, self.parent.datastore.channel1, self.channel1_colour, label=self.channel1_label)
            self.ax1f1.plot(self.parent.datastore.sampletime, self.parent.datastore.channel2, self.channel2_colour, label=self.channel2_label)
            self.ax1f1.plot(self.parent.datastore.sampletime, self.parent.datastore.channel3, self.channel3_colour, label=self.channel3_label)
        elif self.number_of_channels == 5:
            self.ax1f1.plot(self.parent.datastore.sampletime, self.parent.datastore.channel0, self.channel0_colour, label=self.channel0_label)
            self.ax1f1.plot(self.parent.datastore.sampletime, self.parent.datastore.channel1, self.channel1_colour, label=self.channel1_label)
            self.ax1f1.plot(self.parent.datastore.sampletime, self.parent.datastore.channel2, self.channel2_colour, label=self.channel2_label)
            self.ax1f1.plot(self.parent.datastore.sampletime, self.parent.datastore.channel3, self.channel3_colour, label=self.channel3_label)
            self.ax1f1.plot(self.parent.datastore.sampletime, self.parent.datastore.channel4, self.channel4_colour, label=self.channel4_label)
        elif self.number_of_channels == 6:
            self.ax1f1.plot(self.parent.datastore.sampletime, self.parent.datastore.channel0, self.channel0_colour, label=self.channel0_label)
            self.ax1f1.plot(self.parent.datastore.sampletime, self.parent.datastore.channel1, self.channel1_colour, label=self.channel1_label)
            self.ax1f1.plot(self.parent.datastore.sampletime, self.parent.datastore.channel2, self.channel2_colour, label=self.channel2_label)
            self.ax1f1.plot(self.parent.datastore.sampletime, self.parent.datastore.channel3, self.channel3_colour, label=self.channel3_label)
            self.ax1f1.plot(self.parent.datastore.sampletime, self.parent.datastore.channel4, self.channel4_colour, label=self.channel4_label)
            self.ax1f1.plot(self.parent.datastore.sampletime, self.parent.datastore.channel5, self.channel5_colour, label=self.channel5_label)
        elif self.number_of_channels == 7:
            self.ax1f1.plot(self.parent.datastore.sampletime, self.parent.datastore.channel0, self.channel0_colour, label=self.channel0_label)
            self.ax1f1.plot(self.parent.datastore.sampletime, self.parent.datastore.channel1, self.channel1_colour, label=self.channel1_label)
            self.ax1f1.plot(self.parent.datastore.sampletime, self.parent.datastore.channel2, self.channel2_colour, label=self.channel2_label)
            self.ax1f1.plot(self.parent.datastore.sampletime, self.parent.datastore.channel3, self.channel3_colour, label=self.channel3_label)
            self.ax1f1.plot(self.parent.datastore.sampletime, self.parent.datastore.channel4, self.channel4_colour, label=self.channel4_label)
            self.ax1f1.plot(self.parent.datastore.sampletime, self.parent.datastore.channel5, self.channel5_colour, label=self.channel5_label)
            self.ax1f1.plot(self.parent.datastore.sampletime, self.parent.datastore.channel6, self.channel7_colour, label=self.channel6_label)
        elif self.number_of_channels == 8:
            self.ax1f1.plot(self.parent.datastore.sampletime, self.parent.datastore.channel0, self.channel0_colour, label=self.channel0_label)
            self.ax1f1.plot(self.parent.datastore.sampletime, self.parent.datastore.channel1, self.channel1_colour, label=self.channel1_label)
            self.ax1f1.plot(self.parent.datastore.sampletime, self.parent.datastore.channel2, self.channel2_colour, label=self.channel2_label)
            self.ax1f1.plot(self.parent.datastore.sampletime, self.parent.datastore.channel3, self.channel3_colour, label=self.channel3_label)
            self.ax1f1.plot(self.parent.datastore.sampletime, self.parent.datastore.channel4, self.channel4_colour, label=self.channel4_label)
            self.ax1f1.plot(self.parent.datastore.sampletime, self.parent.datastore.channel5, self.channel5_colour, label=self.channel5_label)
            self.ax1f1.plot(self.parent.datastore.sampletime, self.parent.datastore.channel6, self.channel6_colour, label=self.channel6_label)
            self.ax1f1.plot(self.parent.datastore.sampletime, self.parent.datastore.channel7, self.channel7_colour, label=self.channel7_label)
        elif self.number_of_channels == 9:
            self.ax1f1.plot(self.parent.datastore.sampletime, self.parent.datastore.channel0, self.channel0_colour, label=self.channel0_label)
            self.ax1f1.plot(self.parent.datastore.sampletime, self.parent.datastore.channel1, self.channel1_colour, label=self.channel1_label)
            self.ax1f1.plot(self.parent.datastore.sampletime, self.parent.datastore.channel2, self.channel2_colour, label=self.channel2_label)
            self.ax1f1.plot(self.parent.datastore.sampletime, self.parent.datastore.channel3, self.channel3_colour, label=self.channel3_label)
            self.ax1f1.plot(self.parent.datastore.sampletime, self.parent.datastore.channel4, self.channel4_colour, label=self.channel4_label)
            self.ax1f1.plot(self.parent.datastore.sampletime, self.parent.datastore.channel5, self.channel5_colour, label=self.channel5_label)
            self.ax1f1.plot(self.parent.datastore.sampletime, self.parent.datastore.channel6, self.channel6_colour, label=self.channel6_label)
            self.ax1f1.plot(self.parent.datastore.sampletime, self.parent.datastore.channel7, self.channel7_colour, label=self.channel7_label)
            self.ax1f1.plot(self.parent.datastore.sampletime, self.parent.datastore.channel8, self.channel8_colour, label=self.channel8_label)
        else:
            self.logger.critical('INVALID_XML Number of channels outside of scope.')
            return 'INVALID_XML'

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

        return 'SUCCESS'

    def clear(self):
        self.ax1f1.clear()
        self.ax1f1.set_ylim(self.yRangeStart, self.yRangeStop)
        self.ax1f1.set_xlabel(self.xlabel)
        self.ax1f1.set_ylabel(self.ylabel)
        self.ax1f1.set_title(self.instrument_name)
        self.ax1f1.grid(True)
        #self.fig.autofmt_xdate()

