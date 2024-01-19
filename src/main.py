import sys
from PySide6.QtWidgets import QMainWindow, QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QTextEdit, QListView
from PySide6.QtCore import Slot, QAbstractListModel, Qt, QItemSelection
from PySide6.QtGui import QAction
from data import NoteManager

class NoteListModel(QAbstractListModel):
    def __init__(self, manager: NoteManager) -> None:
        super().__init__()
        self.manager = manager
    
    def data(self, index, role) -> str:
        if role == Qt.DisplayRole:
            _, note_title = self.manager.get_id_title()[index.row()]
            return note_title
        if role == Qt.UserRole:
            note_id, _ = self.manager.get_id_title()[index.row()]
            return self.manager.get_note_text_by_id(note_id)
    
    def rowCount(self, parent) -> int:
        return len(self.manager.get_id_title())
        
class NoteView(QWidget):
    def __init__(self, note_list_model: NoteListModel) -> None:
        QWidget.__init__(self)
        
        self.search_bar = QLineEdit()
        self.note_list_view = QListView()
        self.note_list_view.setModel(note_list_model)
        self.note_list_view.selectionModel().selectionChanged.connect(self.set_edited_note)
        self.edit = QTextEdit()
        
        self.left = QVBoxLayout()
        self.left.addWidget(self.search_bar)
        self.left.addWidget(self.note_list_view)
        
        self.layout = QHBoxLayout()
        self.layout.addLayout(self.left)
        self.layout.addWidget(self.edit, 1)
        
        self.setLayout(self.layout)
    
    @Slot(QItemSelection, QItemSelection)
    def set_edited_note(self, selected: QItemSelection, deselected: QItemSelection):
        index = selected.indexes()[0]
        self.edit.setText(index.data(Qt.UserRole))

class MainWindow(QMainWindow):
    def __init__(self, widget) -> None:
        QMainWindow.__init__(self)
        self.setWindowTitle("Small Words")
        self.menu = self.menuBar()
        self.file_menu = self.menu.addMenu("File")
        
        exit_action = QAction("Exit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.exit_app)
        self.file_menu.addAction(exit_action)
        
        self.setCentralWidget(widget)
    
    @Slot()
    def exit_app(self):
        QApplication.quit()

if __name__ == "__main__":
    app = QApplication(sys.argv)

    manager = NoteManager("notes.db")
    note_list_model = NoteListModel(manager)

    widget = MainWindow(NoteView(note_list_model))
    widget.resize(800, 600)
    widget.show()

    sys.exit(app.exec())