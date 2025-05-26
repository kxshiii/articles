Project Overview

The application models:





Authors: Write multiple articles.



Magazines: Publish multiple articles.



Articles: Belong to one author and one magazine.



Relationships: Authors and Magazines have a many-to-many relationship through Articles.

The project uses SQLite for simplicity, with parameterized SQL queries to ensure security and efficiency.
Database Schema

Defined in lib/db/schema.sql:





authors: id (PK, auto-increment), name (VARCHAR, NOT NULL, UNIQUE)



magazines: id (PK, auto-increment), name (VARCHAR, NOT NULL), category (VARCHAR, NOT NULL)



articles: id (PK, auto-increment), title (VARCHAR, NOT NULL), author_id (FK), magazine_id (FK)



Indexes: articles.author_id, articles.magazine_id for query performance.

Model Classes





Author:





Properties: id, name (non-empty string)



Methods: articles(), magazines(), add_article(magazine, title), topic_areas()



Class methods: find_by_id(id), find_by_name(name)



Magazine:





Properties: id, name, category (non-empty strings)



Methods: articles(), contributors(), article_titles(), contributing_authors() (>2 articles)



Class method: top_publisher()



Article:





Properties: id, title (non-empty string), author, magazine



Class method: find_by_id(id)

All SQL queries are parameterized to prevent SQL injection.

