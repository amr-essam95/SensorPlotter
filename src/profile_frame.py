from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
import sys
sys.path.append(".")
from styler import Styler
import os

import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

class ProfileFrame(QtWidgets.QFrame): 
	def __init__(self, parent=None): 
		super().__init__(parent)

		self.profileButtonsFrame = ""
		self.profilePlotFrame = ""
		self.profileLineEdit = ""

		self.styler = Styler()

		self.createProfileButtons()
		self.createProfilePlot()
		self.manageLayouts()

	def createProfileButtons(self):

		chooseProfileLabel = QtWidgets.QLabel("Choose Profile")
		chooseProfileLabel.setMaximumHeight(40)
		chooseProfileLabel.setStyleSheet(self.styler.labelStyle)

		self.profileLineEdit = QtWidgets.QLineEdit()
		self.profileLineEdit.setStyleSheet(self.styler.browseLineEditStyle)
		self.profileLineEdit.setPlaceholderText("Profile path")
		self.profileLineEdit.setEnabled(False)

		browseIcon = QtGui.QIcon("../resources/browse.png")
		browseButton = QtWidgets.QPushButton()
		browseButton.setIcon(browseIcon)
		browseButton.setIconSize(QtCore.QSize(30,30))
		browseButton.clicked.connect(self.onBrowseButtonClicked)

		lineEditLayout = QtWidgets.QHBoxLayout()
		lineEditLayout.setContentsMargins(0,0,0,0)
		lineEditLayout.addWidget(self.profileLineEdit)
		lineEditLayout.addWidget(browseButton)

		lineEditFrame = QtWidgets.QFrame()
		lineEditFrame.setLayout(lineEditLayout)
		lineEditFrame.setStyleSheet(self.styler.browseLineEditFrame)

		setProfileButton = QtWidgets.QPushButton("Set Profile")
		setProfileButton.setToolTip("Set desired force profile")
		setProfileButton.setStyleSheet(self.styler.buttonStyle)
		setProfileButton.clicked.connect(self.onSetProfileClicked)

		profileButtonsLayout = QtWidgets.QVBoxLayout()
		profileButtonsLayout.addWidget(chooseProfileLabel)
		profileButtonsLayout.addWidget(lineEditFrame)
		profileButtonsLayout.addStretch()
		profileButtonsLayout.addWidget(setProfileButton)
		
		self.profileButtonsFrame = QtWidgets.QFrame()
		self.profileButtonsFrame.setLayout(profileButtonsLayout)

	def createProfilePlot(self):

		sc = MplCanvas(self, width=5, height=4, dpi=100)
		sc.axes.plot([0,1,2,3,4], [10,1,20,3,40])
		sc.axes.set_ylabel('Current (mA)', fontsize=10)
		sc.axes.set_xlabel('Gait cycle (%)', fontsize=10)

		toolbar = NavigationToolbar(sc, self)

		profilePlotLayout = QtWidgets.QVBoxLayout()
		# profilePlotLayout.addWidget(toolbar)
		profilePlotLayout.addWidget(sc)

		self.profilePlotFrame = QtWidgets.QFrame()
		self.profilePlotFrame.setLayout(profilePlotLayout)

	def manageLayouts(self):

		seperatorFrame = QtWidgets.QFrame()
		seperatorFrame.setFixedWidth(1)
		seperatorFrame.setStyleSheet(self.styler.seperatorStyle)
		seperatorFrame.setFrameShape(QtWidgets.QFrame.VLine)
		seperatorFrame.setFrameShadow(QtWidgets.QFrame.Sunken)
		
		mainLayout = QtWidgets.QHBoxLayout()
		mainLayout.setContentsMargins(2,2,2,2)
		mainLayout.setSpacing(10)
		mainLayout.addWidget(self.profileButtonsFrame, 1)
		mainLayout.addWidget(seperatorFrame)
		mainLayout.addWidget(self.profilePlotFrame, 2)
		self.setLayout(mainLayout)

	def plotProfileFile(self, profileFilePath):
		
		print ("will parse {}".format(profileFilePath))
		

	# Slots

	def onSetProfileClicked(self):

		print("setProfile clicked")

	def onBrowseButtonClicked(self):

		profileFileTuple = QtWidgets.QFileDialog.getOpenFileName(self, "Select Profile File", ".", "All files (*.*)")
		profileFilePath = profileFileTuple[0]
		if profileFilePath and os.path.exists(profileFilePath):
			self.profileLineEdit.setText(profileFilePath)
			self.plotProfileFile(profileFilePath)


class MplCanvas(FigureCanvasQTAgg):

	def __init__(self, parent=None, width=5, height=4, dpi=100):
		fig = Figure(figsize=(width, height), dpi=dpi)
		self.axes = fig.add_subplot(111)
		super(MplCanvas, self).__init__(fig)
