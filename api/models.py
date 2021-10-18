from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from api import db


class Author(db.Model):
    __tablename__ = "authors"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    surname = db.Column(db.String, nullable=False)
    books = db.relationship("Book", backref="author", lazy=True)
    def add_book(self, name):
        p = Book(name=name, author_id=self.id)
        db.session.add(p)
        db.session.commit()


class Book(db.Model):
    __tablename__ = "books"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey("authors.id"), nullable=False)
