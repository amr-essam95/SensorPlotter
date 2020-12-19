from PyQt5.QtCore import QObject, pyqtSignal

import socket
import struct
import threading
import select
import queue

class SocketCommunicator(QObject):

	# Signal for the state of the connection.
	connectionStatusChanged = pyqtSignal(bool)
	# Signal for the data to be plotted.
	dataReady = pyqtSignal(list)
	# Signal for the sunc and user buttons.
	labelDataReady = pyqtSignal(bool, bool)

	def __init__(self, parent=None):
		"""
			This class handles the socket communication in a different thread to be
			able to handle data every 10 ms and emit a signal with the new data.
		"""

		super(SocketCommunicator, self).__init__(parent)
		self.hostname = '192.168.7.2'
		self.port = 6666
		self.socketConnection = ''
		self.socketConnectionSucceeded = False

		# Flag to stop receiving data.
		self.running = False
		self.lock = threading.Lock()

		# Any data received by this queue will be sent
		self.send_queue = queue.Queue()
		# Any data sent to ssock shows up on rsock
		self.rsock, self.ssock = socket.socketpair()

	def clearData(self):
		# Close socket connection and clear data to be able to connect again.
		if self.socketConnectionSucceeded:
			self.socketConnection.close()
			self.socketConnection = ''
			self.socketConnectionSucceeded = False
			self.send_queue = queue.Queue()
			self.rsock, self.ssock = socket.socketpair()
			self.connectionStatusChanged.emit(False)


	def stopReceivingData(self):
		# This method stops receiving data.
		with self.lock:
			if self.running == True:
				# In case we're receiving data stop the thread loop.
				self.running = False
			else:
				# In case we haven't started receiving data, clear and emit connection closed.
				self.clearData()

	def connect(self):
		try:
			self.socketConnectionSucceeded = True
			self.socketConnection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			self.socketConnection.connect((self.hostname, self.port))
			self.connectionStatusChanged.emit(True)

		except:
			self.connectionStatusChanged.emit(False)
			self.socketConnectionSucceeded = False

	def sendData(self, data):
		if self.socketConnectionSucceeded == True:
			# Put the data to send inside the queue
			self.send_queue.put(data)
   		 	# Sending data to ssock which goes to rsock
			self.ssock.send(b"\x00")
		else:
			print ("Connection is closed, please connect first.")

	def receiveData(self):

		with self.lock:
			self.running = True

		while True:
			with self.lock:
				if self.running == False:
					# End receiving data.
					self.clearData()
					return

			# When either socket has data or rsock has data, select.select will return
			rlist, _, _ = select.select([self.socketConnection, self.rsock], [], [])
			for ready_socket in rlist:
				if ready_socket is self.socketConnection:
					try:
						data = self.socketConnection.recv(56)
					except:
						# If connection is closed.
						self.clearData()
						return
					if not data: continue
					try:
						structList = struct.unpack("iiiiiiihhhhhhhhhhBBBhh",data)
						self.dataReady.emit(list(structList))
						self.labelDataReady.emit(structList[17], structList[19])
					except struct.error as error:
						print ("Wrong format of data is received, {}".format(error))
				else:
					# Ready_socket is rsock

					# Dump the ready mark
					self.rsock.recv(1)

					# Send the data.
					dataToSend = self.send_queue.get()
					self.socketConnection.sendall(dataToSend)