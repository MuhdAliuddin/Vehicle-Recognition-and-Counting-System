import sys

# Object detection imports
import tensorflow as tf
from utils import backbone
from api import openCV_api

# GUI imports
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSlot, QObject, QRegExp
from PyQt5.QtWidgets import QApplication, QDialog, QMainWindow, QMessageBox, QFileDialog
from PyQt5.QtGui import QRegExpValidator
from PyQt5.uic import loadUi
from model import Model
from csvreader import MyWindow


class CarRecognitionCounting(QMainWindow):

    def __init__(self):
        
        super(CarRecognitionCounting, self).__init__()
        self.model = Model()
        loadUi('MainScreen.ui', self)

        self.setStyleSheet('QMainWindow{background-color: #F6F7EB;border: #393E41;}')

        
        self.runButton.clicked.connect(self.runAPI)
        self.browseButton.clicked.connect(self.inputVideo)
        self.outputButton.clicked.connect(self.outputFile)
        self.vidoutputButton.clicked.connect(self.outputVidFile)

    def refreshAll( self ):
        
        '''
        Updates the widgets whenever an interaction happens.
        '''
        
        self.edit_input_video.setText( self.model.getFileName() )

    def runAPI(self):

        '''
        Function when runButton is pressed
        Enters value of visde fps, height and width
        Runs object_detection_api
        '''

        #detection graph and load model
        detection_graph, category_index = backbone.set_model('ssd_mobilenet_v1_coco_2018_01_28')
        is_color_recognition_enabled = 0 # set it to 1 for enabling the color prediction for the detected objects
        roi = 200
        deviation = 3
        
        fpsInput = self.edit_fps_value.text()
        heightInput = self.edit_height_val.text()
        widthInput = self.edit_width_val.text()

        fps = int(round(float(fpsInput)))
        height = int(round(float(heightInput)))
        width = int(round(float(widthInput)))

        input_video = self.model.getFileName()

        # Object detetction and counting
        openCV_api.cumulative_object_counting_y_axis(input_video, detection_graph, category_index, is_color_recognition_enabled, fps, width, height, roi, deviation)

        QMessageBox.about(self, "System Message", "Input video detection complete. Check video output and .csv output for results.")
        

    def inputVideo(self):

        '''Opens new window to select video location
           Receives and store video input location as string'''

        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(
                        None,
                        "QFileDialog.getOpenFileName()",
                        "",
                        "All Files (*);;Python Files (*.py)",
                        options=options)
        
        if fileName:
            self.model.setFileName( fileName )
            self.refreshAll()
            

    def outputFile(self):
        '''
        Function when outputButton is pressed
        Opens new csvReader in new window
        '''

        self.csvReader = MyWindow(self)
        self.csvReader.show()
        

    def outputVidFile(self):

        '''Opens new window to select video location
        Receives and store video input location as string'''
        
        
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        vidfileName, _ = QtWidgets.QFileDialog.getOpenFileName(
                        None,
                        "QFileDialog.getOpenFileName()",
                        "",
                        "All Files (*);;Python Files (*.mp4)",
                        options=options)
                        
        if vidfileName:
            self.model.setFileName( vidfileName )
            openCV_api.play_video(vidfileName)
            
        

    # Exception hook
    sys._excepthook = sys.excepthook
    def application_exception_hook(exctype, value, traceback):

        '''
        Error exception handling
        '''
        
        print(exctype, value, traceback)
        sys._excepthook(exctype, value, traceback)
        sys.exit(1)

    # Exception hook
    sys.excepthook = application_exception_hook
        



app = QApplication(sys.argv)
widget = CarRecognitionCounting()
widget.show()
sys.exit(app.exec_())
    


