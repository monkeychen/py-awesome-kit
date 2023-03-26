import sys
from PyQt6.QtWidgets import QApplication, QDialog
from pyqt01 import Ui_Dialog

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = QDialog()
    dialog = Ui_Dialog()
    dialog.setupUi(window)
    window.show()
    app.exec()
