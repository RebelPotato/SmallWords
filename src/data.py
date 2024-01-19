import sqlite3
from datetime import datetime
from typing import List

class NoteManager:
    def __init__(self, db_name: str):
        self.db_name = db_name
        self.connect_to_database()
        self.create_tables()

    def connect_to_database(self):
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()

    def create_tables(self):
        """
        这个函数尚未记录。
        
        """
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS notes (
                note_id INTEGER PRIMARY KEY,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                previous_version INTEGER,
                age INTEGER,
                created_date TEXT NOT NULL,
                last_edit_date TEXT NOT NULL
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS links (
                link_id INTEGER PRIMARY KEY,
                note_id_1 INTEGER NOT NULL,
                note_id_2 INTEGER NOT NULL,
                FOREIGN KEY(note_id_1) REFERENCES notes(note_id),
                FOREIGN KEY(note_id_2) REFERENCES notes(note_id)
            )
        """)
        self.conn.commit()

    def add_note(self, title: str, content: str, previous_version: int=None):
        """
        Untested
        """
        created_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        last_edit_date = created_date
        next_review_date = created_date
        age = 0
        self.cursor.execute("""
            INSERT INTO notes (title, content, previous_version, age, created_date, last_edit_date)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (title, content, previous_version, age, created_date, last_edit_date))
        self.conn.commit()
        return self.cursor.lastrowid

    def get_id_title(self) -> List[tuple[int, str]]:
        """
        Retrieves all note ids and titles from the 'notes' table in the database.
        Returns a list of note ids and titles.
        """
        query = "SELECT note_id, title FROM notes"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def get_note_text_by_id(self, note_id: int) -> str:
        """
        Retrieves the content of a note with the given note_id from the 'notes' table in the database.
        Returns the content of the note as a string.
        """
        query = "SELECT content FROM notes WHERE note_id = ?"
        self.cursor.execute(query, (note_id,))
        result = self.cursor.fetchone()
        if result:
            return result[0]
        else:
            return ""
    
    