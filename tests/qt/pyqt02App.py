import sys
from PyQt6.QtWidgets import QApplication, QMainWindow
from pyqt02 import Ui_MainWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = QMainWindow()
    dialog = Ui_MainWindow()
    dialog.setupUi(window)
    window.show()
    app.exec()
