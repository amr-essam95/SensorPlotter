from PyQt5.QtWidgets import QFrame, QPushButton, QVBoxLayout, QHBoxLayout, QLabel
from PyQt5.QtCore import Qt, QSize

import sys
sys.path.append(".")
from styler import Styler

from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg

class PlottingFrame(QFrame): 
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
		self.legendLayout = ""

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
	
	def createAnglePlotsLegend(self):

		rxBox = QFrame()
		rxBox.setStyleSheet(self.styler.rxLegendBox)
		rxBox.setFixedSize(QSize(15,15))

		rxLabel = QLabel("RX")
		rxLabel.setStyleSheet(self.styler.rxLegendLabel)

		rxLegendLayout = QHBoxLayout()
		rxLegendLayout.setSpacing(10)
		rxLegendLayout.addWidget(rxBox)
		rxLegendLayout.addWidget(rxLabel)
		rxLegendLayout.setContentsMargins(5,5,5,5)

		lxBox = QFrame()
		lxBox.setStyleSheet(self.styler.lxLegendBox)
		lxBox.setFixedSize(QSize(15,15))

		lxLabel = QLabel("LX")
		lxLabel.setStyleSheet(self.styler.lxLegendLabel)

		lxLegendLayout = QHBoxLayout()
		lxLegendLayout.setSpacing(10)
		lxLegendLayout.addWidget(lxBox)
		lxLegendLayout.addWidget(lxLabel)
		lxLegendLayout.setContentsMargins(0,0,0,0)

		trunkBox = QFrame()
		trunkBox.setStyleSheet(self.styler.trunkLegendBox)
		trunkBox.setFixedSize(QSize(15,15))

		trunkLabel = QLabel("Trunk")
		trunkLabel.setStyleSheet(self.styler.trunkLegendLabel)

		trunkLegendLayout = QHBoxLayout()
		trunkLegendLayout.setSpacing(10)
		trunkLegendLayout.addWidget(trunkBox)
		trunkLegendLayout.addWidget(trunkLabel)
		trunkLegendLayout.setContentsMargins(0,0,0,0)

		self.legendLayout = QHBoxLayout()
		self.legendLayout.setSpacing(20)
		self.legendLayout.addLayout(rxLegendLayout)
		self.legendLayout.addLayout(lxLegendLayout)
		self.legendLayout.addLayout(trunkLegendLayout)
		self.legendLayout.setAlignment(Qt.AlignHCenter)
		self.legendLayout.setContentsMargins(2,2,2,2)

	def createAnglePlotsFrame(self):

		self.createAnglePlotsLegend()
		self.createThighPlot()
		self.createShankPlot()
		self.createCurrentPlot()

		anglePlotsLayout = QVBoxLayout()
		anglePlotsLayout.setContentsMargins(5,5,10,5)
		anglePlotsLayout.setSpacing(0)
		anglePlotsLayout.addLayout(self.legendLayout)
		anglePlotsLayout.addWidget(self.thighPlot)
		anglePlotsLayout.addWidget(self.shankPlot)
		anglePlotsLayout.addWidget(self.currentPlot)

		self.anglePlotsFrame = QFrame()
		self.styler.addShadow(self.anglePlotsFrame)
		self.anglePlotsFrame.setLayout(anglePlotsLayout)

	def createAnalogPlotsFrame(self):

		self.createAnalog0Plot()
		self.createAnalog1Plot()
		self.createAnalog2Plot()
		self.createAnalog3Plot()

		analogPlotsLayout = QVBoxLayout()
		analogPlotsLayout.setContentsMargins(5,5,10,5)
		analogPlotsLayout.setSpacing(0)
		analogPlotsLayout.addWidget(self.analog0Plot)
		analogPlotsLayout.addWidget(self.analog1Plot)
		analogPlotsLayout.addWidget(self.analog2Plot)
		analogPlotsLayout.addWidget(self.analog3Plot)

		self.analogPlotsFrame = QFrame()
		self.styler.addShadow(self.analogPlotsFrame)
		self.analogPlotsFrame.setLayout(analogPlotsLayout)

	def createButtonsFrame(self):

		self.enableLabel = QPushButton("Enable")
		self.enableLabel.setStyleSheet(self.styler.enableLabel)
		self.enableLabel.clicked.connect(self.onEnableButtonClicked)

		self.enableButton = QPushButton()
		self.enableButton.setToolTip("Enable")
		self.enableButton.setStyleSheet(self.styler.enableButtonStyle)
		self.enableButton.setIconSize(QSize(70,70))
		self.enableButton.clicked.connect(self.onEnableButtonClicked)

		enableButtonLayout = QVBoxLayout()
		enableButtonLayout.setSpacing(5)
		enableButtonLayout.setContentsMargins(0,0,0,0)
		enableButtonLayout.addWidget(self.enableButton)
		enableButtonLayout.addWidget(self.enableLabel)

		enableButtonFrame = QFrame()
		enableButtonFrame.setLayout(enableButtonLayout)

		self.syncLabel = QLabel("SYNC")
		self.syncLabel.setStyleSheet(self.styler.labelOffStyle)
		self.syncLabel.setAlignment(Qt.AlignCenter)

		syncLayout = QHBoxLayout()
		syncLayout.addWidget(self.syncLabel, Qt.AlignCenter)

		self.syncFrame = QFrame()
		self.syncFrame.setStyleSheet(self.styler.labelFrameOffStyle)
		self.syncFrame.setFixedSize(QSize(80,80))
		self.syncFrame.setLayout(syncLayout)

		self.userLabel = QLabel("USR")
		self.userLabel.setStyleSheet(self.styler.labelOffStyle)
		self.userLabel.setAlignment(Qt.AlignCenter)

		userLayout = QHBoxLayout()
		userLayout.addWidget(self.userLabel, Qt.AlignCenter)

		self.userFrame = QFrame()
		self.userFrame.setStyleSheet(self.styler.labelFrameOffStyle)
		self.userFrame.setFixedSize(QSize(80,80))
		self.userFrame.setLayout(userLayout)

		buttonsLayout = QVBoxLayout()
		buttonsLayout.setContentsMargins(20,20,20,20)
		buttonsLayout.setAlignment(Qt.AlignHCenter)
		buttonsLayout.addWidget(enableButtonFrame, 0, Qt.AlignTop)
		buttonsLayout.addWidget(self.syncFrame)
		buttonsLayout.addWidget(self.userFrame, 0, Qt.AlignBottom)

		self.buttonsFrame = QFrame()
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
		self.rtLine = self.thighPlot.plot([], [], "RT_AFlt", pen = self.styler.blackPen, name = "RX")
		self.ltLine = self.thighPlot.plot([], [], "LT_AFlt", pen = self.styler.bluePen, name = "LX")
		self.trLine = self.thighPlot.plot([], [], "Tr_AFlt", pen = self.styler.redPen, name = "Trunk")

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
		
		mainLayout = QHBoxLayout()
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