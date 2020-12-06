from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
import sys
import struct
import threading

sys.path.append(".")
from connection_utils import SocketCommunicator
from plot_updater import PlotUpdater


class SocketController(QtCore.QObject):

	streamData = QtCore.pyqtSignal()

	def __init__(self, parent=None):
		super(SocketController, self).__init__(parent)

		self.enableState = 0
		self.magnitudeLx = 0
		self.magnitudeRx = 0
		self.markerState = 0
		self.desiredForceProfile = []

		self.socketCommunicator = SocketCommunicator()
		self.thread = QtCore.QThread(self)
		self.thread.setTerminationEnabled(True)
		self.socketCommunicator.moveToThread(self.thread)

		self.plotUpdater = PlotUpdater(self.socketCommunicator)
		self.updaterThread = QtCore.QThread(self)
		self.updaterThread.setTerminationEnabled(True)
		self.plotUpdater.moveToThread(self.updaterThread)

		self.updaterThread.finished.connect(self.threadFinished)

		parent.destroyed.connect(self.onParentDestroyed)

		self.streamData.connect(self.socketCommunicator.receiveData)
		self.thread.start()

		self.socketCommunicator.dataReady.connect(self.plotUpdater.onDataReady)
		self.updaterThread.start()
	
	def threadFinished(self):
		print ("thread finished")
		
	def onParentDestroyed(self):

		self.socketCommunicator = None
		self.plotUpdater = None

		self.thread.terminate()
		self.updaterThread.terminate()

		self.thread = None
		self.updaterThread = None

	def startConnection(self):

		self.socketCommunicator.connect()

	def sendData(self):
		structData = self.constructData()
		self.socketCommunicator.sendData(structData)

	def constructData(self):
		
		dummy1 = 0
		dummy2 = 0
		structData = struct.pack('?BB?100HHH', self.enableState, self.magnitudeLx, self.magnitudeRx, self.markerState, *self.desiredForceProfile, dummy1, dummy2)
		return structData

	def startStreaming(self):

		self.streamData.emit()

	def enableStateChanged(self, state):
		self.enableState = state

	def magnitudeScalingLXChanged(self, value):
		self.magnitudeLx = value

	def magnitudeScalingRXChanged(self, value):
		self.magnitudeRx = value

	def markerStateChanged(self, markerState):
		self.markerState = markerState

	def desiredForceProfileChanged(self, desiredForce):
		self.desiredForceProfile = desiredForce