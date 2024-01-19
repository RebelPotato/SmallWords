import sqlite3

class Note:
    def __init__(self, id: int, title: str, contents: str, previous_version: int=None):
        self.id = id
        self.title = title
        self.contents = contents
        self.previous_version = previous_version

class Notes:
    def __init__(self):
        self.connection = sqlite3.connect('notes.db')
        self.cursor = self.connection.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS notes
                               (id INTEGER PRIMARY KEY AUTOINCREMENT,
                                title TEXT,
                                contents TEXT,
                                previous_version INTEGER)''')
        self.connection.commit()

    def add_note(self, note: Note):
        self.cursor.execute('''INSERT INTO notes (title, contents, previous_version)
                               VALUES (?, ?, ?)''',
                            (note.title, note.contents, note.previous_version))
        self.connection.commit()

    def get_all_notes(self):
        self.cursor.execute("SELECT * FROM notes")
        rows: list[Notes] = self.cursor.fetchall()
        return map(rows, lambda row : Note(row[0], row[1], row[2], row[3]))
    
    
