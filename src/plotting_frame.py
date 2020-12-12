from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
import sys
sys.path.append(".")
from styler import Styler

from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg

class PlottingFrame(QtWidgets.QFrame): 
	def __init__(self, socketController, parent=None): 
		super().__init__()

		self.anglePlotsFrame = ""
		self.analogPlotsFrame = ""
		self.buttonsFrame = ""
		self.enableButton = ""
		self.syncButton = ""
		self.userButton = ""
		self.syncFrame = ""
		self.userFrame = ""
		self.enableLabel = ""

		self.enableState = 0

		self.removeFirstElement = False

		self.time = []

		self.thighPlot = ""
		self.rtLine = ""
		self.rtData = []
		self.ltLine = ""
		self.ltData = []
		self.trLine = ""
		self.trData = []

		self.shankPlot = ""
		self.rsLine = ""
		self.rsData = []
		self.lsLine = ""
		self.lsData = []

		self.currentPlot = ""
		self.rmReadoutLine = ""
		self.rmRData = []
		self.lmReadoutLine = ""
		self.lmRData = []
		self.rmSentLine = ""
		self.rmSData = []
		self.lmSentLine = ""
		self.lmSData = []

		self.analog0Plot = ""
		self.analogLine0 = ""
		self.analog0Data = []
		
		self.analog1Plot = ""
		self.analogLine1 = ""
		self.analog1Data = []

		self.analog2Plot = ""
		self.analogLine2 = ""
		self.analog2Data = []

		self.analog3Plot = ""
		self.analogLine3 = ""
		self.analog3Data = []

		self.styler = Styler()

		self.socketController = socketController

		self.socketController.socketCommunicator.labelDataReady.connect(self.onLabelDataReady)

		self.createAnglePlotsFrame()
		self.createAnalogPlotsFrame()
		self.createButtonsFrame()
		self.manageLayouts()

	def createAnglePlotsFrame(self):

		self.createThighPlot()
		self.createShankPlot()
		self.createCurrentPlot()

		anglePlotsLayout = QtWidgets.QVBoxLayout()
		anglePlotsLayout.setContentsMargins(5,5,10,5)
		anglePlotsLayout.setSpacing(0)
		anglePlotsLayout.addWidget(self.thighPlot)
		anglePlotsLayout.addWidget(self.shankPlot)
		anglePlotsLayout.addWidget(self.currentPlot)

		self.anglePlotsFrame = QtWidgets.QFrame()
		self.styler.addShadow(self.anglePlotsFrame)
		self.anglePlotsFrame.setLayout(anglePlotsLayout)

	def createAnalogPlotsFrame(self):

		self.createAnalog0Plot()
		self.createAnalog1Plot()
		self.createAnalog2Plot()
		self.createAnalog3Plot()

		analogPlotsLayout = QtWidgets.QVBoxLayout()
		analogPlotsLayout.setContentsMargins(5,5,10,5)
		analogPlotsLayout.setSpacing(0)
		analogPlotsLayout.addWidget(self.analog0Plot)
		analogPlotsLayout.addWidget(self.analog1Plot)
		analogPlotsLayout.addWidget(self.analog2Plot)
		analogPlotsLayout.addWidget(self.analog3Plot)

		self.analogPlotsFrame = QtWidgets.QFrame()
		self.styler.addShadow(self.analogPlotsFrame)
		self.analogPlotsFrame.setLayout(analogPlotsLayout)

	def createButtonsFrame(self):

		self.enableLabel = QtWidgets.QPushButton("Enable")
		self.enableLabel.setStyleSheet(self.styler.enableLabel)
		self.enableLabel.clicked.connect(self.onEnableButtonClicked)

		self.enableButton = QtWidgets.QPushButton()
		self.enableButton.setToolTip("Enable")
		self.enableButton.setStyleSheet(self.styler.enableButtonStyle)
		self.enableButton.setIconSize(QtCore.QSize(70,70))
		self.enableButton.clicked.connect(self.onEnableButtonClicked)

		enableButtonLayout = QtWidgets.QVBoxLayout()
		enableButtonLayout.setSpacing(5)
		enableButtonLayout.setContentsMargins(0,0,0,0)
		enableButtonLayout.addWidget(self.enableButton)
		enableButtonLayout.addWidget(self.enableLabel)

		enableButtonFrame = QtWidgets.QFrame()
		enableButtonFrame.setLayout(enableButtonLayout)

		self.syncLabel = QtWidgets.QLabel("SYNC")
		self.syncLabel.setStyleSheet(self.styler.labelOffStyle)
		self.syncLabel.setAlignment(QtCore.Qt.AlignCenter)

		syncLayout = QtWidgets.QHBoxLayout()
		syncLayout.addWidget(self.syncLabel, QtCore.Qt.AlignCenter)

		self.syncFrame = QtWidgets.QFrame()
		self.syncFrame.setStyleSheet(self.styler.labelFrameOffStyle)
		self.syncFrame.setFixedSize(QtCore.QSize(80,80))
		self.syncFrame.setLayout(syncLayout)

		self.userLabel = QtWidgets.QLabel("USR")
		self.userLabel.setStyleSheet(self.styler.labelOffStyle)
		self.userLabel.setAlignment(QtCore.Qt.AlignCenter)

		userLayout = QtWidgets.QHBoxLayout()
		userLayout.addWidget(self.userLabel, QtCore.Qt.AlignCenter)

		self.userFrame = QtWidgets.QFrame()
		self.userFrame.setStyleSheet(self.styler.labelFrameOffStyle)
		self.userFrame.setFixedSize(QtCore.QSize(80,80))
		self.userFrame.setLayout(userLayout)

		buttonsLayout = QtWidgets.QVBoxLayout()
		buttonsLayout.setContentsMargins(20,20,20,20)
		buttonsLayout.setAlignment(QtCore.Qt.AlignHCenter)
		buttonsLayout.addWidget(enableButtonFrame, 0, QtCore.Qt.AlignTop)
		buttonsLayout.addWidget(self.syncFrame)
		buttonsLayout.addWidget(self.userFrame, 0, QtCore.Qt.AlignBottom)

		self.buttonsFrame = QtWidgets.QFrame()
		self.buttonsFrame.setLayout(buttonsLayout)
		self.styler.addShadow(self.buttonsFrame)

	def createPlot(self, title, xLabel, yLabel):

		plot = pg.PlotWidget()

		blackColor = (0,0,0)

		plot.setBackground('w')
		plot.setTitle("<span style=\"color:black; font-size:15pt\">{}</span>".format(title))

		styles = {'color':'rgba(0,0,0,1)', 'font-size':'15px'}
		plot.getAxis('left').setPen(color=blackColor)
		plot.getAxis('bottom').setPen(color=blackColor)

		plot.getAxis('left').setTextPen(color=blackColor)
		plot.getAxis('bottom').setTextPen(color=blackColor) 

		plot.setLabel('left', xLabel, **styles)
		plot.setLabel('bottom', yLabel, **styles)

		plot.setContentsMargins(0,0,0,0)

		return plot

	def createThighPlot(self):

		self.thighPlot = self.createPlot('', 'Thigh (deg)', '')
		self.rtLine = self.thighPlot.plot([], [], "RT_AFlt", pen = self.styler.blackPen)
		self.ltLine = self.thighPlot.plot([], [], "LT_AFlt", pen = self.styler.bluePen)
		self.trLine = self.thighPlot.plot([], [], "Tr_AFlt", pen = self.styler.redPen)

	def createShankPlot(self):

		self.shankPlot = self.createPlot('', 'Shank (deg)', '')
		self.rsLine = self.shankPlot.plot([], [], "RS_AFlt", pen = self.styler.blackPen)
		self.lsLine = self.shankPlot.plot([], [], "LS_AFlt", pen = self.styler.bluePen)

	def createCurrentPlot(self):

		self.currentPlot = self.createPlot('', 'Current (mA)', 'Time (S)')
		self.rmReadoutLine = self.currentPlot.plot([], [], "RM_CurR", pen = self.styler.blackPen)
		self.lmReadoutLine = self.currentPlot.plot([], [], "LM_CurR", pen = self.styler.blackDottedPen)
		self.rmSentLine = self.currentPlot.plot([], [], "RM_CurS", pen = self.styler.bluePen)
		self.lmSentLine = self.currentPlot.plot([], [], "LM_CurS", pen = self.styler.blueDottedPen)

	def createAnalog0Plot(self):

		self.analog0Plot = self.createPlot('', 'Ch0 (mV)', '')
		self.analogLine0 = self.analog0Plot.plot([], [], "Analog 0", pen = self.styler.blackPen)

	def createAnalog1Plot(self):

		self.analog1Plot = self.createPlot('', 'Ch1 (mV)', '')
		self.analogLine1 = self.analog1Plot.plot([], [], "Analog 1", pen = self.styler.blackPen)

	def createAnalog2Plot(self):

		self.analog2Plot = self.createPlot('', 'Ch2 (mV)', '')
		self.analogLine2 = self.analog2Plot.plot([], [], "Analog 2", pen = self.styler.blackPen)

	def createAnalog3Plot(self):

		self.analog3Plot = self.createPlot('', 'Ch3 (mV)', 'Time (S)')
		self.analogLine3 = self.analog3Plot.plot([], [], "Analog 3", pen = self.styler.blackPen)

	def manageLayouts(self):
		
		mainLayout = QtWidgets.QHBoxLayout()
		mainLayout.setContentsMargins(2,2,2,2)
		mainLayout.setSpacing(10)
		mainLayout.addWidget(self.anglePlotsFrame, 2)
		mainLayout.addWidget(self.buttonsFrame, 1)
		mainLayout.addWidget(self.analogPlotsFrame, 2)

		self.setLayout(mainLayout)

	# Slots

	def onEnableButtonClicked(self):
		
		if self.enableState == 0:
			self.enableState = 1
			self.enableLabel.setText("Disable")
			self.socketController.enableStateChanged(self.enableState)
		else:
			self.enableState = 0
			self.enableLabel.setText("Enable")
			self.socketController.enableStateChanged(self.enableState)

	def setSyncLabelState(self, state):

		if state == True:
			self.syncLabel.setStyleSheet(self.styler.labelOnStyle)
			self.syncFrame.setStyleSheet(self.styler.labelFrameOnStyle)
		else:
			self.syncLabel.setStyleSheet(self.styler.labelOffStyle)
			self.syncFrame.setStyleSheet(self.styler.labelFrameOffStyle)

	def setUserLabelState(self, state):

		if state == True:
			self.userLabel.setStyleSheet(self.styler.labelOnStyle)
			self.userFrame.setStyleSheet(self.styler.labelFrameOnStyle)
		else:
			self.userLabel.setStyleSheet(self.styler.labelOffStyle)
			self.userFrame.setStyleSheet(self.styler.labelFrameOffStyle)

	def onLabelDataReady(self, syncIn, userBtn):
		
		self.setSyncLabelState(syncIn)
		self.setUserLabelState(userBtn)