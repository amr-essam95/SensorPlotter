from PyQt5.QtCore import Qt, QObject, pyqtSignal, QThread
import sys
import csv
import struct
import threading

sys.path.append(".")
from connection_utils import SocketCommunicator
from plot_updater import PlotUpdater


class SocketController(QObject):

	streamData = pyqtSignal()
	connectToSocket = pyqtSignal()
	connectionStatusChanged = pyqtSignal(bool)
	markerStateChanged = pyqtSignal(int)

	def __init__(self, parent=None):
		super(SocketController, self).__init__(parent)

		self.enableState = 0
		self.magnitudeLx = 0
		self.magnitudeRx = 0
		self.markerState = 0
		self.desiredForceProfile = [0] * 100
		self.connectionSucceded = False
		self.headerList = []

		# This flag prevents serveral trials to connect at the same time.
		self.connecting = False
		
		# Fill header list for the log file.
		self.fillLogHeaderList()

		# Create new thread for handling socket communication.
		self.socketCommunicator = SocketCommunicator()
		self.thread = QThread(self)
		self.thread.setTerminationEnabled(True)
		self.socketCommunicator.moveToThread(self.thread)

		# Create new thread for updating graphs.
		self.plotUpdater = PlotUpdater(self.socketCommunicator)
		self.updaterThread = QThread(self)
		self.updaterThread.setTerminationEnabled(True)
		self.plotUpdater.moveToThread(self.updaterThread)

		parent.destroyed.connect(self.onParentDestroyed)

		self.streamData.connect(self.socketCommunicator.receiveData)
		self.connectToSocket.connect(self.socketCommunicator.connect)
		self.thread.start()

		self.socketCommunicator.dataReady.connect(self.plotUpdater.onDataReady)
		self.socketCommunicator.connectionStatusChanged.connect(self.onConnectionStatusChanged)

		self.markerStateChanged.connect(self.plotUpdater.onMarkerStateChanged)
		self.updaterThread.start()
		
	def onParentDestroyed(self):

		self.socketCommunicator = None
		self.plotUpdater = None

		self.thread.terminate()
		self.updaterThread.terminate()

		self.thread = None
		self.updaterThread = None

	def onConnectionStatusChanged(self, status):

		self.connectionSucceded = status
		self.connecting = False
		self.connectionStatusChanged.emit(self.connectionSucceded)

	def startConnection(self):

		if self.connectionSucceded == False and self.connecting == False:
			self.connecting =  True
			self.connectToSocket.emit()

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

	def onMarkerStateChanged(self, markerState):
		self.markerState = markerState
		self.markerStateChanged.emit(self.markerState)
		self.sendData()

	def desiredForceProfileChanged(self, desiredForce):
		self.desiredForceProfile = desiredForce
		self.sendData()

	def fillLogHeaderList(self):

		self.headerList = [
			"Timestamp(s)",
			"Timestamp(ns)",
			"RS_AFlt",
			"LS_AFlt",
			"RT_AFlt",
			"LT_AFlt",
			"Tr_AFlt",
			"RM_Enc",
			"LM_Enc",
			"RM_CurR",
			"LM_CurR",
			"RM_CurS",
			"LM_CurS",
			"Analog0",
			"Analog1",
			"Analog2",
			"Analog3",
			"Sync_IN",
			"Sync_OUT",
			"USR_BTN",
			"Left enable",
			"Right enable",
			"Dummy0",
			"Dummy1",
			"Marker State"
		]

	def logData(self, participantId):

		with open('log_{}'.format(participantId), mode='w') as logFile:

			logFile.write("{}\n".format(participantId))
			logWriter = csv.writer(logFile, delimiter='\t')

			# Write Header.
			logWriter.writerow(self.headerList)

			receivedData = self.plotUpdater.receivedData
			logWriter.writerows(receivedData)