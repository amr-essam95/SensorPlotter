from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
import socket
import struct
import threading

class SocketCommunicator(QtCore.QObject):

	dataReady = QtCore.pyqtSignal(int, int, int, int, int, int, int, int, int, int, int, int, int, int)
	labelDataReady = QtCore.pyqtSignal(bool, bool)

	def __init__(self, parent=None):
		super(SocketCommunicator, self).__init__(parent)
		# self.hostname = '192.168.7.2'
		self.hostname = '127.0.0.1'
		self.port = 6666
		self.socketConnection = ''
		self.socketConnectionSucceeded = False

	def connect(self):
		try:
			self.socketConnectionSucceeded = True
			self.socketConnection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			self.socketConnection.connect((self.hostname, self.port))
		except:
			self.socketConnectionSucceeded = False
			print ("Connection with Server failed.")

	def sendData(self, data):
		if self.socketConnectionSucceeded == True:
			self.socketConnection.sendall(data)
		else:
			print ("Connection is closed, please connect first.")

	def receiveData(self):
		while True:
			data = self.socketConnection.recv(60)
			if not data: break
			structList = struct.unpack("iiiiiiihhHHHHHHHHBBBhhhh",data)
			self.dataReady.emit(structList[0], structList[4], structList[5], structList[6], structList[2], structList[3], structList[9], structList[10], structList[11], structList[12], structList[13], structList[14], structList[15], structList[16])
			self.labelDataReady.emit(structList[17], structList[19])