from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
import sys
sys.path.append(".")
from styler import Styler
from settings_frame import SettingsFrame
from plotting_frame import PlottingFrame

class MainWindow(QtWidgets.QMainWindow): 
    def __init__(self): 
        super().__init__() 

        self.settingsFrame = ""
        self.plottingAreaFrame = ""
        
        self.styler = Styler()
  
        # setting title 
        self.setWindowTitle("Sensor Plotter") 
  
        # Creating widgets. 
        self.createSettingsFrame()
        self.createPlottingAreaWidget()

        self.manageLayouts()
  
        # showing all the widgets 
        self.showMaximized()
  
    def createSettingsFrame(self): 
  
        self.settingsFrame = SettingsFrame(self)
        self.settingsFrame.setStyleSheet(self.styler.roundedStyle)

    def createPlottingAreaWidget(self): 
  
        self.plottingAreaFrame = PlottingFrame()
        self.plottingAreaFrame.setStyleSheet(self.styler.roundedStyle)

    def manageLayouts(self):

        mainLayout = QtWidgets.QVBoxLayout()
        mainLayout.setContentsMargins(10,10,10,10)
        mainLayout.setSpacing(10)
        mainLayout.addWidget(self.settingsFrame,2)
        mainLayout.addWidget(self.plottingAreaFrame,5)

        mainFrame = QtWidgets.QFrame(self)
        mainFrame.setLayout(mainLayout)
        self.setCentralWidget(mainFrame)