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
		self.socketController.socketCommunicator.thighDataReady.connect(self.onThighDataReady)
		self.socketController.socketCommunicator.shankDataReady.connect(self.onShankDataReady)
		self.socketController.socketCommunicator.currentDataReady.connect(self.onCurrentDataReady)
		self.socketController.socketCommunicator.analog0DataReady.connect(self.onAnalog0DataReady)
		self.socketController.socketCommunicator.analog1DataReady.connect(self.onAnalog1DataReady)
		self.socketController.socketCommunicator.analog2DataReady.connect(self.onAnalog2DataReady)
		self.socketController.socketCommunicator.analog3DataReady.connect(self.onAnalog3DataReady)

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
		plot.setTitle("<span style=\"color:black; font-size:15pt\">{}</span>".format(title))

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
		self.rtLine = self.thighPlot.plot([], [], "RT_AFlt", pen = self.styler.blackPen)
		self.ltLine = self.thighPlot.plot([], [], "LT_AFlt", pen = self.styler.bluePen)
		self.trLine = self.thighPlot.plot([], [], "Tr_AFlt", pen = self.styler.redPen)

	def createShankPlot(self):

		self.shankPlot = self.createPlot('Shank Plot', 'Shank (deg)', 'Time (S)')
		self.rsLine = self.shankPlot.plot([], [], "RS_AFlt", pen = self.styler.blackPen)
		self.lsLine = self.shankPlot.plot([], [], "LS_AFlt", pen = self.styler.bluePen)

	def createCurrentPlot(self):

		self.currentPlot = self.createPlot('Current Plot', 'Current (deg)', 'Time (S)')
		self.rmReadoutLine = self.currentPlot.plot([], [], "RM_CurR", pen = self.styler.blackPen)
		self.lmReadoutLine = self.currentPlot.plot([], [], "LM_CurR", pen = self.styler.blackDottedPen)
		self.rmSentLine = self.currentPlot.plot([], [], "RM_CurS", pen = self.styler.bluePen)
		self.lmSentLine = self.currentPlot.plot([], [], "LM_CurS", pen = self.styler.blueDottedPen)

	def createAnalog0Plot(self):

		self.analog0Plot = self.createPlot('Analog 0', 'Ch0 (mV)', 'Time (S)')
		self.analogLine0 = self.analog0Plot.plot([], [], "Analog 0", pen = self.styler.blackPen)

	def createAnalog1Plot(self):

		self.analog1Plot = self.createPlot('Analog 1', 'Ch1 (mV)', 'Time (S)')
		self.analogLine1 = self.analog1Plot.plot([], [], "Analog 1", pen = self.styler.blackPen)

	def createAnalog2Plot(self):

		self.analog2Plot = self.createPlot('Analog 2', 'Ch2 (mV)', 'Time (S)')
		self.analogLine2 = self.analog2Plot.plot([], [], "Analog 2", pen = self.styler.blackPen)

	def createAnalog3Plot(self):

		self.analog3Plot = self.createPlot('Analog 3', 'Ch3 (mV)', 'Time (S)')
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

	def onThighDataReady(self, time, rt, lt, tr):

		if (len(self.time) > 20):
			self.removeFirstElement = True
		if (self.removeFirstElement):
			self.time = self.time[1:]
			self.rtData = self.rtData[1:]
			self.ltData = self.ltData[1:]
			self.trData = self.trData[1:]

		self.time.append(time)
		self.rtData.append(rt * 0.001)
		self.ltData.append(lt * 0.001)
		self.trData.append(tr * 0.001)

		self.rtLine.setData(self.time, self.rtData)
		self.ltLine.setData(self.time, self.ltData)
		self.trLine.setData(self.time, self.trData)

	def onShankDataReady(self, time, rs, ls):

		if (self.removeFirstElement):
			self.rsData = self.rsData[1:]
			self.lsData = self.lsData[1:]

		self.rsData.append(rs * 0.001)
		self.lsData.append(ls * 0.001)

		self.rsLine.setData(self.time, self.rsData)
		self.lsLine.setData(self.time, self.lsData)

	def onCurrentDataReady(self, time, rmR, lmR, rmS, lmS):

		if (self.removeFirstElement):
			self.rmRData = self.rmRData[1:]
			self.lmRData = self.lmRData[1:]
			self.rmSData = self.rmSData[1:]
			self.lmSData = self.lmSData[1:]

		self.rmRData.append(rmR * 0.001)
		self.lmRData.append(lmR * 0.001)
		self.rmSData.append(rmS * 0.001)
		self.lmSData.append(lmS * 0.001)

		self.rmReadoutLine.setData(self.time, self.rmRData)
		self.lmReadoutLine.setData(self.time, self.lmRData)
		self.rmSentLine.setData(self.time, self.rmSData)
		self.lmSentLine.setData(self.time, self.lmSData)

	def onAnalog0DataReady(self, analog0):

		if (self.removeFirstElement):
			self.rmRanalog0DataData = self.analog0Data[1:]

		self.analog0Data.append(analog0)
		self.analogLine0.setData(self.time, self.analog0Data)

	def onAnalog1DataReady(self, analog1):

		if (self.removeFirstElement):
			self.analog1Data = self.analog1Data[1:]

		self.analog1Data.append(analog1)
		self.analogLine1.setData(self.time, self.analog1Data)

	def onAnalog2DataReady(self, analog2):

		if (self.removeFirstElement):
			self.analog2Data = self.analog2Data[1:]

		self.analog2Data.append(analog2)
		self.analogLine2.setData(self.time, self.analog2Data)

	def onAnalog3DataReady(self, analog3):

		if (self.removeFirstElement):
			self.analog3Data = self.analog3Data[1:]

		self.analog3Data.append(analog3)
		self.analogLine3.setData(self.time, self.analog3Data)