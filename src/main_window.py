from PyQt5.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QMainWindow

import sys
sys.path.append(".")
from styler import Styler
from settings_frame import SettingsFrame
from plotting_frame import PlottingFrame
from socket_controller import SocketController

class MainWindow(QMainWindow): 
    def __init__(self): 
        super().__init__() 

        self.settingsFrame = ""
        self.plottingAreaFrame = ""
        
        self.styler = Styler()

        self.socketController = SocketController(self)
  
        # setting title 
        self.setWindowTitle("myoswiss")

        self.setStyleSheet("background-color: white")
  
        # Creating widgets. 
        self.createSettingsFrame()
        self.createPlottingAreaWidget()

        self.connectPlotter()

        self.manageLayouts()
  
        # showing all the widgets
        self.showMaximized()
  
    def createSettingsFrame(self): 
  
        self.settingsFrame = SettingsFrame(self.socketController, self)
        self.settingsFrame.setStyleSheet(self.styler.roundedStyle)

    def createPlottingAreaWidget(self): 
  
        self.plottingAreaFrame = PlottingFrame(self.socketController)
        self.plottingAreaFrame.setStyleSheet(self.styler.roundedStyle)

    def manageLayouts(self):

        mainLayout = QVBoxLayout()
        mainLayout.setContentsMargins(10,10,10,10)
        mainLayout.setSpacing(10)
        mainLayout.addWidget(self.settingsFrame,2)
        mainLayout.addWidget(self.plottingAreaFrame,5)

        mainFrame = QFrame(self)
        mainFrame.setLayout(mainLayout)
        self.setCentralWidget(mainFrame)

    def connectPlotter(self):

        self.socketController.plotUpdater.rtLine = self.plottingAreaFrame.rtLine
        self.socketController.plotUpdater.ltLine = self.plottingAreaFrame.ltLine
        self.socketController.plotUpdater.trLine = self.plottingAreaFrame.trLine
        self.socketController.plotUpdater.rsLine = self.plottingAreaFrame.rsLine
        self.socketController.plotUpdater.lsLine = self.plottingAreaFrame.lsLine
        self.socketController.plotUpdater.rmReadoutLine = self.plottingAreaFrame.rmReadoutLine
        self.socketController.plotUpdater.lmReadoutLine = self.plottingAreaFrame.lmReadoutLine
        self.socketController.plotUpdater.rmSentLine = self.plottingAreaFrame.rmSentLine
        self.socketController.plotUpdater.lmSentLine = self.plottingAreaFrame.lmSentLine
        self.socketController.plotUpdater.analogLine0 = self.plottingAreaFrame.analogLine0
        self.socketController.plotUpdater.analogLine1 = self.plottingAreaFrame.analogLine1
        self.socketController.plotUpdater.analogLine2 = self.plottingAreaFrame.analogLine2
        self.socketController.plotUpdater.analogLine3 = self.plottingAreaFrame.analogLine3