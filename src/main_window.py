from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
import sys
sys.path.append(".")
from styler import Styler

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
  
        self.settingsFrame = QtWidgets.QFrame(self)
        self.addShadow(self.settingsFrame)
        self.settingsFrame.setStyleSheet(self.styler.roundedStyle)

    def createPlottingAreaWidget(self): 
  
        self.plottingAreaFrame = QtWidgets.QFrame(self)
        self.addShadow(self.plottingAreaFrame)
        self.plottingAreaFrame.setStyleSheet(self.styler.roundedStyle)

    def manageLayouts(self):

        mainLayout = QtWidgets.QVBoxLayout()
        mainLayout.setContentsMargins(10,10,10,10)
        mainLayout.setSpacing(10)
        mainLayout.addWidget(self.settingsFrame,1)
        mainLayout.addWidget(self.plottingAreaFrame,4)

        mainFrame = QtWidgets.QFrame(self)
        mainFrame.setLayout(mainLayout)
        self.setCentralWidget(mainFrame)
        

    def addShadow(self, widget):
        
        effect = QtWidgets.QGraphicsDropShadowEffect()
        effect.setBlurRadius(8)
        effect.setXOffset(0)
        effect.setYOffset(0)
        effect.setColor(QColor(65,88,134))
        widget.setGraphicsEffect(effect);  
