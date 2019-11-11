# -*- coding:utf-8 -*-
"""
Created on Feb 1, 2016

@author: m
"""

from PyQt4 import QtGui, QtCore

import time
import sys
sys.path.insert(0, '../../guitests/src/QTangoWidgets')

import pyqtgraph as pq
import PyTango as pt
import threading
import numpy as np
# import QTangoWidgets as qw
from AttributeReadThreadClass import AttributeClass


# noinspection PyAttributeOutsideInit,PyAttributeOutsideInit,PyAttributeOutsideInit,PyAttributeOutsideInit,PyAttributeOutsideInit,PyAttributeOutsideInit,PyAttributeOutsideInit,PyAttributeOutsideInit,PyAttributeOutsideInit,PyAttributeOutsideInit,PyAttributeOutsideInit,PyAttributeOutsideInit,PyAttributeOutsideInit
class TangoDeviceClient(QtGui.QWidget):
    def __init__(self, redpitayaName, specName, motorName, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.devCam = pt.DeviceProxy('lima/liveviewer/i-bc2-dia-scrn-01')
        self.devQuad = pt.DeviceProxy('I-KBC2/MAG/PSPG-01-CAB07')
        self.devCorr = pt.DeviceProxy('I-KBC2/MAG/PSIA-04')
        
        self.timeVector = None
        self.xData = None
        self.xDataTemp = None


        self.title = 'Quad Centering'


        t0 = time.clock()
        print time.clock() - t0, ' s'

        self.guiLock = threading.Lock()
        self.positionOffset = 0.0
        self.wavelengthVector = self.specDev.read_attribute('Wavelengths')

        self.layout = QtGui.QVBoxLayout(self)
        self.gridLayout1 = QtGui.QGridLayout()
        self.gridLayout2 = QtGui.QGridLayout()
        self.gridLayout3 = QtGui.QGridLayout()
        self.gridLayout4 = QtGui.QGridLayout()


        self.startPosSpinbox = QtGui.QDoubleSpinBox()
        self.startPosSpinbox.setDecimals(3)
        self.startPosSpinbox.setMaximum(2000000)
        self.startPosSpinbox.setMinimum(-2000000)
        self.startPosSpinbox.setValue(46.8)
        self.stepSizeSpinbox = QtGui.QDoubleSpinBox()
        self.stepSizeSpinbox.setDecimals(3)
        self.stepSizeSpinbox.setMaximum(2000000)
        self.stepSizeSpinbox.setMinimum(-2000000)
        self.stepSizeSpinbox.setValue(0.05)
        self.currentPosSpinbox = QtGui.QDoubleSpinBox()
        self.currentPosSpinbox.setDecimals(3)
        self.currentPosSpinbox.setMaximum(2000000)
        self.currentPosSpinbox.setMinimum(-2000000)
        self.averageSpinbox = QtGui.QSpinBox()
        self.averageSpinbox.setMaximum(100)
        self.averageSpinbox.setValue(self.settings.value('averages', 5).toInt()[0])
        self.averageSpinbox.editingFinished.connect(self.setAverage)
        self.setPosSpinbox = QtGui.QDoubleSpinBox()
        self.setPosSpinbox.setDecimals(3)
        self.setPosSpinbox.setMaximum(2000000)
        self.setPosSpinbox.setMinimum(-2000000)
        self.setPosSpinbox.setValue(63.7)
        self.setPosSpinbox.setValue(self.settings.value('setPos', 63).toDouble()[0])
        self.setPosSpinbox.editingFinished.connect(self.writePosition)
        self.currentPosLabel = QtGui.QLabel()
        f = self.currentPosLabel.font()
        f.setPointSize(14)
        currentPosTextLabel = QtGui.QLabel('Current pos ')
        currentPosTextLabel.setFont(f)
        self.currentPosLabel.setFont(f)
        self.currentSpeedLabel = QtGui.QLabel()


        self.startButton = QtGui.QPushButton('Start')
        self.startButton.clicked.connect(self.startScan)
        self.stopButton = QtGui.QPushButton('Stop')
        self.stopButton.clicked.connect(self.stopScan)
        self.exportButton = QtGui.QPushButton('Export')
        self.exportButton.clicked.connect(self.exportScan)

        self.pos = self.motorDev.read_attribute('position').value
        self.currentPosSpinbox.setValue(self.pos)


        self.gridLayout1.addWidget(QtGui.QLabel("Start position"), 0, 0)
        self.gridLayout1.addWidget(self.startPosSpinbox, 0, 1)
        self.gridLayout1.addWidget(QtGui.QLabel("Step size"), 1, 0)
        self.gridLayout1.addWidget(self.stepSizeSpinbox, 1, 1)
        self.gridLayout1.addWidget(QtGui.QLabel("Averages"), 2, 0)
        self.gridLayout1.addWidget(self.averageSpinbox, 2, 1)
        self.gridLayout2.addWidget(QtGui.QLabel("Set position"), 0, 0)
        self.gridLayout2.addWidget(self.setPosSpinbox, 0, 1)
        self.gridLayout2.addWidget(QtGui.QLabel("Start scan"), 1, 0)
        self.gridLayout2.addWidget(self.startButton, 1, 1)
        self.gridLayout2.addWidget(QtGui.QLabel("Stop scan"), 2, 0)
        self.gridLayout2.addWidget(self.stopButton, 2, 1)
        self.gridLayout2.addWidget(QtGui.QLabel("Export scan"), 3, 0)
        self.gridLayout2.addWidget(self.exportButton, 3, 1)
        self.gridLayout3.addWidget(currentPosTextLabel, 0, 0)
        self.gridLayout3.addWidget(self.currentPosLabel, 0, 1)
        self.gridLayout3.addWidget(QtGui.QLabel("Current speed"), 1, 0)
        self.gridLayout3.addWidget(self.currentSpeedLabel, 1, 1)


        self.SpectrometerStatusLabel = QtGui.QLabel()
        SpectrometerStatusTextLabel= QtGui.QLabel('Spec Status')
        self.specStatus = self.specDev.read_attribute('State').value



        self.gridLayout4.addWidget(QtGui.QLabel("Init"), 1, 0)
        self.gridLayout4.addWidget(self.specInitButton, 1, 1)
        self.gridLayout4.addWidget(QtGui.QLabel("On"), 2, 0)
        self.gridLayout4.addWidget(self.specOnButton, 2, 1)
 
        self.gridLayout4.addWidget(QtGui.QLabel("Stop"), 3, 0)
        self.gridLayout4.addWidget(self.specStopButton, 3, 1)
        self.gridLayout4.addWidget(SpectrometerStatusTextLabel, 4, 0)
        self.gridLayout4.addWidget(self.SpectrometerStatusLabel, 4, 1)


        # plots
        self.plotWidget = pq.PlotWidget(useOpenGL=True)
        self.SpectrumPlot = self.plotWidget.plot()
        self.SpectrumPlot.setPen((200, 25, 10))
        self.SpectrumPlot.antialiasing = True
        self.plotWidget.setAntialiasing(True)
        self.plotWidget.showGrid(True, True)

        plotLayout = QtGui.QHBoxLayout()
        plotLayout.addWidget(self.plotWidget)

        #adding layouts        gridLay = QtGui.QHBoxLayout()
        gridLay = QtGui.QHBoxLayout()
        gridLay.addLayout(self.gridLayout1)
        gridLay.addSpacerItem(QtGui.QSpacerItem(30, 20, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum))
        gridLay.addLayout(self.gridLayout2)
        gridLay.addSpacerItem(QtGui.QSpacerItem(30, 20, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum))
        gridLay.addLayout(self.gridLayout3)
        gridLay.addSpacerItem(QtGui.QSpacerItem(30, 20, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum))
        gridLay.addLayout(self.gridLayout4)
        gridLay.addSpacerItem(QtGui.QSpacerItem(30, 20, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum))
        self.layout.addLayout(gridLay)
        self.layout.addLayout(plotLayout)


        self.waveform1 = np.zeros(4000)
        self.waveform2 = np.zeros(4000)
        self.trendData1 = np.zeros(600)
        self.trendData2 = np.zeros(600)
        self.scanData = np.array([])
        self.timeData = np.array([])
        self.posData = np.array([])
        self.avgSamples = 5
        self.currentSample = 0
        self.avgData = 0
        self.targetPos = 0.0
        self.measureUpdateTimes = np.array([time.time()])
        self.lock = threading.Lock()

        self.spectrum = np.array([])

        self.running = False
        self.scanning = False
        self.moving = False
        self.moveStart = False
        self.scanTimer = QtCore.QTimer()
        self.scanTimer.timeout.connect(self.scanUpdateAction)

        self.settings = QtCore.QSettings('Maxlab', 'RedpitayaTangoAutocorrelation')


        self.resize(800,400)
        self.update()


    def readSpectrometerState(self, data):
        print 'reading spectrometer status'
        self.SpectrometerStatusLabel.setText('status here')
        self.spectrometerName.setState(data)
        self.onOffCommands.setStatus(data)

    def readPeakEnergy(self, data):
        self.attributes['PeakEnergy'] = data.value

    def readPeakWidth(self, data):
        self.attributes['PeakWidth'] = data.value



    def setAverage(self):
        self.avgSamples = self.averageSpinbox.value()

    def startScan(self):
        self.scanData = np.array([])
        self.timeData = np.array([])
        self.scanning = True
        self.motorDev.write_attribute('position', self.startPosSpinbox.value())
        newPos = self.startPosSpinbox.value()
        self.pos = self.motorDev.read_attribute('position').value
        self.currentPosSpinbox.setValue(self.pos)
        print 'Moving from ', self.pos
        motorState = self.motorDev.state()
#        while self.pos != self.startPosSpinbox.value():
        while (np.abs(self.pos - newPos) > 0.005) or (motorState == pt.DevState.MOVING):
            time.sleep(0.25)
            self.pos = self.motorDev.read_attribute('position').value
            self.currentPosSpinbox.setValue(self.pos)
            motorState = self.motorDev.state()
            self.update()
        self.scanTimer.start(100 * self.avgSamples)


    def stopScan(self):
        print 'Stopping scan'
        self.running = False
        self.scanning = False
        self.scanTimer.stop()

    def exportScan(self):
        print 'Exporting scan data'
        data = np.vstack((self.posData, self.timeData, self.scanData)).transpose()
        filename = ''.join(('scandata_', time.strftime('%Y-%m-%d_%Hh%M'), '.txt'))
        np.savetxt(filename, data)

    def scanUpdateAction(self):
        self.scanTimer.stop()
        while self.running == True:
            time.sleep(0.1)
        newPos = self.targetPos + self.stepSizeSpinbox.value()
        print 'New pos: ', newPos
        self.attributes['position'].attr_write(newPos)
        self.targetPos = newPos
        self.running = True
        self.moveStart = True

    def measureScanData(self):
        self.avgData = self.trendData1[-self.avgSamples:].mean()
        self.scanData = np.hstack((self.scanData, self.avgData))
        pos = np.double(str(self.currentPosLabel.text()))
        newTime = (pos - self.startPosSpinbox.value()) * 2 * 1e-3 / 299792458.0
        self.timeData = np.hstack((self.timeData, newTime))
        self.posData = np.hstack((self.posData, pos * 1e-3))
        if self.timeUnitsRadio.isChecked() == True:
            self.plot5.setData(x=self.timeData * 1e12, y=self.scanData)
        else:
            self.plot5.setData(x=self.posData * 1e3, y=self.scanData)

    def measureData(self):
        if self.running == True and self.moving == False:
            data = self.devices['redpitaya'].read_attributes(['waveform1', 'waveform2'])
            self.waveform1 = data[0].value
            self.waveform2 = data[1].value
        goodInd = np.arange(self.signalStartIndex.value(), self.signalEndIndex.value() + 1, 1)
        bkgInd = np.arange(self.backgroundStartIndex.value(), self.backgroundEndIndex.value() + 1, 1)
        bkg = self.waveform1[bkgInd].mean()
        bkgPump = self.waveform2[bkgInd].mean()
        autoCorr = (self.waveform1[goodInd] - bkg).sum()
        pump = (self.waveform2[goodInd] - bkgPump).sum()
#        pump = 1.0
        if self.normalizePumpCheck.isChecked() == True:
            try:
                self.trendData1 = np.hstack((self.trendData1[1:], autoCorr / pump))
            except:
                pass
        else:
            self.trendData1 = np.hstack((self.trendData1[1:], autoCorr))
        self.plot3.setData(y=self.trendData1)

        # Evaluate the fps
        t = time.time()
        if self.measureUpdateTimes.shape[0] > 10:
            self.measureUpdateTimes = np.hstack((self.measureUpdateTimes[1:], t))
        else:
            self.measureUpdateTimes = np.hstack((self.measureUpdateTimes, t))
        fps = 1 / np.diff(self.measureUpdateTimes).mean()
        self.fpsLabel.setText(QtCore.QString.number(fps, 'f', 1))

        # If we are running a scan, update the scan data
        if self.running == True:
            if self.moving == False and self.moveStart == False:
                self.currentSample += 1
                if self.currentSample >= self.avgSamples:
                    self.running = False
                    self.measureScanData()
                    self.currentSample = 0
                    self.scanUpdateAction()


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    myapp = TangoDeviceClient()
    myapp.show()
    sys.exit(app.exec_())



