# Seed data for Object Relations Code Challenge
from lib.models.author import Author
from lib.models.magazine import Magazine
from lib.models.article import Article

def seed():
    # Create authors
    alice = Author("Alice")
    bob = Author("Bob")
    carol = Author("Carol")
    alice.save()
    bob.save()
    carol.save()

    # Create magazines
    tech = Magazine("Tech Today", "Technology")
    food = Magazine("Foodies", "Cooking")
    travel = Magazine("Wanderlust", "Travel")
    tech.save()
    food.save()
    travel.save()

    # Create articles (7 total, varied relationships)
    Article("AI Revolution", alice, tech).save()
    Article("Python Tips", alice, tech).save()
    Article("Gourmet at Home", bob, food).save()
    Article("Street Food", carol, food).save()
    Article("Backpacking Europe", alice, travel).save()
    Article("Solo Travel", bob, travel).save()
    Article("Tech for Travelers", carol, tech).save()
