import sys
from PySide6.QtWidgets import QMainWindow, QApplication
from PySide6.QtCore import Slot
from PySide6.QtGui import QAction

class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setWindowTitle("Small Words")
        self.menu = self.menuBar()
        self.file_menu = self.menu.addMenu("File")
        
        exit_action = QAction("Exit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.exit_app)
        
        self.file_menu.addAction(exit_action)
    
    @Slot()
    def exit_app(self):
        QApplication.quit()

if __name__ == "__main__":
    app = QApplication(sys.argv)

    widget = MainWindow()
    widget.resize(800, 600)
    widget.show()

    sys.exit(app.exec())