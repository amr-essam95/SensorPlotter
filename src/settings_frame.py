from PyQt5.QtWidgets import QFrame, QFileDialog, QPushButton, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPlainTextEdit, QSlider
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QColor, QIntValidator, QPixmap, QIcon
import sys
import os
sys.path.append(".")
from styler import Styler
from profile_frame import ProfileFrame
from connection_utils import SocketCommunicator

class SettingsFrame(QFrame): 
	
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
		self.magnitudeLxInput  = ""
		self.magnitudeLxSlider = ""
		self.magnitudeRxLabel = ""
		self.magnitudeRxInput = ""
		self.magnitudeRxSlider = ""
		self.participantIdLineEdit = ""
		self.setMarkerButton = ""
		self.logLineEdit = ""
		self.logDirPath = ""

		self.connectIcon = QIcon("resources/connect.png")
		self.disconnectIcon = QIcon("resources/disconnect.png")

		self.markerState = 0
		self.connectionOpened = False
		self.streaming = False

		self.styler = Styler()

		self.socketController = socketController
		self.socketController.connectionStatusChanged.connect(self.onConnectionStatusChanged)

		self.createRunningSettings()
		self.createLoggingSettings()
		self.createSlidersSettings()
		self.createProfileSettings()
		self.manageLayouts()

	def createRunningSettings(self):

		logoIcon = QPixmap("resources/myoswiss-K.png")
		logoLabel = QLabel()
		logoLabel.setPixmap(logoIcon)
		logoLabel.setFixedHeight(30)

		logoLabelLayout = QHBoxLayout()
		logoLabelLayout.setSpacing(0)
		logoLabelLayout.setContentsMargins(2,2,2,2)
		logoLabelLayout.addWidget(logoLabel)

		self.connectButton = QPushButton("  Connect")
		self.connectButton.setToolTip("Connect to the server")
		self.connectButton.setStyleSheet(self.styler.buttonStyle)
		self.connectButton.clicked.connect(self.onConnectButtonClicked)
		self.connectButton.setIcon(self.connectIcon)

		streamIcon = QIcon("resources/stream.png")
		self.streamButton = QPushButton("  Stream")
		self.streamButton.setToolTip("Stream from the server")
		self.streamButton.setStyleSheet(self.styler.buttonStyle)
		self.streamButton.clicked.connect(self.onStreamButtonClicked)
		self.streamButton.setIcon(streamIcon)
		self.streamButton.setEnabled(False)

		buttonsLayout = QHBoxLayout()
		buttonsLayout.setSpacing(4)
		buttonsLayout.setContentsMargins(0,0,0,0)
		buttonsLayout.addWidget(self.connectButton)
		buttonsLayout.addWidget(self.streamButton)

		self.connectionStatusLabel = QLabel("Status: No connection")
		self.connectionStatusLabel.setToolTip("Connection Status")
		self.connectionStatusLabel.setFixedHeight(15)
		self.connectionStatusLabel.setStyleSheet(self.styler.connectionStatusLabel)

		self.logger = QPlainTextEdit("")
		self.logger.setReadOnly(True)
		self.logger.setToolTip("Log area")

		loggerLayout = QVBoxLayout()
		loggerLayout.setSpacing(1)
		loggerLayout.setContentsMargins(1,1,1,0)
		loggerLayout.addWidget(self.connectionStatusLabel)
		loggerLayout.addWidget(self.logger)

		loggerFrame = QFrame()
		loggerFrame.setLayout(loggerLayout)
		loggerFrame.setStyleSheet(self.styler.loggerFrame)
		self.logger.setStyleSheet(self.styler.noBorder)

		runningSettingsLayout = QVBoxLayout()
		runningSettingsLayout.addLayout(logoLabelLayout)
		runningSettingsLayout.addLayout(buttonsLayout)
		runningSettingsLayout.addWidget(loggerFrame)

		self.runningSettingsFrame = QFrame()
		self.runningSettingsFrame.setLayout(runningSettingsLayout)
		self.styler.addShadow(self.runningSettingsFrame)

	def createLoggingSettings(self):

		participantIdLabel = QLabel("Participant Id")
		participantIdLabel.setMaximumHeight(15)
		participantIdLabel.setMinimumHeight(15)
		participantIdLabel.setStyleSheet(self.styler.labelStyle)

		self.participantIdLineEdit = QLineEdit()
		self.participantIdLineEdit.setStyleSheet(self.styler.lineEditStyle)
		self.participantIdLineEdit.setPlaceholderText("Participant Id")

		logDirLabel = QLabel("Log Dir Path")
		logDirLabel.setMaximumHeight(15)
		logDirLabel.setMinimumHeight(15)
		logDirLabel.setStyleSheet(self.styler.labelStyle)

		self.logLineEdit = QLineEdit()
		self.logLineEdit.setStyleSheet(self.styler.browseLineEditStyle)
		self.logLineEdit.setPlaceholderText("Log Dir Path")
		self.logLineEdit.setEnabled(False)

		browseIcon = QIcon("resources/browse.png")
		browseButton = QPushButton()
		browseButton.setIcon(browseIcon)
		browseButton.setIconSize(QSize(30,30))
		browseButton.clicked.connect(self.onBrowseButtonClicked)

		lineEditLayout = QHBoxLayout()
		lineEditLayout.setContentsMargins(0,0,0,0)
		lineEditLayout.addWidget(self.logLineEdit)
		lineEditLayout.addWidget(browseButton)

		lineEditFrame = QFrame()
		lineEditFrame.setLayout(lineEditLayout)
		lineEditFrame.setStyleSheet(self.styler.browseLineEditFrame)

		logDirLayout = QVBoxLayout()
		logDirLayout.setContentsMargins(0,0,0,0)
		logDirLayout.addWidget(logDirLabel)
		logDirLayout.addWidget(lineEditFrame)

		logIcon = QIcon("resources/log.png")
		logButton = QPushButton("  Log")
		logButton.setToolTip("Connect to the server")
		logButton.setStyleSheet(self.styler.buttonStyle)
		logButton.clicked.connect(self.onLogButtonClicked)
		logButton.setIcon(logIcon)

		loggingSettingsLayout = QVBoxLayout()
		loggingSettingsLayout.addWidget(participantIdLabel)
		loggingSettingsLayout.addWidget(self.participantIdLineEdit)
		loggingSettingsLayout.addLayout(logDirLayout)
		loggingSettingsLayout.addStretch()
		loggingSettingsLayout.addWidget(logButton)

		self.loggingSettingsFrame = QFrame()
		self.loggingSettingsFrame.setLayout(loggingSettingsLayout)
		self.styler.addShadow(self.loggingSettingsFrame)

	def createSlidersSettings(self):

		self.magnitudeLxLabel = QLabel("Magnitude Scaling Lx :")
		self.magnitudeLxLabel.setStyleSheet(self.styler.labelStyle)

		self.magnitudeLxInput = QLineEdit("0")

		lxValidator = QIntValidator(0, 100)
		self.magnitudeLxInput.setValidator(lxValidator)
		self.magnitudeLxInput.textChanged.connect(self.magnitudeLxInputChanged)

		magnitudeLxLayout = QHBoxLayout()
		magnitudeLxLayout.setSpacing(2)
		magnitudeLxLayout.addWidget(self.magnitudeLxLabel)
		magnitudeLxLayout.addWidget(self.magnitudeLxInput)

		self.magnitudeLxSlider = QSlider(Qt.Horizontal)
		self.magnitudeLxSlider.setMinimum(0)
		self.magnitudeLxSlider.setMaximum(100)
		self.magnitudeLxSlider.setSingleStep(1)
		self.magnitudeLxSlider.setTickInterval(10)
		self.magnitudeLxSlider.setTickPosition(QSlider.TicksBelow)
		self.magnitudeLxSlider.setTracking(False)
		self.magnitudeLxSlider.valueChanged.connect(self.magnitudeLxSliderValueChanged)
		self.magnitudeLxSlider.sliderMoved.connect(self.magnitudeLxSliderMoved)

		self.magnitudeRxLabel = QLabel("Magnitude Scaling Rx :")
		self.magnitudeRxLabel.setStyleSheet(self.styler.labelStyle)

		self.magnitudeRxInput = QLineEdit("0")

		rxValidator = QIntValidator(0, 100)
		self.magnitudeRxInput.setValidator(rxValidator)
		self.magnitudeRxInput.textChanged.connect(self.magnitudeRxInputChanged)

		magnitudeRxLayout = QHBoxLayout()
		magnitudeRxLayout.setSpacing(2)
		magnitudeRxLayout.addWidget(self.magnitudeRxLabel)
		magnitudeRxLayout.addWidget(self.magnitudeRxInput)

		self.magnitudeRxSlider = QSlider(Qt.Horizontal)
		self.magnitudeRxSlider.setMinimum(0)
		self.magnitudeRxSlider.setMaximum(100)
		self.magnitudeRxSlider.setSingleStep(1)
		self.magnitudeRxSlider.setTickInterval(10)
		self.magnitudeRxSlider.setTickPosition(QSlider.TicksBelow)
		self.magnitudeRxSlider.setTracking(False)
		self.magnitudeRxSlider.valueChanged.connect(self.magnitudeRxSliderValueChanged)
		self.magnitudeRxSlider.sliderMoved.connect(self.magnitudeRxSliderMoved)

		self.setMarkerButton = QPushButton("Set Marker")
		self.setMarkerButton.setToolTip("Set marker in log data")
		self.setMarkerButton.setStyleSheet(self.styler.buttonStyle)
		self.setMarkerButton.clicked.connect(self.onSetMarkerButtonClicked)

		slidersSettingsLayout = QVBoxLayout()
		slidersSettingsLayout.addSpacing(8)
		slidersSettingsLayout.addLayout(magnitudeLxLayout)
		slidersSettingsLayout.addWidget(self.magnitudeLxSlider)
		slidersSettingsLayout.addLayout(magnitudeRxLayout)
		slidersSettingsLayout.addWidget(self.magnitudeRxSlider)
		slidersSettingsLayout.addWidget(self.setMarkerButton)

		self.slidersSettingsFrame = QFrame()
		self.slidersSettingsFrame.setLayout(slidersSettingsLayout)
		self.styler.addShadow(self.slidersSettingsFrame)

	def createProfileSettings(self):

		self.profileSettingsFrame = ProfileFrame(self.socketController)
		self.styler.addShadow(self.profileSettingsFrame)

	def manageLayouts(self):
		
		mainLayout = QHBoxLayout()
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

	def onConnectionStatusChanged(self, status):

		self.connectionOpened = status
		if (self.connectionOpened):
			self.connectionStatusLabel.setText("Status: Connected")
			self.streamButton.setEnabled(True)

			self.connectButton.setText("  Disconnect")
			self.connectButton.setToolTip("Disconnect")
			self.connectButton.setIcon(self.disconnectIcon)
		else:
			self.connectionStatusLabel.setText("Status: No connection")
			self.addMessageToLogger("Connection failed to the server.")
			self.streamButton.setEnabled(False)

			self.connectButton.setText("  Connect")
			self.connectButton.setToolTip("Connect to the server")
			self.connectButton.setIcon(self.connectIcon)

	def onConnectButtonClicked(self):

		if self.connectionOpened:
			self.socketController.resetConnection()
		else:
			self.socketController.startConnection()

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

		self.magnitudeLxInput.setText("{}".format(value))

	def magnitudeRxSliderValueChanged(self, value):
		
		self.magnitudeRxSliderMoved(value)
		self.socketController.magnitudeScalingRXChanged(value)

	def magnitudeRxSliderMoved(self, value):

		self.magnitudeRxInput.setText("{}".format(value))

	def onLogButtonClicked(self):
		participantId = self.participantIdLineEdit.text().strip()
		self.socketController.logData(participantId, self.logDirPath)

	def magnitudeLxInputChanged(self, value):
		
		if value == "":
			value = 0
		else:
			value = int(value)
		self.magnitudeLxSlider.setValue(value)

	def magnitudeRxInputChanged(self, value):
		
		if value == "":
			value = 0
		else:
			value = int(value)
		self.magnitudeRxSlider.setValue(value)

	def onBrowseButtonClicked(self):

		logDirPath = QFileDialog.getExistingDirectory(self, "Select Log Filre Directory", ".", QFileDialog.ShowDirsOnly)
		if logDirPath:
			self.logLineEdit.setText(logDirPath)
			self.logDirPath = logDirPath