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
		self.connectionSucceded = False

		# Create new thread for handling socket communication.
		self.socketCommunicator = SocketCommunicator()
		self.thread = QtCore.QThread(self)
		self.thread.setTerminationEnabled(True)
		self.socketCommunicator.moveToThread(self.thread)

		# Create new thread for updating graphs.
		self.plotUpdater = PlotUpdater(self.socketCommunicator)
		self.updaterThread = QtCore.QThread(self)
		self.updaterThread.setTerminationEnabled(True)
		self.plotUpdater.moveToThread(self.updaterThread)

		parent.destroyed.connect(self.onParentDestroyed)

		self.streamData.connect(self.socketCommunicator.receiveData)
		self.thread.start()

		self.socketCommunicator.dataReady.connect(self.plotUpdater.onDataReady)
		self.updaterThread.start()
		
	def onParentDestroyed(self):

		self.socketCommunicator = None
		self.plotUpdater = None

		self.thread.terminate()
		self.updaterThread.terminate()

		self.thread = None
		self.updaterThread = None

	def startConnection(self):

		if self.connectionSucceded == False:
			self.connectionSucceded = self.socketCommunicator.connect()
			return self.connectionSucceded
		else:
			return True

	def sendData(self):
		if self.connectionSucceded:
			structData = self.constructData()
			if structData != None:
				self.socketCommunicator.sendData(structData)

	def constructData(self):
		
		if len(self.desiredForceProfile) != 100:
			return None
		dummy1 = 0
		dummy2 = 0
		structData = struct.pack('?BB?100HHH', self.enableState, self.magnitudeLx, self.magnitudeRx, self.markerState, *self.desiredForceProfile, dummy1, dummy2)
		return structData

	def startStreaming(self):

		if len(self.desiredForceProfile) != 100:
			return False, "No profile available."
		if self.connectionSucceded:
			self.streamData.emit()
			return True, ""
		else:
			return False, "No connection to server."

	def enableStateChanged(self, state):
		self.enableState = state
		self.sendData()

	def magnitudeScalingLXChanged(self, value):
		self.magnitudeLx = value
		self.sendData()

	def magnitudeScalingRXChanged(self, value):
		self.magnitudeRx = value
		self.sendData()

	def markerStateChanged(self, markerState):
		self.markerState = markerState
		self.sendData()

	def desiredForceProfileChanged(self, desiredForce):
		self.desiredForceProfile = desiredForce
		self.sendData()