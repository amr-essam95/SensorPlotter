from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
import socket
import struct

class SocketCommunicator(QtCore.QObject):

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
			structList = struct.unpack("iiiiiiihhhhhhHHHHBBBhhhh",data)
			print (structList)

	def run(self):
		print("Thread start")
		self.receiveData()
		print("Thread complete")