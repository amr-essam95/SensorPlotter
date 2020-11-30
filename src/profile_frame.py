from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
import sys
sys.path.append(".")
from styler import Styler

class ProfileFrame(QtWidgets.QFrame): 
    def __init__(self, parent=None): 
        super().__init__(parent)

        self.profileButtonsFrame = ""
        self.profilePlotFrame = ""

        self.styler = Styler()

        self.createProfileButtons()
        self.createProfilePlot()
        self.manageLayouts()

    def createProfileButtons(self):

        profileButtonsLayout = QtWidgets.QVBoxLayout()
        
        self.profileButtonsFrame = QtWidgets.QFrame()
        self.profileButtonsFrame.setLayout(profileButtonsLayout)

    def createProfilePlot(self):
        
        profilePlotLayout = QtWidgets.QVBoxLayout()

        self.profilePlotFrame = QtWidgets.QFrame()
        self.profilePlotFrame.setLayout(profilePlotLayout)

    def manageLayouts(self):
        
        mainLayout = QtWidgets.QHBoxLayout()
        mainLayout.setContentsMargins(2,2,2,2)
        mainLayout.setSpacing(10)
        mainLayout.addWidget(self.profileButtonsFrame, 1)
        mainLayout.addWidget(self.profilePlotFrame, 2)
        self.setLayout(mainLayout)