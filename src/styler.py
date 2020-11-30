from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QColor

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

        self.labelStyle = """
            QLabel {
                font-size: 12px;
            }
        """

    def addShadow(self, widget):
        
        effect = QtWidgets.QGraphicsDropShadowEffect()
        effect.setBlurRadius(8)
        effect.setXOffset(0)
        effect.setYOffset(0)
        effect.setColor(QColor(65,88,134))
        widget.setGraphicsEffect(effect);  