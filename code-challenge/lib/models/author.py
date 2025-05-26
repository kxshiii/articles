# Author model for Object Relations Code Challenge
from lib.db.connection import get_connection

class Author:
    def __init__(self, name, id=None):
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Author name must be a non-empty string.")
        self.id = id
        self.name = name.strip()

    def save(self):
        conn = get_connection()
        try:
            with conn:
                if self.id is None:
                    cursor = conn.execute(
                        "INSERT INTO authors (name) VALUES (?)", (self.name,)
                    )
                    self.id = cursor.lastrowid
                else:
                    conn.execute(
                        "UPDATE authors SET name=? WHERE id=?", (self.name, self.id)
                    )
        finally:
            conn.close()

    @classmethod
    def find_by_id(cls, id):
        conn = get_connection()
        try:
            row = conn.execute("SELECT * FROM authors WHERE id=?", (id,)).fetchone()
            return cls(row["name"], row["id"]) if row else None
        finally:
            conn.close()

    @classmethod
    def find_by_name(cls, name):
        conn = get_connection()
        try:
            row = conn.execute("SELECT * FROM authors WHERE name=?", (name,)).fetchone()
            return cls(row["name"], row["id"]) if row else None
        finally:
            conn.close()

    def articles(self):
        from lib.models.article import Article
        from lib.models.magazine import Magazine
        conn = get_connection()
        try:
            rows = conn.execute(
                "SELECT * FROM articles WHERE author_id=?", (self.id,)
            ).fetchall()
            return [Article(row["title"], self, Magazine.find_by_id(row["magazine_id"]), row["id"]) for row in rows]
        finally:
            conn.close()

    def magazines(self):
        from lib.models.magazine import Magazine
        conn = get_connection()
        try:
            rows = conn.execute(
                "SELECT DISTINCT m.* FROM magazines m JOIN articles a ON m.id = a.magazine_id WHERE a.author_id=?",
                (self.id,)
            ).fetchall()
            return [Magazine(row["name"], row["category"], row["id"]) for row in rows]
        finally:
            conn.close()

    def add_article(self, magazine, title):
        from lib.models.article import Article
        if not hasattr(magazine, 'id'):
            raise ValueError("magazine must be a Magazine instance")
        if not isinstance(title, str) or not title.strip():
            raise ValueError("title must be a non-empty string")
        article = Article(title.strip(), self, magazine)
        article.save()
        return article

    def topic_areas(self):
        conn = get_connection()
        try:
            rows = conn.execute(
                "SELECT DISTINCT m.category FROM magazines m JOIN articles a ON m.id = a.magazine_id WHERE a.author_id=?",
                (self.id,)
            ).fetchall()
            return [row["category"] for row in rows]
        finally:
            conn.close()
