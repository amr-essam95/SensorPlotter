from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor

class MainWindow(QtWidgets.QMainWindow): 
    def __init__(self): 
        super().__init__() 

        self.settingsFrame = ""
        self.plottingAreaFrame = ""
  
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

    def createPlottingAreaWidget(self): 
  
        self.plottingAreaFrame = QtWidgets.QFrame(self)
        self.addShadow(self.plottingAreaFrame)

    def manageLayouts(self):

        mainLayout = QtWidgets.QVBoxLayout()
        mainLayout.setContentsMargins(10,10,10,10)
        mainLayout.addWidget(self.settingsFrame,1)
        mainLayout.addWidget(self.plottingAreaFrame,3)

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
