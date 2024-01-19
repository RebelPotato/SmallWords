from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel
from PySide6.QtCore import Slot
from model import Note

class NoteWidget(QWidget):
    def __init__(self, note: Note):
        super().__init__()
        self.view_note(note)

    @Slot()
    def view_note(self, note: Note):
        self.note = note
        layout = QVBoxLayout()
        self.setLayout(layout)

        title_label = QLabel(note.title)
        content_label = QLabel(note.contents)

        layout.addWidget(title_label)
        layout.addWidget(content_label)


class NoteListWidget(QWidget):
    def __init__(self, notes: list[Note]):
        super().__init__()
        self.view_notes(notes)

    @Slot()
    def view_notes(self, notes: list[Note]):
        self.notes = notes
        layout = QVBoxLayout()
        self.setLayout(layout)

        for note in notes:
            title_label = QLabel(note.title)
            layout.addWidget(title_label)


class MainWidget(QWidget):
    def __init__(self, notes: list[Note]):
        super().__init__()
        self.setup_ui(notes[0], notes)

    def setup_ui(self, note: Note, notes: list[Note]):
        self.note = note
        self.notes = notes
        layout = QHBoxLayout()
        self.setLayout(layout)

        note_widget = NoteWidget(self.note)
        note_list_widget = NoteListWidget(self.notes)

        layout.addWidget(note_widget)
        layout.addWidget(note_list_widget)
    
    def view_note(self, note: Note):
        self.note = note
        note_widget = NoteWidget(self.note)
        self.layout().replaceWidget(self.layout().itemAt(0).widget(), note_widget)

