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
		self.runButton = ""
		self.syncButton = ""
		self.userButton = ""
		self.syncFrame = ""
		self.userFrame = ""

		self.thighPlot = ""
		self.shankPlot = ""
		self.currentPlot = ""

		self.analog0Plot = ""
		self.analog1Plot = ""
		self.analog2Plot = ""
		self.analog3Plot = ""

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
		anglePlotsLayout.setContentsMargins(10,10,10,10)
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
		analogPlotsLayout.setContentsMargins(10,10,10,10)
		analogPlotsLayout.setSpacing(0)
		analogPlotsLayout.addWidget(self.analog0Plot)
		analogPlotsLayout.addWidget(self.analog1Plot)
		analogPlotsLayout.addWidget(self.analog2Plot)
		analogPlotsLayout.addWidget(self.analog3Plot)

		self.analogPlotsFrame = QtWidgets.QFrame()
		self.styler.addShadow(self.analogPlotsFrame)
		self.analogPlotsFrame.setLayout(analogPlotsLayout)

	def createButtonsFrame(self):

		self.runButton = QtWidgets.QPushButton()
		self.runButton.setStyleSheet(self.styler.playButtonStyle)
		self.runButton.setIconSize(QtCore.QSize(70,70))
		self.runButton.clicked.connect(self.onRunButtonClicked)

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
		buttonsLayout.addWidget(self.runButton, 0, QtCore.Qt.AlignTop)
		buttonsLayout.addWidget(self.syncFrame)
		buttonsLayout.addWidget(self.userFrame, 0, QtCore.Qt.AlignBottom)

		self.buttonsFrame = QtWidgets.QFrame()
		self.buttonsFrame.setLayout(buttonsLayout)
		self.styler.addShadow(self.buttonsFrame)

	def createPlot(self, title, xLabel, yLabel):

		plot = pg.PlotWidget()

		blackColor = (0,0,0)

		plot.setBackground('w')
		plot.setTitle("<span style=\"color:black; font-size:30==40pt\">{}</span>".format(title))

		styles = {'color':'rgba(0,0,0,1)', 'font-size':'15px'}
		plot.getAxis('left').setPen(color=blackColor)
		plot.getAxis('bottom').setPen(color=blackColor)

		plot.getAxis('left').setTextPen(color=blackColor)
		plot.getAxis('bottom').setTextPen(color=blackColor) 

		plot.setLabel('left', xLabel, **styles)
		plot.setLabel('bottom', yLabel, **styles)

		return plot

	def createThighPlot(self):
		
		self.thighPlot = self.createPlot('Thigh Plot', 'Thigh (deg)', 'Time (S)')

	def createShankPlot(self):

		self.shankPlot = self.createPlot('Shank Plot', 'Shank (deg)', 'Time (S)')

	def createCurrentPlot(self):

		self.currentPlot = self.createPlot('Current Plot', 'Current (deg)', 'Time (S)')

	def createAnalog0Plot(self):

		self.analog0Plot = self.createPlot('Analog 0', 'Ch0 (mV)', 'Time (S)')

	def createAnalog1Plot(self):

		self.analog1Plot = self.createPlot('Analog 1', 'Ch1 (mV)', 'Time (S)')

	def createAnalog2Plot(self):

		self.analog2Plot = self.createPlot('Analog 2', 'Ch2 (mV)', 'Time (S)')

	def createAnalog3Plot(self):

		self.analog3Plot = self.createPlot('Analog 3', 'Ch3 (mV)', 'Time (S)')

	def manageLayouts(self):
		
		mainLayout = QtWidgets.QHBoxLayout()
		mainLayout.setContentsMargins(2,2,2,2)
		mainLayout.setSpacing(10)
		mainLayout.addWidget(self.anglePlotsFrame, 2)
		mainLayout.addWidget(self.buttonsFrame, 1)
		mainLayout.addWidget(self.analogPlotsFrame, 2)

		self.setLayout(mainLayout)


	# Slots

	def onRunButtonClicked(self):
		
		self.runButton.clicked.disconnect(self.onRunButtonClicked)
		self.runButton.setStyleSheet(self.styler.pauseButtonStyle)
		self.runButton.clicked.connect(self.onPauseButtonClicked)
		self.socketController.enableStateChanged(1)

	def onPauseButtonClicked(self):

		self.runButton.clicked.disconnect(self.onPauseButtonClicked)
		self.runButton.setStyleSheet(self.styler.playButtonStyle)
		self.runButton.clicked.connect(self.onRunButtonClicked)
		self.socketController.enableStateChanged(0)

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
