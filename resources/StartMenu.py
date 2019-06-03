import sys

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSlot, QObject, QRegExp
from PyQt5.QtWidgets import QApplication, QDialog, QMainWindow, QMessageBox, QFileDialog
from PyQt5.uic import loadUi

class StartMenu(QtWidgets):

    def __init__(self):

        super(StartMenu, self).__init__()
        loadUi('StartMenu.ui', self)
        self.model = Model()
        self.setStyleSheet('QWidget{background-color: #F6F7EB;border: #393E41;}')


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


app = QtWidgets(sys.argv)
widget = CarRecognitionCounting()
widget.show()
sys.exit(app.exec_())

    

    
