# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\Marija\Documents\workspace\tests\quad_centering\QuadCentering_v3.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
import pyqtgraph as pq


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Quad Centering")
        Form.resize(1529, 858)
        #main layout
        self.gridLayout = QtGui.QGridLayout(Form)
        self.gridLayout.setObjectName("gridLayout")
        
        #VL1
        self.verticalLayout1 = QtGui.QVBoxLayout()
        self.verticalLayout1.setSizeConstraint(QtGui.QLayout.SetMinimumSize)
        self.verticalLayout1.setObjectName("verticalLayout")

        #self.graphicsView = pq.ImageView()
        self.cameraWidget = pq.PlotWidget(title='')
        self.cameraWidget.setGeometry(QtCore.QRect(0, 1, 491, 501))
        self.cameraWidget.setObjectName("graphicsView")
        self.img = pq.ImageItem(border='w')
        self.cameraWidget.addItem(self.img)
        #self.graphicsView.setMinimumSize(QtCore.QSize(450, 350))
        #self.graphicsView.setMaximumSize(QtCore.QSize(650, 550))
        
        #vspaceritem = QtGui.QSpacerItem(100,100,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Expanding)
        
        self.scanPlotWidget = pq.PlotWidget(useOpenGL=True)
        self.scanPlotWidget.setMaximumSize(QtCore.QSize(650, 250))
        self.scanPlotWidget.setGeometry(QtCore.QRect(9, 619, 481, 211))
        self.scanPlotWidget.setAutoFillBackground(False)
        self.scanPlotWidget.setObjectName("scanPlotWidget")
        self.plot01 = self.scanPlotWidget.plot()
        #self.scanPlotWidget.
        
        self.verticalLayout1.addWidget(self.cameraWidget)
        #self.verticalLayout.addItem(vspaceritem)
        self.verticalLayout1.addWidget(self.scanPlotWidget)
        self.gridLayout.addLayout(self.verticalLayout1, 0, 0, 1, 1)
        
        #VL2        
        self.VerticalLayout2 = QtGui.QVBoxLayout()
        self.VerticalLayout2.setSizeConstraint(QtGui.QLayout.SetDefaultConstraint)
        self.VerticalLayout2.setObjectName("VerticalLayout2")
        
        #box1
        self.DeviceSelectionBox = QtGui.QGroupBox()
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.DeviceSelectionBox.sizePolicy().hasHeightForWidth())
        self.DeviceSelectionBox.setSizePolicy(sizePolicy)
        self.DeviceSelectionBox.setMaximumSize(QtCore.QSize(350, 150))
        self.DeviceSelectionBox.setMinimumSize(QtCore.QSize(200, 200))
        self.DeviceSelectionBox.setObjectName("DeviceSelectionBox")
        
        self.SectionSelectionLabel = QtGui.QLabel(self.DeviceSelectionBox)
        self.SectionSelectionLabel.setGeometry(QtCore.QRect(20, 20, 50, 13))
        self.SectionSelectionLabel.setObjectName("SectionSelectionLabel")
        self.quadSelectionLabel = QtGui.QLabel(self.DeviceSelectionBox)
        self.quadSelectionLabel.setGeometry(QtCore.QRect(20, 50, 50, 16))
        self.quadSelectionLabel.setObjectName("screenSelectionLabel")        
        self.correctorSelectionLabel = QtGui.QLabel(self.DeviceSelectionBox)
        self.correctorSelectionLabel.setGeometry(QtCore.QRect(20, 80, 50, 13))
        self.correctorSelectionLabel.setObjectName("quadSelectionLabel")    
        self.screenSelectionLabel = QtGui.QLabel(self.DeviceSelectionBox)
        self.screenSelectionLabel.setGeometry(QtCore.QRect(20, 110, 50, 13))
        self.screenSelectionLabel.setObjectName("correctorSelectionLabel")        
        
        self.SectionSelectionCombobox = QtGui.QComboBox(self.DeviceSelectionBox)
        self.SectionSelectionCombobox.setGeometry(QtCore.QRect(80, 20, 271, 20))
        self.SectionSelectionCombobox.setObjectName("SectionSelectionCombobox")
        self.quadSelectionCombobox = QtGui.QComboBox(self.DeviceSelectionBox)
        self.quadSelectionCombobox.setGeometry(QtCore.QRect(80, 50, 271, 20))
        self.quadSelectionCombobox.setObjectName("screenSelectrionCombobox")
        self.correctorSelectionCombobox = QtGui.QComboBox(self.DeviceSelectionBox)
        self.correctorSelectionCombobox.setGeometry(QtCore.QRect(80, 80, 271, 20))
        self.correctorSelectionCombobox.setObjectName("quadSelectionCombobox")
        self.screenSelectionCombobox = QtGui.QComboBox(self.DeviceSelectionBox)
        self.screenSelectionCombobox.setGeometry(QtCore.QRect(80, 110, 271, 20))
        self.screenSelectionCombobox.setObjectName("correctorSelectionCombobox")
        
        #self.startScanButton = QtGui.QPushButton(self.ScanSetupBox)
        #self.startScanButton.setGeometry(QtCore.QRect(200, 110, 75, 23))
        #self.startScanButton.setObjectName("startScanButton")
        
        self.startCameraButton = QtGui.QPushButton(self.DeviceSelectionBox)
        self.startCameraButton.setGeometry(QtCore.QRect(80, 140, 100, 30))
        self.startCameraButton.setObjectName("start camera")
        self.startCameraButton.setText('start camera')

        self.stopCameraButton = QtGui.QPushButton(self.DeviceSelectionBox)
        self.stopCameraButton.setGeometry(QtCore.QRect(200, 140, 100, 30))
        self.stopCameraButton.setObjectName("stop camera")
        self.stopCameraButton.setText('stop camera')

        self.VerticalLayout2.addWidget(self.DeviceSelectionBox)
        
        #box2
        self.DeviceInfoBox = QtGui.QGroupBox()
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.DeviceInfoBox.sizePolicy().hasHeightForWidth())
        self.DeviceInfoBox.setSizePolicy(sizePolicy)
        self.DeviceInfoBox.setMinimumSize(QtCore.QSize(150, 0))
        self.DeviceInfoBox.setMaximumSize(QtCore.QSize(200, 80))
        self.DeviceInfoBox.setObjectName("DeviceInfoBox")
        self.quadReadValueLabel = QtGui.QLabel(self.DeviceInfoBox)
        self.quadReadValueLabel.setGeometry(QtCore.QRect(20, 20, 41, 16))
        self.quadReadValueLabel.setObjectName("quadReadValueLabel")
        self.quadReadValue = QtGui.QLabel(self.DeviceInfoBox)
        self.quadReadValue.setGeometry(QtCore.QRect(80, 23, 49, 13))
        self.quadReadValue.setObjectName("quadReadValue")
        self.correctorReadValueLabel = QtGui.QLabel(self.DeviceInfoBox)
        self.correctorReadValueLabel.setGeometry(QtCore.QRect(20, 50, 41, 16))
        self.correctorReadValueLabel.setObjectName("correctorReadValueLabel")
        self.correctorReadValue = QtGui.QLabel(self.DeviceInfoBox)
        self.correctorReadValue.setGeometry(QtCore.QRect(80, 53, 49, 13))
        self.correctorReadValue.setObjectName("correctorReadValue")
        self.VerticalLayout2.addWidget(self.DeviceInfoBox)
        
        #box3
        self.ScanSetupBox = QtGui.QGroupBox()
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ScanSetupBox.sizePolicy().hasHeightForWidth())
        self.ScanSetupBox.setSizePolicy(sizePolicy)
        self.ScanSetupBox.setMaximumSize(QtCore.QSize(650, 150))
        self.ScanSetupBox.setMinimumSize(QtCore.QSize(450, 100))
        self.ScanSetupBox.setAutoFillBackground(False)
        self.ScanSetupBox.setObjectName("ScanSetupBox")
        self.quadNumLabel = QtGui.QLabel(self.ScanSetupBox)
        self.quadNumLabel.setGeometry(QtCore.QRect(20, 20, 71, 16))
        self.quadNumLabel.setObjectName("quadNumLabel")
        self.quadMinLabel = QtGui.QLabel(self.ScanSetupBox)
        self.quadMinLabel.setGeometry(QtCore.QRect(20, 50, 71, 16))
        self.quadMinLabel.setObjectName("quadMinLabel")
        self.quadMaxLabel = QtGui.QLabel(self.ScanSetupBox)
        self.quadMaxLabel.setGeometry(QtCore.QRect(20, 80, 71, 16))
        self.quadMaxLabel.setObjectName("quadMaxLabel")
        self.NumShotsLabel = QtGui.QLabel(self.ScanSetupBox)
        self.NumShotsLabel.setGeometry(QtCore.QRect(20, 110, 71, 16))
        self.NumShotsLabel.setObjectName("NumShotsLabel")
        
        self.quadNumSpinbox = QtGui.QSpinBox(self.ScanSetupBox)
        self.quadNumSpinbox.setGeometry(QtCore.QRect(100, 20, 72, 22))
        self.quadNumSpinbox.setProperty("value", 4)
        self.quadNumSpinbox.setObjectName("quadNumSpinbox")
        self.quadMinSpinbox = QtGui.QDoubleSpinBox(self.ScanSetupBox)
        self.quadMinSpinbox.setGeometry(QtCore.QRect(100, 50, 72, 22))
        self.quadMinSpinbox.setObjectName("quadMinSpinbox")
        self.quadMinSpinbox.setMinimum(-100)
        self.quadMinSpinbox.setDecimals(3)        
        self.quadMaxSpinbox = QtGui.QDoubleSpinBox(self.ScanSetupBox)
        self.quadMaxSpinbox.setGeometry(QtCore.QRect(100, 80, 72, 22))
        self.quadMaxSpinbox.setObjectName("quadMaxSpinbox")
        self.quadMaxSpinbox.setMinimum(-100)
        self.quadMaxSpinbox.setDecimals(3)
        self.numShotsSpinbox = QtGui.QSpinBox(self.ScanSetupBox)
        self.numShotsSpinbox.setGeometry(QtCore.QRect(100, 110, 72, 22))
        self.numShotsSpinbox.setProperty("value", 1)
        self.numShotsSpinbox.setObjectName("numShotsSpinbox")

        self.numCorrLabel = QtGui.QLabel(self.ScanSetupBox)
        self.numCorrLabel.setGeometry(QtCore.QRect(200, 20, 81, 16))
        self.numCorrLabel.setObjectName("numCorrLabel")       
        self.corrMinLabel = QtGui.QLabel(self.ScanSetupBox)
        self.corrMinLabel.setGeometry(QtCore.QRect(200, 50, 81, 16))
        self.corrMinLabel.setObjectName("corrMinLabel")
        self.ImaxLabel = QtGui.QLabel(self.ScanSetupBox)
        self.ImaxLabel.setGeometry(QtCore.QRect(200, 80, 81, 16))
        self.ImaxLabel.setObjectName("ImaxLabel")
        
        self.numCorrSpinbox = QtGui.QSpinBox(self.ScanSetupBox)
        self.numCorrSpinbox.setGeometry(QtCore.QRect(280, 20, 72, 22))
        self.numCorrSpinbox.setProperty("value", 5)
        self.numCorrSpinbox.setObjectName("numCorrSpinbox")                
        self.corrMinSpinbox = QtGui.QDoubleSpinBox(self.ScanSetupBox)
        self.corrMinSpinbox.setGeometry(QtCore.QRect(280, 50, 72, 22))
        self.corrMinSpinbox.setObjectName("corrMinSpinbox")
        self.corrMinSpinbox.setMinimum(-100)
        self.corrMinSpinbox.setDecimals(3)
        self.corrMaxSpinbox = QtGui.QDoubleSpinBox(self.ScanSetupBox)
        self.corrMaxSpinbox.setGeometry(QtCore.QRect(280, 80, 72, 22))
        self.corrMaxSpinbox.setObjectName("corrMax")   
        self.corrMaxSpinbox.setMinimum(-100)
        self.corrMaxSpinbox.setDecimals(3)
        
        self.startScanButton = QtGui.QPushButton(self.ScanSetupBox)
        self.startScanButton.setGeometry(QtCore.QRect(200, 110, 75, 23))
        self.startScanButton.setObjectName("startScanButton")

        self.VerticalLayout2.addWidget(self.ScanSetupBox)
        
        
        ## box test
        self.LoadDataBox = QtGui.QGroupBox()
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.LoadDataBox.sizePolicy().hasHeightForWidth())        
        
        self.LoadDataBox.setSizePolicy(sizePolicy)
        self.LoadDataBox.setMaximumSize(QtCore.QSize(650, 150))
        self.LoadDataBox.setMinimumSize(QtCore.QSize(450, 100))
        self.LoadDataBox.setAutoFillBackground(False)
        self.LoadDataBox.setObjectName("LoadDataBox")
        
        self.loadScanDataButton = QtGui.QPushButton(self.LoadDataBox)
        self.loadScanDataButton.setGeometry(QtCore.QRect(80, 40, 120, 30))
        self.loadScanDataButton.setObjectName("load scan data")
        self.loadScanDataButton.setText('load scan data')

        self.loadFromDiskButton = QtGui.QPushButton(self.LoadDataBox)
        self.loadFromDiskButton.setGeometry(QtCore.QRect(80, 80, 120, 30))
        self.loadFromDiskButton.setObjectName("load from disk")
        self.loadFromDiskButton.setText('load from disk')
        
        self.analyzeDataButton = QtGui.QPushButton(self.LoadDataBox)
        self.analyzeDataButton.setGeometry(QtCore.QRect(80, 120, 120, 30))
        self.analyzeDataButton.setObjectName("analyze_data")
        self.analyzeDataButton.setText('analyze data')

        self.VerticalLayout2.addWidget(self.LoadDataBox)        
        ##
        
        self.gridLayout.addLayout(self.VerticalLayout2, 0, 1, 1, 1)
        self.verticalLayout_3 = QtGui.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        
        self.AnalysisPlot1 = pq.PlotWidget(useOpenGL=True, title='Peak pos vs quad I')
        self.AnalysisPlot1.setMaximumSize(QtCore.QSize(450, 400))
        self.AnalysisPlot1.setObjectName("AnalysisPlot1")
        self.plot11 = self.AnalysisPlot1.plot()
        self.verticalLayout_3.addWidget(self.AnalysisPlot1)
        
        self.AnalysisPlot2 = pq.PlotWidget(useOpenGL=True, title='Slope vs corr I')
        self.AnalysisPlot2.setMaximumSize(QtCore.QSize(450, 400))
        self.AnalysisPlot2.setObjectName("AnalysisPlot2")
        self.verticalLayout_3.addWidget(self.AnalysisPlot2)
        self.plot21 = self.AnalysisPlot2.plot()        
        
        self.gridLayout.addLayout(self.verticalLayout_3, 0, 2, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Quad Centering"))
        self.DeviceSelectionBox.setTitle(_translate("Form", "Device Selection"))
        self.SectionSelectionLabel.setText(_translate("Form", "Section"))
        self.quadSelectionLabel.setText(_translate("Form", "Quad"))
        self.screenSelectionLabel.setText(_translate("Form", "Screen"))
        self.correctorSelectionLabel.setText(_translate("Form", "Corrector"))
        self.DeviceInfoBox.setTitle(_translate("Form", "Device info"))
        self.quadReadValueLabel.setText(_translate("Form", "quad I"))
        self.quadReadValue.setText(_translate("Form", "--"))
        self.correctorReadValueLabel.setText(_translate("Form", "corr I"))
        self.correctorReadValue.setText(_translate("Form", "--"))
        self.ScanSetupBox.setTitle(_translate("Form", "Scan Setup"))
        self.quadNumLabel.setText(_translate("Form", "Num quad I\'s"))
        self.NumShotsLabel.setText(_translate("Form", "Num shots"))
        self.quadMinLabel.setText(_translate("Form", "I quad min"))
        self.quadMaxLabel.setText(_translate("Form", "I quad max"))
        self.corrMinLabel.setText(_translate("Form", "I corr min"))
        self.ImaxLabel.setText(_translate("Form", "I corr max"))
        self.startScanButton.setText(_translate("Form", "Start scan"))
        self.numCorrLabel.setText(_translate("Form", "Num corr Is"))
        self.LoadDataBox.setTitle(_translate("Form", "Load Data"))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Form = QtGui.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

