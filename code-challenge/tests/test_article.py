import pytest
from lib.models.article import Article
from lib.models.author import Author
from lib.models.magazine import Magazine

@pytest.fixture(autouse=True)
def setup_and_teardown():
    from scripts.setup_db import setup_db
    setup_db()
    yield

def test_article_creation_and_find():
    alice = Author.find_by_name("Alice")
    tech = Magazine.find_by_id(1)
    article = Article("Test Article", alice, tech)
    article.save()
    found = Article.find_by_id(article.id)
    assert found is not None
    assert found.title == "Test Article"
    assert found.author.id == alice.id
    assert found.magazine.id == tech.id

def test_article_title_validation():
    alice = Author.find_by_name("Alice")
    tech = Magazine.find_by_id(1)
    with pytest.raises(ValueError):
        Article("", alice, tech)
    with pytest.raises(ValueError):
        Article(None, alice, tech)
