import pytest
from lib.models.author import Author
from lib.models.magazine import Magazine
from lib.models.article import Article
from lib.db.connection import get_connection

@pytest.fixture(autouse=True)
def setup_and_teardown():
    from scripts.setup_db import setup_db
    setup_db()
    yield

def test_author_creation_and_find():
    author = Author("Test Author")
    author.save()
    found = Author.find_by_id(author.id)
    assert found is not None
    assert found.name == "Test Author"

def test_author_name_validation():
    with pytest.raises(ValueError):
        Author("")
    with pytest.raises(ValueError):
        Author(None)

def test_author_articles_and_magazines():
    alice = Author.find_by_name("Alice")
    articles = alice.articles()
    assert len(articles) >= 1
    magazines = alice.magazines()
    assert any(mag.name == "Tech Today" for mag in magazines)

def test_add_article_and_topic_areas():
    alice = Author.find_by_name("Alice")
    travel = Magazine.find_by_id(3)
    article = alice.add_article(travel, "New Adventures")
    assert article.title == "New Adventures"
    assert travel.category in alice.topic_areas()
