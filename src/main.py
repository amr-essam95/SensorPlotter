import sys
sys.path.append(".")

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from main_window import MainWindow

  
# create pyqt5 app 
App = QtWidgets.QApplication(sys.argv) 
  
# create the instance of our Window 
window = MainWindow()
  
# start the app 
sys.exit(App.exec())