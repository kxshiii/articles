# Magazine model for Object Relations Code Challenge
from lib.db.connection import get_connection

class Magazine:
    def __init__(self, name, category, id=None):
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Magazine name must be a non-empty string.")
        if not isinstance(category, str) or not category.strip():
            raise ValueError("Magazine category must be a non-empty string.")
        self.id = id
        self.name = name.strip()
        self.category = category.strip()

    def save(self):
        conn = get_connection()
        try:
            with conn:
                if self.id is None:
                    cursor = conn.execute(
                        "INSERT INTO magazines (name, category) VALUES (?, ?)", (self.name, self.category)
                    )
                    self.id = cursor.lastrowid
                else:
                    conn.execute(
                        "UPDATE magazines SET name=?, category=? WHERE id=?",
                        (self.name, self.category, self.id)
                    )
        finally:
            conn.close()

    @classmethod
    def find_by_id(cls, id):
        conn = get_connection()
        try:
            row = conn.execute("SELECT * FROM magazines WHERE id=?", (id,)).fetchone()
            return cls(row["name"], row["category"], row["id"]) if row else None
        finally:
            conn.close()

    def articles(self):
        from lib.models.article import Article
        from lib.models.author import Author
        conn = get_connection()
        try:
            rows = conn.execute(
                "SELECT * FROM articles WHERE magazine_id=?", (self.id,)
            ).fetchall()
            return [Article(row["title"], Author.find_by_id(row["author_id"]), self, row["id"]) for row in rows]
        finally:
            conn.close()

    def contributors(self):
        from lib.models.author import Author
        conn = get_connection()
        try:
            rows = conn.execute(
                "SELECT DISTINCT a.* FROM authors a JOIN articles ar ON a.id = ar.author_id WHERE ar.magazine_id=?",
                (self.id,)
            ).fetchall()
            return [Author(row["name"], row["id"]) for row in rows]
        finally:
            conn.close()

    def article_titles(self):
        conn = get_connection()
        try:
            rows = conn.execute(
                "SELECT title FROM articles WHERE magazine_id=?", (self.id,)
            ).fetchall()
            return [row["title"] for row in rows]
        finally:
            conn.close()

    def contributing_authors(self):
        from lib.models.author import Author
        conn = get_connection()
        try:
            rows = conn.execute(
                "SELECT a.*, COUNT(ar.id) as article_count FROM authors a "
                "JOIN articles ar ON a.id = ar.author_id WHERE ar.magazine_id=? "
                "GROUP BY a.id HAVING article_count > 2",
                (self.id,)
            ).fetchall()
            return [Author(row["name"], row["id"]) for row in rows]
        finally:
            conn.close()

    @classmethod
    def top_publisher(cls):
        conn = get_connection()
        try:
            row = conn.execute(
                "SELECT m.*, COUNT(a.id) as article_count FROM magazines m "
                "JOIN articles a ON m.id = a.magazine_id "
                "GROUP BY m.id ORDER BY article_count DESC LIMIT 1"
            ).fetchone()
            return cls(row["name"], row["category"], row["id"]) if row else None
        finally:
            conn.close()
