from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
import sys
import struct

sys.path.append(".")
from connection_utils import SocketCommunicator


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

		parent.destroyed.connect(self.onParentDestroyed)

		self.streamData.connect(self.socketCommunicator.receiveData)
		self.thread.start()

		
	def onParentDestroyed(self):
		print ("will delete")

		self.socketCommunicator = None
		self.thread.terminate()
		self.thread = None

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
		print ("Enable State : {}".format(self.enableState))

	def magnitudeScalingLXChanged(self, value):
		self.magnitudeLx = value
		print ("Magnitude Lx : {}".format(self.magnitudeLx))

	def magnitudeScalingRXChanged(self, value):
		self.magnitudeRx = value
		print ("Magnitude Rx : {}".format(self.magnitudeRx))

	def markerStateChanged(self, markerState):
		self.markerState = markerState
		print ("Marker State : {}".format(self.markerState))

	def desiredForceProfileChanged(self, desiredForce):
		self.desiredForceProfile = desiredForce
		print ("Desired Force Profile : {}".format(str(len(self.desiredForceProfile))))