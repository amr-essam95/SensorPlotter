from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QColor
import pyqtgraph as pg

class Styler:
	def __init__(self):
		self.roundedStyle = "border-radius: 3px;"
		
		self.borderStyle = "border: 1px solid black"

		self.buttonStyle = """
			QPushButton {
				border: 1px solid rgb(65,88,134);
				height: 30px;
				padding: 4px;
				font-size: 12px;
			}
			QPushButton::Pressed {
				border: 2px solid rgb(65,88,134);
			}
		"""

		self.lineEditStyle = """
			QLineEdit {
				border-bottom: 1px solid rgb(65,88,134);
				border-radius: 0px;
				height: 30px;
				font-size: 11px;
			}
		"""

		self.browseLineEditStyle = """
			QLineEdit {
				border-radius: 0px;
				height: 30px;
				font-size: 11px;
			}
			QLineEdit::disabled {
				color: black;
			}
		"""

		self.browseLineEditFrame = """
			QFrame {
				border-bottom: 1px solid rgb(65,88,134);
				border-radius: 0px;
			}
		"""

		self.labelStyle = """
			QLabel {
				font-size: 12px;
			}
		"""

		self.seperatorStyle = """
			QFrame {
				background-color: rgb(65,88,134);
			}
		"""

		self.browseButtonStyle = """
			QPushButton {
				border-bottom: 1px solid rgb(65,88,134);
				border-radius: 0px;
				height: 30px;
				font-size: 11px;
			}
		"""

		self.enableButtonStyle = """
			QPushButton {
				qproperty-icon: url('resources/path847.png');
			}
		"""

		self.labelOnStyle = """
			QLabel {
				font-size: 20px;
				color: white;
				background-color: transparent;
			}
		"""

		self.labelFrameOnStyle = """
			QFrame {
				background-color: green;
				border-radius: 40px;
			}
		"""

		self.labelOffStyle = """
			QLabel {
				font-size: 20px;
				color: black;
				background-color: transparent;
			}
		"""

		self.labelFrameOffStyle = """
			QFrame {
				background-color: rgb(230,230,230);
				border-radius: 40px;
			}
		"""

		self.enableLabel = """
			QPushButton {
				font-size : 15px;
			}
		"""

		self.buttonOnStyle = """
			QPushButton {
				background-color: rgb(65,88,134);
				border: 1px solid rgb(65,88,134);
				height: 30px;
				padding: 4px;
				font-size: 12px;
				color: white;
			}
			QPushButton::Pressed {
				border: 2px solid rgb(65,88,134);
				background-color: rgb(255,255,255);
				color: black;
			}
		"""

		self.connectionStatusLabel = """
			QLabel {
				margin-left: 1px;
				border: none;
			}
		"""

		self.loggerFrame = """
			QFrame {
				border: 1px solid rgb(65,88,134);
			}
		"""

		self.noBorder = """
			QFrame {
				border: none;
			}
		"""

		self.rxLegendBox = """
			QFrame {
				border: none;
				background-color: rgb(0,0,0);
			}
		"""

		self.rxLegendLabel = """
			QFrame {
				border: none;
				color: rgb(0,0,0);
				font-size: 13px;
			}
		"""

		self.lxLegendBox = """
			QFrame {
				border: none;
				background-color: rgb(44,90,160);
			}
		"""

		self.lxLegendLabel = """
			QFrame {
				border: none;
				color: rgb(44,90,160);
				font-size: 13px;
			}
		"""

		self.trunkLegendBox = """
			QFrame {
				border: none;
				background-color: rgb(170,0,0);
			}
		"""

		self.trunkLegendLabel = """
			QFrame {
				border: none;
				color: rgb(170,0,0);
				font-size: 13px;
			}
		"""

		self.blackPen = pg.mkPen(color=(0,0,0))
		self.blackDottedPen = pg.mkPen(color=(0,0,0), style=QtCore.Qt.DashLine)
		self.bluePen = pg.mkPen(color=(44,90,160))
		self.blueDottedPen = pg.mkPen(color=(44,90,160), style=QtCore.Qt.DashLine)
		self.redPen = pg.mkPen(color=(170,0,0))

		

	def addShadow(self, widget):
		
		effect = QtWidgets.QGraphicsDropShadowEffect()
		effect.setBlurRadius(8)
		effect.setXOffset(0)
		effect.setYOffset(0)
		effect.setColor(QColor(65,88,134))
		widget.setGraphicsEffect(effect);  