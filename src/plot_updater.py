from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
import sys
import struct

from styler import Styler

from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg

sys.path.append(".")
from connection_utils import SocketCommunicator
from qt_thread_updater import get_updater
import threading

class PlotUpdater(QtCore.QObject):

	def __init__(self, socketCommunicator, parent=None):
		super(PlotUpdater, self).__init__(parent)

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

		self.socketCommunicator = socketCommunicator

		# self.socketCommunicator.thighDataReady.connect(self.onThighDataReady)
		# self.socketCommunicator.shankDataReady.connect(self.onShankDataReady)
		# self.socketCommunicator.currentDataReady.connect(self.onCurrentDataReady)
		# self.socketCommunicator.analog0DataReady.connect(self.onAnalog0DataReady)
		# self.socketCommunicator.analog1DataReady.connect(self.onAnalog1DataReady)
		# self.socketCommunicator.analog2DataReady.connect(self.onAnalog2DataReady)
		# self.socketCommunicator.analog3DataReady.connect(self.onAnalog3DataReady)

		
	def run2(self):
		print ("start listening2")
		print(threading.current_thread().name)
		print(threading.get_ident())

	def run(self):
		print ("start listening")
		print(threading.current_thread().name)
		print(threading.get_ident())

	def onDataReady(self, time, rt, lt, tr, rs, ls, rmR, lmR, rmS, lmS, analog0, analog1, analog2, analog3):

		if (len(self.time) > 20):
			self.removeFirstElement = True
		
		if (self.removeFirstElement):
			self.time = self.time[1:]

		self.time.append(time)

		self.onThighDataReady(rt, lt, tr)
		self.onShankDataReady(rs, ls)
		self.onCurrentDataReady( rmR, lmR, rmS, lmS)
		self.onAnalog0DataReady(analog0)
		self.onAnalog1DataReady(analog1)
		self.onAnalog2DataReady(analog2)
		self.onAnalog3DataReady(analog3)

	def onThighDataReady(self, rt, lt, tr):

		# print(threading.current_thread().name)
		# print(threading.get_ident())

		if self.removeFirstElement:
			self.rtData = self.rtData[1:]
			self.ltData = self.ltData[1:]
			self.trData = self.trData[1:]
		
		self.rtData.append(rt * 0.001)
		self.ltData.append(lt * 0.001)
		self.trData.append(tr * 0.001)

		get_updater().call_latest(self.rtLine.setData, self.time, self.rtData)
		get_updater().call_latest(self.ltLine.setData, self.time, self.ltData)
		get_updater().call_latest(self.trLine.setData, self.time, self.trData)

		# self.rtLine.setData(self.time, self.rtData)
		# self.ltLine.setData(self.time, self.ltData)
		# self.trLine.setData(self.time, self.trData)

	def onShankDataReady(self, rs, ls):

		if self.removeFirstElement:
			self.rsData = self.rsData[1:]
			self.lsData = self.lsData[1:]

		self.rsData.append(rs * 0.001)
		self.lsData.append(ls * 0.001)

		# self.rsLine.setData(self.time, self.rsData)
		# self.lsLine.setData(self.time, self.lsData)

		get_updater().call_latest(self.rsLine.setData, self.time, self.rsData)
		get_updater().call_latest(self.lsLine.setData, self.time, self.lsData)

	def onCurrentDataReady(self, rmR, lmR, rmS, lmS):

		if (self.removeFirstElement):
			self.rmRData = self.rmRData[1:]
			self.lmRData = self.lmRData[1:]
			self.rmSData = self.rmSData[1:]
			self.lmSData = self.lmSData[1:]

		self.rmRData.append(rmR * 0.001)
		self.lmRData.append(lmR * 0.001)
		self.rmSData.append(rmS * 0.001)
		self.lmSData.append(lmS * 0.001)

		# self.rmReadoutLine.setData(self.time, self.rmRData)
		# self.lmReadoutLine.setData(self.time, self.lmRData)
		# self.rmSentLine.setData(self.time, self.rmSData)
		# self.lmSentLine.setData(self.time, self.lmSData)

		
		get_updater().call_latest(self.rmReadoutLine.setData, self.time, self.rmRData)
		get_updater().call_latest(self.lmReadoutLine.setData, self.time, self.lmRData)
		get_updater().call_latest(self.rmSentLine.setData, self.time, self.rmSData)
		get_updater().call_latest(self.lmSentLine.setData, self.time, self.lmSData)

	def onAnalog0DataReady(self, analog0):

		if (self.removeFirstElement):
			self.analog0Data = self.analog0Data[1:]

		self.analog0Data.append(analog0)
		# self.analogLine0.setData(self.time, self.analog0Data)

		get_updater().call_latest(self.analogLine0.setData, self.time, self.analog0Data)

	def onAnalog1DataReady(self, analog1):

		if (self.removeFirstElement):
			self.analog1Data = self.analog1Data[1:]

		self.analog1Data.append(analog1)
		# self.analogLine1.setData(self.time, self.analog1Data)

		get_updater().call_latest(self.analogLine1.setData, self.time, self.analog1Data)

	def onAnalog2DataReady(self, analog2):

		if (self.removeFirstElement):
			self.analog2Data = self.analog2Data[1:]

		self.analog2Data.append(analog2)
		# self.analogLine2.setData(self.time, self.analog2Data)

		get_updater().call_latest(self.analogLine2.setData, self.time, self.analog2Data)

	def onAnalog3DataReady(self, analog3):

		if (self.removeFirstElement):
			self.analog3Data = self.analog3Data[1:]

		self.analog3Data.append(analog3)
		# self.analogLine3.setData(self.time, self.analog3Data)

		get_updater().call_latest(self.analogLine3.setData, self.time, self.analog3Data)

