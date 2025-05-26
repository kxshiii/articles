# Article model for Object Relations Code Challenge
from lib.db.connection import get_connection

class Article:
    def __init__(self, title, author, magazine, id=None):
        if not isinstance(title, str) or not title.strip():
            raise ValueError("Article title must be a non-empty string.")
        self.id = id
        self.title = title.strip()
        self.author = author
        self.magazine = magazine

    def save(self):
        conn = get_connection()
        try:
            with conn:
                if self.id is None:
                    cursor = conn.execute(
                        "INSERT INTO articles (title, author_id, magazine_id) VALUES (?, ?, ?)",
                        (self.title, self.author.id, self.magazine.id)
                    )
                    self.id = cursor.lastrowid
                else:
                    conn.execute(
                        "UPDATE articles SET title=?, author_id=?, magazine_id=? WHERE id=?",
                        (self.title, self.author.id, self.magazine.id, self.id)
                    )
        finally:
            conn.close()

    @classmethod
    def find_by_id(cls, id):
        from lib.models.author import Author
        from lib.models.magazine import Magazine
        conn = get_connection()
        try:
            row = conn.execute("SELECT * FROM articles WHERE id=?", (id,)).fetchone()
            if row:
                author = Author.find_by_id(row["author_id"])
                magazine = Magazine.find_by_id(row["magazine_id"])
                return cls(row["title"], author, magazine, row["id"])
            return None
        finally:
            conn.close()
