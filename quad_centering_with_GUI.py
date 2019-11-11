'''
Created on 5 Nov 2018

@author: markot
'''


from QuadCentering_ui_v2 import Ui_Form

#import warnings
from PyQt4 import QtGui, QtCore
#import logging
import sys
import time
#import threading
import PyTango as pt
import numpy as np
import pyqtgraph as pq
#from scipy.stats import gennorm
#from scipy.special import gamma 
#from __builtin__ import str
#import scipy as sy
from time import sleep
from ConfigParser import SafeConfigParser
import os.path
from scipy.optimize import curve_fit
import glob
import matplotlib.pyplot as plt


class QuadCentering(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        #super().__init__()
        
        # pull device attribute names from the Tango database
        db = pt.Database()
        # Export every magnet there is
        self.magnetlist = db.get_device_exported_for_class('Magnet')[:]
        # Filter out everything that starts with 'I' (Linac) and contains 'Q' (quadrupole)
        self.section_quad_list = []
        self.section_names = []
        self.quad_list = []
        self.corrector_list = [x for x in self.magnetlist if x.startswith('I') and 'CO' in x]
        for x in self.magnetlist:                
            if x.startswith('I-') and 'Q' in x:
                section = x[0:str.find(x,'/MAG/')]
                self.quad_list.append(x)
                quad = x
                if section not in self.section_names:
                    self.section_names.append(section)
                listitem = [section,quad]
                self.section_quad_list.append(listitem)

        #cameralist = db.get_device_exported_for_class('BeamViewerDeviceServer')[:] 
        cameralist = db.get_device_exported_for_class('LiveViewer')[:] 
        BPMlist = db.get_device_exported_for_class('LiberaSinglePassE')[:]
        #screenlist = db.get_device_exported_for_class('CameraScreen')[:] 
        self.cameraNames = [x[0:] for x in cameralist if ('/I-' in x or '/i-' in x)]        
        self.BPMNames = [x for x in BPMlist if 'BPL' in x]
        #self.screenNames = [x for x in screenlist if 'SCRN' in x]    
        self.corrector_current = self.corrector_list[0]
        self.quad_selected = self.quad_list[0]
        self.camera_current = self.cameraNames[0]
        #print dir(self.camera_current)
        
        self.corrector_type = 'hkick'
        #roi initial values
        self._pixX = 400
        self._pixY = 120    

        self.x_no_pixels = 1282
        self.y_no_pixels = 1026  
        
        self.stop_timer = False
        self.cameraTimer = QtCore.QTimer()
        self.cameraTimer.timeout.connect(self.updateImage)
                
        self.ui = Ui_Form()
        x = self.ui.setupUi(self)
        self.setup_layout()
        #print dir(self.ui.graphicsView)
        self.configSetup()        
        #self.updatescreenSelected()

        
    def configSetup(self):
        #save and load settings
        self.config_file = 'config.ini'
        self.config = SafeConfigParser()
        self.config.read('config.ini')
        if not os.path.isfile(self.config_file):
            for quad in self.quad_list:
                self.config.add_section(quad)
                self.config.set(quad,'corr','')
                self.config.set(quad,'camera','')
                with open('config.ini','w') as f:
                    self.config.write(f)
        else:
            print self.config.get(self.quad_list[0],'corr')
            
    def initScanData(self):
        self.scan_result = dict()
        self.scan_result["raw_data"] = None
        #self.image_matrix = [[list() for j in range(self.noCorrScanPoints)] for i in range(self.noQuadScanPoints)]
        
        #im = np.zeros((5,6))
        #image_matrix = [x[:] for x in [[im]*3]*4]

        im = np.zeros(self.imageShape)
        self.image_matrix = [x[:] for x in [[im]*self.noQuadScanPoints]*self.noCorrScanPoints]
        
    def startScan(self):
        print 'starting scan'
                
        self.noCorrScanPoints = self.ui.numCorrSpinbox.value()
        self.corr_scan_initial = self.ui.corrMinSpinbox.value()
        self.corr_scan_final = self.ui.corrMaxSpinbox.value()
        self.corrScanValues = np.linspace(self.corr_scan_initial,self.corr_scan_final,self.noCorrScanPoints)
        
        self.noQuadScanPoints = self.ui.quadNumSpinbox.value()
        self.quad_scan_initial = self.ui.quadMinSpinbox.value()
        self.quad_scan_final = self.ui.quadMaxSpinbox.value()
        self.quadScanValues = np.linspace(self.quad_scan_initial,self.quad_scan_final,self.noQuadScanPoints)
        
        self.no_shots = self.ui.numShotsSpinbox.value()
        self.initScanData()
        
        
        #save selected settings
        with open('config.ini','w') as f:
            self.config.write(f)
            
        self.scanData = np.array([])
        #self.corrScanValues = np.array([])
        #self.quadScanValues = np.array([])
        self.scanning = True
        
#        xd, yd = self._roi.size()
#        xd = int(xd)
#        yd = int(yd)
#        x0, y0 = int(self._roi.x()), int(self._roi.y())    
#        print 'roi coords', x0,xd,y0,yd
        
        #img_cnt = self.cameraDevice.imagecounter
        #print img_cnt
        i=0
        j=0
        for corr_setting in self.corrScanValues:
            self.corrCircuitDev.write_attribute('Current',corr_setting)
            j=0
            for quad_setting in self.quadScanValues:
                print i,j
                self.quadCircuitDev.write_attribute('Current',quad_setting)
                print 'quad', str(quad_setting), 'corr', str(corr_setting)
                sleep(0.5)
                #image = np.random.rand(self.imageShape[0],self.imageShape[1])
                image = np.zeros(self.imageShape)
                for k in range(self.no_shots):
                    self.updateImage()
                    #print self.peak_position
                    image = (image*k + self.image)/(k+1)
                self.image_matrix[i][j]=image
                lineout = np.mean(image[self.roi_xi:self.roi_xf,self.roi_yi:self.roi_yf],0)
                current_curve = pq.PlotCurveItem(lineout, pen = i)
                self.ui.scanPlotWidget.addItem(current_curve)
                j+=1
            i+=1
                
        #return to start values               
        self.corrCircuitDev.write_attribute('Current',self.corr_current_initial)
        self.quadCircuitDev.write_attribute('Current',self.quad_current_initial)        
        
                
    def updateSectionSelected(self):
        self.ui.quadSelectionCombobox.clear()
        self.sectionSelected = self.ui.SectionSelectionCombobox.currentText()
        current_quad_names = []
        for [s,q] in self.section_quad_list:
            if s==self.sectionSelected:
                current_quad_names.append(q) 
                                
        self.ui.quadSelectionCombobox.addItems(current_quad_names)
        
    def updateCorrSelected(self):
        self.corr_current = self.ui.correctorSelectionCombobox.currentText()
        corrDevice = pt.DeviceProxy(str(self.corr_current))
        
        current_corr_circuit = corrDevice.get_property('CircuitProxies')['CircuitProxies'][0]
        current_corr_circuit_dev = pt.DeviceProxy(current_corr_circuit)
        current_corr_powersupply = current_corr_circuit_dev.get_property('PowerSupplyProxy')['PowerSupplyProxy'][0]

        self.corrCircuitDev = pt.DeviceProxy(current_corr_powersupply)
        self.corr_current_initial = self.corrCircuitDev.read_attribute('Current').value
        #print self.corr_current_initial
        self.ui.correctorReadValue.setText(str(self.corr_current_initial))
        self.corrector_type = corrDevice.get_property('Type')['Type'][0]
        self.ui.corrMinSpinbox.setValue(self.corr_current_initial-0.3)
        self.ui.corrMaxSpinbox.setValue(self.corr_current_initial+0.3)
        #print self.corrector_type
        #print self.quad_selected
        self.config.set(str(self.quad_selected),'corr',str(self.corr_current))
 
    def updateQuadSelected(self):
        self.quad_selected = self.ui.quadSelectionCombobox.currentText()
        quadDevice = pt.DeviceProxy(str(self.quad_selected))
        
        current_quad_circuit = quadDevice.get_property('CircuitProxies')['CircuitProxies'][0]
        current_quad_circuit_dev = pt.DeviceProxy(current_quad_circuit)
        current_quad_powersupply = current_quad_circuit_dev.get_property('PowerSupplyProxy')['PowerSupplyProxy'][0]

        self.quadCircuitDev = pt.DeviceProxy(current_quad_powersupply)
        self.quad_current_initial = self.quadCircuitDev.read_attribute('Current').value
        self.ui.quadMinSpinbox.setValue(0.2+self.quad_current_initial)
        self.ui.quadMaxSpinbox.setValue(-0.2+self.quad_current_initial)
        self.ui.quadReadValue.setText(str(self.quad_current_initial))
        
                    
        
    def updatescreenSelected(self):
        self.screenSelected = self.ui.screenSelectionCombobox.currentText()
        self.cameraDevice = pt.DeviceProxy(str(self.screenSelected))
        
        #take one image to determine the size of self.bkgndImage
        self.image = self.cameraDevice.read_attribute('Image').value.astype(np.double)
        self.image = np.rot90(self.image)
        self.bkgndImage = np.zeros((len(self.image),1))        
        self.imageShape = np.shape(self.image)
        
        self.updateImage()
        
        #self.cameraTimer = True

    def gaus_func(self, x, *p):
        """Function for fitting a Gaussian profile"""
        C, A, mu, sigma = p
        return A * np.exp( -(x-mu)**2 / (2.*sigma**2) ) + C
        
    def lin_func(self,x,*p):
        a, b = p
        return a*x+b
        
    def updateImage(self):
        #if self.subtractBkgndButton.isChecked():
        self.image = self.cameraDevice.read_attribute('Image').value.astype(np.double)
        #-self.bkgndImage
        self.image = self.cameraDevice.image.astype(np.int16)
        self.image = np.rot90(self.image)
            #-self.bkgndImage,3)
        #else:
        #    self.image = np.rot90(self.cameraDevice.image,3).astype(np.int16)
            #self.image = self.cameraDevice.read_attribute('Image').value.astype(np.double)
        self.ui.img.setImage(self.image)

        crop = self._roi.getArrayRegion(self.image,self.ui.img)
        if self.corrector_type == 'hkick':
            self.lineout_axis = 0
        else:
            self.lineout_axis = 1
        self.imgLineout = np.sum(crop,axis=self.lineout_axis)
        #fwhm_current = self.fwhm(self.imgLineout)
        #fwhm_current = 0
 
        #lineout and fit to it
        self.plot11.setData(self.imgLineout)
        ydata = self.imgLineout
        xdata = np.arange(1, len(ydata)+1)
        #initial guess for the fit
        c = np.mean(ydata[0:25] + ydata[-26:-1]) / 2
        mu = len(xdata)/2
        s = 50
        a = np.max(ydata) - c 
        p0 =    [c, a, mu, s]    
        coeff, var_matrix = curve_fit(self.gaus_func, xdata, ydata, p0=p0, maxfev = 10000)
        self.peak_position = coeff[2]
        fit = self.gaus_func(xdata, *coeff)    
        #print coeff    
        
        self.plot12.setData(fit)
        
        
        if self.stop_timer is not True:
            self.cameraTimer.start(100)
            
    def change_roi(self):
        roi_xd, roi_yd = np.round(self._roi.size())
        self.roi_xi, self.roi_yi = np.round(self._roi.pos())
        self.roi_xf, self.roi_yf = self.roi_xi+roi_xd, self.roi_yi+roi_yd
        #self._pixX = np.round(xd)
        #self._pixY = np.round(yd)  
        print self.roi_xi,self.roi_xf, self.roi_yi,self.roi_yf
    
 
    def setup_layout(self):
        
        #graphic        
        self.ui.cameraWidget.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        #print dir(self.ui.cameraWidget)
        #self.ui.cameraWidget.
        
        #roi
        self._roi = pq.ROI([30, 510], [self._pixX, self._pixY])
        self._roi.addScaleHandle(1, 0)
        self._roi.scaleSnap = True  # Force ROI to integer snap positions
        #self._roi.maxBounds = QtCore.QRect(0, 0, 1280, 1024)
        self._roi.sigRegionChangeFinished.connect(self.change_roi)
        #self.ui.graphicsView.addItem(self._roi)
        #self._roi.setZValue(10)  # make sure ROI is drawn above image
        self.ui.cameraWidget.addItem(self._roi)
        
        
        #lineout & fit to it
        self.plot11 = self.ui.scanPlotWidget.plot(axisItems = ['signal sum','pixel','',''])
        self.plot12 = self.ui.scanPlotWidget.plot(axisItems = ['fit','pixel','',''])
        pen=pq.mkPen('r', width=2, style=QtCore.Qt.DashLine)
        self.plot12.setPen(pen)

        #combo boxes
        self.ui.SectionSelectionCombobox.addItems(self.section_names)
        self.ui.SectionSelectionCombobox.setCurrentIndex(0)
        self.ui.SectionSelectionCombobox.currentIndexChanged.connect(self.updateSectionSelected)
        #self.ui.SectionSelectionCombobox.setCurrentIndex(1)
        self.ui.SectionSelectionCombobox.setCurrentIndex(3)
        
        self.ui.quadSelectionCombobox.currentIndexChanged.connect(self.updateQuadSelected)
        self.ui.quadSelectionCombobox.setCurrentIndex(2)
        
        self.ui.screenSelectionCombobox.addItems(self.cameraNames)
        self.ui.screenSelectionCombobox.currentIndexChanged.connect(self.updatescreenSelected)
        self.ui.screenSelectionCombobox.setCurrentIndex(14)
        
        self.ui.correctorSelectionCombobox.addItems(self.corrector_list)
        self.ui.correctorSelectionCombobox.currentIndexChanged.connect(self.updateCorrSelected)
        self.ui.correctorSelectionCombobox.setCurrentIndex(36)

        self.ui.startCameraButton.clicked.connect(self.cameraStart)
        self.ui.stopCameraButton.clicked.connect(self.cameraStop)
        
        self.ui.startScanButton.clicked.connect(self.startScan)
        
        self.ui.loadFromDiskButton.clicked.connect(self.loadDataFromDisk)
        self.ui.analyzeDataButton.clicked.connect(self.analyzeData)
        self.ui.loadScanDataButton.clicked.connect(self.loadScanData)
        
    def loadScanData(self):
        self.cameraTimer = False        
        
        #self.no_corr = self.noCorrScanPoints
        #self.no_quad = self.noQuadScanPoints
        #self.no_shots = self
        #self.corrData = self.corrScanValues
        
        #use a composit image to choose a ROI
        for i in range(self.noCorrScanPoints):
            for j in range(self.noQuadScanPoints):
                #for k in range(self.no_shots):
                im = self.image_matrix[i][j]
                if i==j==0:
                    self.x_no_pixels, self.y_no_pixels = im.shape
                    composite_image = np.zeros((self.x_no_pixels,self.y_no_pixels))
                    composite_image+=im
                
        self.ui.img.setImage(composite_image)
      
        
    def loadDataFromDisk(self):
        self.cameraTimer = False
        filelist = glob.glob('img_[0-9]*.tiff')


        self.noCorrScanPoints = np.max([int(x[4]) for x in filelist])
        self.noQuadScanPoints = np.max([int(x[6]) for x in filelist])
        self.no_shots = np.max([int(x[8]) for x in filelist])
        
        try:
            corr_and_quad_settings_filename = 'corr_and_quad_settings.txt'
            data = np.load(corr_and_quad_settings_filename)
        except:
            self.corrScanValues = np.arange(self.noCorrScanPoints)
            self.quadScanValues = np.arange(self.noQuadScanPoints) 

        for i in range(self.noCorrScanPoints):
            for j in range(self.noQuadScanPoints):
                for k in range(self.no_shots):
                    #determine the image size
                    fname = ''.join(('img_',str(i+1),'_',str(j+1),'_',str(k+1),'.tiff'))
                    im = plt.imread(fname)
                    if i==j==k==0:
                        self.x_no_pixels, self.y_no_pixels = im.shape
                        composite_image = np.zeros((self.x_no_pixels,self.y_no_pixels))
                    composite_image+=im
        
        #self.ui.img.setImage(np.rot90(composite_image))                    
        self.ui.img.setImage(composite_image)
        
        #filelocation = '/home/controlroom/Link to Marija/quad_centering'
        #filename= str(QtGui.QFileDialog.getOpenFileName(self,'Select files',filelocation,'img*.tiff'))
        #print filename
        #root.debug(''.join(('File selected: ', str(filename))))
        
    def analyzeData(self):
        print 'analyzing data'        
        #self.ui.plot01.setData([])
        self.ui.scanPlotWidget.clear()
        self.ui.AnalysisPlot1.clear()
        self.ui.AnalysisPlot2.clear()
        self.peak_positions = np.zeros((self.noCorrScanPoints,self.noQuadScanPoints))
    
    
        for i in range(self.noCorrScanPoints):
            for j in range(self.noQuadScanPoints):
                current_summed_lineout = np.zeros(self.roi_xf-self.roi_xi)                
                for k in range(self.no_shots):
                    fname = ''.join(('img_',str(i+1),'_',str(j+1),'_',str(k+1),'.tiff'))
                    im = plt.imread(fname)
                        
                    lineout = np.mean(im[self.roi_xi:self.roi_xf,self.roi_yi:self.roi_yf],1)
                    current_summed_lineout = (current_summed_lineout*k+lineout)/(k+1.0)
                    #lineout = np.mean(im[480:650,900:1250],1)
                
                #fitting to each line
                xdata = np.arange(len(current_summed_lineout))
                ydata = current_summed_lineout
                c = np.mean(ydata[0:25] + ydata[-26:-1]) / 2
                mu = len(xdata)/2
                s = 50
                a = np.max(ydata) - c 
                p0 =    [c, a, mu, s]  
                try:
                    coeff, var_matrix = curve_fit(self.gaus_func, xdata, ydata, p0=p0, maxfev = 10000)
                except:
                    coeff = p0
                self.peak_positions[i,j] = coeff[2]
                #fit = self.gaus_func(xdata, *coeff)   
                    
                current_curve = pq.PlotCurveItem(current_summed_lineout, pen = i)
                self.ui.scanPlotWidget.addItem(current_curve)
                #self.ui.plot01.setData(lineout)
                
        slope =[]
        for i in range(self.noCorrScanPoints):
            current_line = pq.PlotDataItem(self.peak_positions[i,:], pen = i, symbol = 'o')
            xdata = np.arange(len(self.peak_positions[i,:]))
            coeff,var_matrix = curve_fit(self.lin_func, xdata, self.peak_positions[i,:], p0=[1, 10])
            slope.append(coeff[0])
            #current_line.set
            self.ui.AnalysisPlot1.addItem(current_line)
            #self.ui.plot11.setData(self.peak_positions[])
        
        slope_line = pq.PlotDataItem(self.corrScanValues,slope,symbol = 'o')
        self.ui.AnalysisPlot2.addItem(slope_line)
        #self.ui.plot21.setData(self.corrData,slope)      
        coeff, var_matrix = curve_fit(self.lin_func, self.corrScanValues, slope, [3, 3], maxfev = 10000)
        fit_x_values = np.linspace(np.min(self.corrScanValues),np.max(self.corrScanValues),25)
        
        fit_curve = pq.PlotDataItem(fit_x_values, coeff[0]*fit_x_values+coeff[1], pen = 'r', style=QtCore.Qt.DashLine)
        self.ui.AnalysisPlot2.addItem(fit_curve)
        
        
        self.corrected_corrector_value = -coeff[1]/coeff[0]
        print self.corrected_corrector_value    
        
        self.cameraTimer = True
                    
    def cameraStop(self):
        self.cameraDevice.stop()
        
    def cameraStart(self):
         self.cameraDevice.start()
         sleep(2)
         self.cameraDevice.startacquisition()   
        
    def closeEvent(self, event):
        self.stop_timer = True
        self.deleteLater()
        time.sleep(0.1)
        print 'stopping'
        
   
if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    #app.processEvents()
    myapp = QuadCentering()
    myapp.show()
    #splash.finish(myapp)
    sys.exit(app.exec_())

