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

		self.connectionStatusLabel = ""
		self.connectButton = ""
		self.streamButton = ""
		self.magnitudeLxLabel = ""
		self.magnitudeRxLabel = ""
		self.participantIdLineEdit = ""
		self.setMarkerButton = ""

		self.markerState = 0
		self.connectionOpened = False
		self.streaming = False

		self.styler = Styler()

		self.socketController = socketController

		self.createRunningSettings()
		self.createLoggingSettings()
		self.createSlidersSettings()
		self.createProfileSettings()
		self.manageLayouts()

	def createRunningSettings(self):

		logoIcon = QtGui.QPixmap("../resources/myoswiss-K.png")
		logoLabel = QtWidgets.QLabel()
		logoLabel.setPixmap(logoIcon)
		logoLabel.setFixedHeight(30)

		logoLabelLayout = QtWidgets.QHBoxLayout()
		logoLabelLayout.setSpacing(0)
		logoLabelLayout.setContentsMargins(2,2,2,2)
		logoLabelLayout.addWidget(logoLabel)

		connectIcon = QtGui.QIcon("../resources/connect.png")
		self.connectButton = QtWidgets.QPushButton("  Connect")
		self.connectButton.setToolTip("Connect to the server")
		self.connectButton.setStyleSheet(self.styler.buttonStyle)
		self.connectButton.clicked.connect(self.onConnectButtonClicked)
		self.connectButton.setIcon(connectIcon)

		streamIcon = QtGui.QIcon("../resources/stream.png")
		self.streamButton = QtWidgets.QPushButton("  Stream")
		self.streamButton.setToolTip("Stream from the server")
		self.streamButton.setStyleSheet(self.styler.buttonStyle)
		self.streamButton.clicked.connect(self.onStreamButtonClicked)
		self.streamButton.setIcon(streamIcon)
		self.streamButton.setEnabled(False)

		buttonsLayout = QtWidgets.QHBoxLayout()
		buttonsLayout.setSpacing(4)
		buttonsLayout.setContentsMargins(0,0,0,0)
		buttonsLayout.addWidget(self.connectButton)
		buttonsLayout.addWidget(self.streamButton)

		self.connectionStatusLabel = QtWidgets.QLabel("Status: No connection")
		self.connectionStatusLabel.setToolTip("Connection Status")
		self.connectionStatusLabel.setFixedHeight(15)
		self.connectionStatusLabel.setStyleSheet(self.styler.connectionStatusLabel)

		self.logger = QtWidgets.QPlainTextEdit("")
		self.logger.setReadOnly(True)
		self.logger.setToolTip("Log area")

		loggerLayout = QtWidgets.QVBoxLayout()
		loggerLayout.setSpacing(1)
		loggerLayout.setContentsMargins(1,1,1,0)
		loggerLayout.addWidget(self.connectionStatusLabel)
		loggerLayout.addWidget(self.logger)

		loggerFrame = QtWidgets.QFrame()
		loggerFrame.setLayout(loggerLayout)
		loggerFrame.setStyleSheet(self.styler.loggerFrame)
		self.logger.setStyleSheet(self.styler.noBorder)

		runningSettingsLayout = QtWidgets.QVBoxLayout()
		runningSettingsLayout.addLayout(logoLabelLayout)
		runningSettingsLayout.addLayout(buttonsLayout)
		runningSettingsLayout.addWidget(loggerFrame)

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
		magnitudeLxSlider.setTracking(False)
		magnitudeLxSlider.valueChanged.connect(self.magnitudeLxSliderValueChanged)
		magnitudeLxSlider.sliderMoved.connect(self.magnitudeLxSliderMoved)

		self.magnitudeRxLabel = QtWidgets.QLabel("Magnitude Scaling Rx : 0")
		self.magnitudeRxLabel.setStyleSheet(self.styler.labelStyle)

		magnitudeRxSlider = QtWidgets.QSlider(Qt.Horizontal)
		magnitudeRxSlider.setMinimum(0)
		magnitudeRxSlider.setMaximum(100)
		magnitudeRxSlider.setSingleStep(1)
		magnitudeRxSlider.setTickInterval(10)
		magnitudeRxSlider.setTickPosition(QtWidgets.QSlider.TicksBelow)
		magnitudeRxSlider.setTracking(False)
		magnitudeRxSlider.valueChanged.connect(self.magnitudeRxSliderValueChanged)
		magnitudeRxSlider.sliderMoved.connect(self.magnitudeRxSliderMoved)

		self.setMarkerButton = QtWidgets.QPushButton("Set Marker")
		self.setMarkerButton.setToolTip("Set marker in log data")
		self.setMarkerButton.setStyleSheet(self.styler.buttonStyle)
		self.setMarkerButton.clicked.connect(self.onSetMarkerButtonClicked)

		slidersSettingsLayout = QtWidgets.QVBoxLayout()
		slidersSettingsLayout.addSpacing(8)
		slidersSettingsLayout.addWidget(self.magnitudeLxLabel)
		slidersSettingsLayout.addWidget(magnitudeLxSlider)
		slidersSettingsLayout.addWidget(self.magnitudeRxLabel)
		slidersSettingsLayout.addWidget(magnitudeRxSlider)
		slidersSettingsLayout.addWidget(self.setMarkerButton)

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
		mainLayout.addWidget(self.runningSettingsFrame, 2)
		mainLayout.addWidget(self.loggingSettingsFrame, 1)
		mainLayout.addWidget(self.slidersSettingsFrame, 2)
		mainLayout.addWidget(self.profileSettingsFrame, 4)

		self.setLayout(mainLayout)

	def addMessageToLogger(self, msg):

		self.logger.appendPlainText(msg)
		self.logger.verticalScrollBar().setValue(self.logger.verticalScrollBar().maximum())

	# Slots

	def onConnectButtonClicked(self):

		self.connectionOpened = self.socketController.startConnection()
		if (self.connectionOpened):
			self.connectionStatusLabel.setText("Status: Connected")
			self.connectButton.setEnabled(False)
			self.streamButton.setEnabled(True)
		else:
			self.connectionStatusLabel.setText("Status: No connection")
			self.addMessageToLogger("Connection failed to the server.")
			self.connectButton.setEnabled(True)
			self.streamButton.setEnabled(False)

	def onStreamButtonClicked(self):

		self.streaming, errMsg = self.socketController.startStreaming()
		if self.streaming:
			self.connectionStatusLabel.setText("Status: Streaming")
			self.streamButton.setEnabled(False)
		else:
			self.streamButton.setEnabled(True)
			self.addMessageToLogger("Streaming failed, {}".format(errMsg))


	def onSetMarkerButtonClicked(self):

		if self.markerState == 1:
			self.markerState = 0
			self.setMarkerButton.setStyleSheet(self.styler.buttonStyle)
		else:
			self.markerState = 1
			self.setMarkerButton.setStyleSheet(self.styler.buttonOnStyle)
		self.socketController.onMarkerStateChanged(self.markerState)

	def magnitudeLxSliderValueChanged(self, value):
		
		self.magnitudeLxSliderMoved(value)
		self.socketController.magnitudeScalingLXChanged(value)

	def magnitudeLxSliderMoved(self, value):

		self.magnitudeLxLabel.setText("Magnitude Scaling Lx : {}".format(value))

	def magnitudeRxSliderValueChanged(self, value):

		self.magnitudeRxSliderMoved(value)
		self.socketController.magnitudeScalingRXChanged(value)

	def magnitudeRxSliderMoved(self, value):

		self.magnitudeRxLabel.setText("Magnitude Scaling Rx : {}".format(value))

	def onLogButtonClicked(self):
		participantId = self.participantIdLineEdit.text().strip()


		self.socketController.logData(participantId)
		