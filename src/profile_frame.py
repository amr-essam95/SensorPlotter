from PyQt5.QtWidgets import QFrame, QPushButton, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon

import sys
sys.path.append(".")
from styler import Styler
import os

from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg

import csv

class ProfileFrame(QFrame): 
	def __init__(self, socketController, parent=None): 
		super().__init__(parent)

		self.profileButtonsFrame = ""
		self.profilePlotFrame = ""
		self.profileLineEdit = ""
		self.profilePlot = ""
		self.profileIntList = [0] * 100

		self.styler = Styler()

		self.socketController = socketController

		self.createProfileButtons()
		self.createProfilePlot()
		self.manageLayouts()

	def createProfileButtons(self):

		chooseProfileLabel = QLabel("Choose Profile")
		chooseProfileLabel.setMaximumHeight(40)
		chooseProfileLabel.setStyleSheet(self.styler.labelStyle)

		self.profileLineEdit = QLineEdit()
		self.profileLineEdit.setStyleSheet(self.styler.browseLineEditStyle)
		self.profileLineEdit.setPlaceholderText("Profile path")
		self.profileLineEdit.setEnabled(False)

		browseIcon = QIcon("resources/browse.png")
		browseButton = QPushButton()
		browseButton.setIcon(browseIcon)
		browseButton.setIconSize(QSize(30,30))
		browseButton.clicked.connect(self.onBrowseButtonClicked)

		lineEditLayout = QHBoxLayout()
		lineEditLayout.setContentsMargins(0,0,0,0)
		lineEditLayout.addWidget(self.profileLineEdit)
		lineEditLayout.addWidget(browseButton)

		lineEditFrame = QFrame()
		lineEditFrame.setLayout(lineEditLayout)
		lineEditFrame.setStyleSheet(self.styler.browseLineEditFrame)

		setProfileButton = QPushButton("Set Profile")
		setProfileButton.setToolTip("Set desired force profile")
		setProfileButton.setStyleSheet(self.styler.buttonStyle)
		setProfileButton.clicked.connect(self.onSetProfileClicked)

		profileButtonsLayout = QVBoxLayout()
		profileButtonsLayout.addWidget(chooseProfileLabel)
		profileButtonsLayout.addWidget(lineEditFrame)
		profileButtonsLayout.addStretch()
		profileButtonsLayout.addWidget(setProfileButton)
		
		self.profileButtonsFrame = QFrame()
		self.profileButtonsFrame.setLayout(profileButtonsLayout)

	def createProfilePlot(self):

		self.profilePlot = pg.PlotWidget()

		blackColor = (0,0,0)

		self.profilePlot.setBackground('w')
		self.profilePlot.setTitle("<span style=\"color:black; font-size:15pt\">Profile Plot</span>")

		styles = {'color':'rgba(0,0,0,1)', 'font-size':'15px'}
		self.profilePlot.getAxis('left').setPen(color=blackColor)
		self.profilePlot.getAxis('bottom').setPen(color=blackColor)

		self.profilePlot.getAxis('left').setTextPen(color=blackColor)
		self.profilePlot.getAxis('bottom').setTextPen(color=blackColor) 

		self.profilePlot.setLabel('left', 'Current (mA)', **styles)
		self.profilePlot.setLabel('bottom', 'Gait cycle (%)', **styles)

		profilePlotLayout = QVBoxLayout()
		profilePlotLayout.addWidget(self.profilePlot)

		self.profilePlotFrame = QFrame()
		self.profilePlotFrame.setLayout(profilePlotLayout)

	def manageLayouts(self):

		seperatorFrame = QFrame()
		seperatorFrame.setFixedWidth(1)
		seperatorFrame.setStyleSheet(self.styler.seperatorStyle)
		seperatorFrame.setFrameShape(QFrame.VLine)
		seperatorFrame.setFrameShadow(QFrame.Sunken)
		
		mainLayout = QHBoxLayout()
		mainLayout.setContentsMargins(2,2,2,2)
		mainLayout.setSpacing(10)
		mainLayout.addWidget(self.profileButtonsFrame, 1)
		mainLayout.addWidget(seperatorFrame)
		mainLayout.addWidget(self.profilePlotFrame, 2)
		self.setLayout(mainLayout)

	def plotProfileFile(self, profileFilePath):
		
		f = open(profileFilePath, "r")
		fileContent = f.read()
		profileStrList = fileContent.split(',')
		self.profileIntList = [int(i) for i in profileStrList] 
		
		x = range(0, 100, 1)

		blackPen = pg.mkPen(color=(0,0,0))
		self.profilePlot.clear()
		self.profilePlot.plot(x, self.profileIntList, pen=blackPen)

	# Slots

	def onSetProfileClicked(self):

		self.socketController.desiredForceProfileChanged(self.profileIntList)

	def onBrowseButtonClicked(self):

		profileFileTuple = QFileDialog.getOpenFileName(self, "Select Profile File", ".", "All files (*.*)")
		profileFilePath = profileFileTuple[0]
		if profileFilePath and os.path.exists(profileFilePath):
			self.profileLineEdit.setText(profileFilePath)
			self.plotProfileFile(profileFilePath)