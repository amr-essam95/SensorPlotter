from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
import sys
sys.path.append(".")
from styler import Styler
from profile_frame import ProfileFrame
from connection_utils import SocketCommunicator

class SettingsFrame(QtWidgets.QFrame): 
	
	def __init__(self, socketController, parent=None): 
		super().__init__()

		self.runningSettingsFrame = ""
		self.loggingSettingsFrame = ""
		self.slidersSettingsFrame = ""
		self.profileSettingsFrame = ""

		self.magnitudeLxLabel = ""
		self.magnitudeRxLabel = ""
		self.participantIdLineEdit = ""

		self.markerState = 0

		self.styler = Styler()

		self.socketController = socketController

		self.createRunningSettings()
		self.createLoggingSettings()
		self.createSlidersSettings()
		self.createProfileSettings()
		self.manageLayouts()

	def createRunningSettings(self):

		connectIcon = QtGui.QIcon("../resources/connect.png")
		connectButton = QtWidgets.QPushButton("  Connect")
		connectButton.setToolTip("Connect to the server")
		connectButton.setStyleSheet(self.styler.buttonStyle)
		connectButton.clicked.connect(self.onConnectButtonClicked)
		connectButton.setIcon(connectIcon)

		streamIcon = QtGui.QIcon("../resources/stream.png")
		streamButton = QtWidgets.QPushButton("  Stream")
		streamButton.setToolTip("Stream from the server")
		streamButton.setStyleSheet(self.styler.buttonStyle)
		streamButton.clicked.connect(self.onStreamButtonClicked)
		streamButton.setIcon(streamIcon)

		runningSettingsLayout = QtWidgets.QVBoxLayout()
		runningSettingsLayout.addWidget(connectButton)
		runningSettingsLayout.addWidget(streamButton)

		self.runningSettingsFrame = QtWidgets.QFrame()
		self.runningSettingsFrame.setLayout(runningSettingsLayout)
		self.styler.addShadow(self.runningSettingsFrame)

	def createLoggingSettings(self):

		participantIdLabel = QtWidgets.QLabel("Participant Id")
		participantIdLabel.setMaximumHeight(40)
		participantIdLabel.setStyleSheet(self.styler.labelStyle)

		self.participantIdLineEdit = QtWidgets.QLineEdit()
		self.participantIdLineEdit.setStyleSheet(self.styler.lineEditStyle)
		self.participantIdLineEdit.setPlaceholderText("Participant Id")

		logIcon = QtGui.QIcon("../resources/log.png")
		logButton = QtWidgets.QPushButton("  Log")
		logButton.setToolTip("Connect to the server")
		logButton.setStyleSheet(self.styler.buttonStyle)
		logButton.clicked.connect(self.onLogButtonClicked)
		logButton.setIcon(logIcon)

		loggingSettingsLayout = QtWidgets.QVBoxLayout()
		loggingSettingsLayout.addWidget(participantIdLabel)
		loggingSettingsLayout.addWidget(self.participantIdLineEdit)
		loggingSettingsLayout.addStretch()
		loggingSettingsLayout.addWidget(logButton)

		self.loggingSettingsFrame = QtWidgets.QFrame()
		self.loggingSettingsFrame.setLayout(loggingSettingsLayout)
		self.styler.addShadow(self.loggingSettingsFrame)

	def createSlidersSettings(self):

		self.magnitudeLxLabel = QtWidgets.QLabel("Magnitude Scaling Lx : 0")
		self.magnitudeLxLabel.setStyleSheet(self.styler.labelStyle)

		magnitudeLxSlider = QtWidgets.QSlider(Qt.Horizontal)
		magnitudeLxSlider.setMinimum(0)
		magnitudeLxSlider.setMaximum(100)
		magnitudeLxSlider.setSingleStep(1)
		magnitudeLxSlider.setTickInterval(10)
		magnitudeLxSlider.setTickPosition(QtWidgets.QSlider.TicksBelow)
		magnitudeLxSlider.valueChanged.connect(self.magnitudeLxSliderValueChanged)

		self.magnitudeRxLabel = QtWidgets.QLabel("Magnitude Scaling Rx : 0")
		self.magnitudeRxLabel.setStyleSheet(self.styler.labelStyle)

		magnitudeRxSlider = QtWidgets.QSlider(Qt.Horizontal)
		magnitudeRxSlider.setMinimum(0)
		magnitudeRxSlider.setMaximum(100)
		magnitudeRxSlider.setSingleStep(1)
		magnitudeRxSlider.setTickInterval(10)
		magnitudeRxSlider.setTickPosition(QtWidgets.QSlider.TicksBelow)
		magnitudeRxSlider.valueChanged.connect(self.magnitudeRxSliderValueChanged)

		setMarkerButton = QtWidgets.QPushButton("Set Marker")
		setMarkerButton.setToolTip("Set marker in log data")
		setMarkerButton.setStyleSheet(self.styler.buttonStyle)
		setMarkerButton.clicked.connect(self.onSetMarkerButtonClicked)

		slidersSettingsLayout = QtWidgets.QVBoxLayout()
		slidersSettingsLayout.addSpacing(8)
		slidersSettingsLayout.addWidget(self.magnitudeLxLabel)
		slidersSettingsLayout.addWidget(magnitudeLxSlider)
		slidersSettingsLayout.addWidget(self.magnitudeRxLabel)
		slidersSettingsLayout.addWidget(magnitudeRxSlider)
		slidersSettingsLayout.addWidget(setMarkerButton)

		self.slidersSettingsFrame = QtWidgets.QFrame()
		self.slidersSettingsFrame.setLayout(slidersSettingsLayout)
		self.styler.addShadow(self.slidersSettingsFrame)

	def createProfileSettings(self):

		self.profileSettingsFrame = ProfileFrame(self.socketController)
		self.styler.addShadow(self.profileSettingsFrame)

	def manageLayouts(self):
		
		mainLayout = QtWidgets.QHBoxLayout()
		mainLayout.setContentsMargins(2,2,2,2)
		mainLayout.setSpacing(10)
		mainLayout.addWidget(self.runningSettingsFrame, 1)
		mainLayout.addWidget(self.loggingSettingsFrame, 1)
		mainLayout.addWidget(self.slidersSettingsFrame, 2)
		mainLayout.addWidget(self.profileSettingsFrame, 4)

		self.setLayout(mainLayout)

	# Slots

	def onConnectButtonClicked(self):

		self.socketController.startConnection()

	def onStreamButtonClicked(self):

		self.socketController.startStreaming()


	def onSetMarkerButtonClicked(self):

		if self.markerState == 1:
			self.markerState = 0
		else:
			self.markerState = 1
		self.socketController.markerStateChanged(self.markerState)

	def magnitudeLxSliderValueChanged(self, value):

		self.magnitudeLxLabel.setText("Magnitude Scaling Lx : {}".format(value))
		self.socketController.magnitudeScalingLXChanged(value)

	def magnitudeRxSliderValueChanged(self, value):

		self.magnitudeRxLabel.setText("Magnitude Scaling Rx : {}".format(value))
		self.socketController.magnitudeScalingRXChanged(value)

	def onLogButtonClicked(self):
		participantId = self.participantIdLineEdit.text().strip()
		logFile = open('log_{}'.format(participantId), 'w')
		logFile.write("{}".format(participantId))

		self.socketController.sendData()
		