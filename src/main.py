from PyQt5.QtWidgets import QApplication
from main_window import MainWindow

import sys
sys.path.append(".")

# create pyqt5 app 
App = QApplication(sys.argv) 
  
# create the instance of our Window 
window = MainWindow()
  
# start the app 
sys.exit(App.exec())