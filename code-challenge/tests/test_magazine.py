import pytest
from lib.models.magazine import Magazine
from lib.models.author import Author
from lib.models.article import Article

@pytest.fixture(autouse=True)
def setup_and_teardown():
    from scripts.setup_db import setup_db
    setup_db()
    yield

def test_magazine_creation_and_find():
    mag = Magazine("Science World", "Science")
    mag.save()
    found = Magazine.find_by_id(mag.id)
    assert found is not None
    assert found.name == "Science World"
    assert found.category == "Science"

def test_magazine_name_category_validation():
    with pytest.raises(ValueError):
        Magazine("", "Science")
    with pytest.raises(ValueError):
        Magazine("Science World", "")

def test_magazine_articles_and_contributors():
    tech = Magazine.find_by_id(1)
    articles = tech.articles()
    assert len(articles) >= 1
    contributors = tech.contributors()
    assert any(a.name == "Alice" for a in contributors)

def test_article_titles_and_contributing_authors():
    food = Magazine.find_by_id(2)
    titles = food.article_titles()
    assert "Gourmet at Home" in titles or "Street Food" in titles
    # Add more articles for Alice in food magazine to test contributing_authors
    alice = Author.find_by_name("Alice")
    food = Magazine.find_by_id(2)
    alice.add_article(food, "Alice's Food Article 1")
    alice.add_article(food, "Alice's Food Article 2")
    alice.add_article(food, "Alice's Food Article 3")
    authors = food.contributing_authors()
    assert any(a.name == "Alice" for a in authors)

def test_top_publisher():
    top = Magazine.top_publisher()
    assert top is not None
    assert isinstance(top, Magazine)
