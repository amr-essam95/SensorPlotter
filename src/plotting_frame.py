from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
import sys
sys.path.append(".")
from styler import Styler

class PlottingFrame(QtWidgets.QFrame): 
    def __init__(self, parent=None): 
        super().__init__() 

        self.styler = Styler()