from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
import sys
sys.path.append(".")
from styler import Styler

class PlottingFrame(QtWidgets.QFrame): 
	def __init__(self, parent=None): 
		super().__init__()

		self.anglePlotsFrame = ""
		self.analogPlotsFrame = ""
		self.buttonsFrame = ""
		self.runButton = ""
		self.syncButton = ""
		self.userButton = ""
		self.syncFrame = ""
		self.userFrame = ""

		self.styler = Styler()

		self.createAnglePlotsFrame()
		self.createAnalogPlotsFrame()
		self.createButtonsFrame()
		self.manageLayouts()

	def createAnglePlotsFrame(self):

		self.anglePlotsFrame = QtWidgets.QFrame()
		self.styler.addShadow(self.anglePlotsFrame)

	def createAnalogPlotsFrame(self):

		self.analogPlotsFrame = QtWidgets.QFrame()
		self.styler.addShadow(self.analogPlotsFrame)

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

	def onPauseButtonClicked(self):

		self.runButton.clicked.disconnect(self.onPauseButtonClicked)
		self.runButton.setStyleSheet(self.styler.playButtonStyle)
		self.runButton.clicked.connect(self.onRunButtonClicked)

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
