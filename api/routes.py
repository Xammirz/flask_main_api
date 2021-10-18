from flask import Flask, render_template, jsonify, request
from api.models import *
from api import app

@app.route("/")
def index():
    authors = Author.query.all()
    return render_template("index.html", authors=authors)


@app.route("/book", methods=["POST"])
def book():
    """Book a flight."""

    # Get form information.
    name = request.form.get("name")
    try:
        author_id = int(request.form.get("author_id"))
    except ValueError:
        return render_template("error.html", message="Invalid flight number.")


    # Make sure the flight exists.
    author = Author.query.get(author_id)
    if not author:
        return render_template("error.html", message="No such flight with that id.")

    # Add passenger.
    author.add_book(name)
    return render_template("success.html")


@app.route("/authors")
def authors():
    """List all flights."""
    authors = Author.query.all()
    return render_template("authors.html", authors=authors)


@app.route("/authors/<int:author_id>")
def author(author_id):
    """List details about a single flight."""

    # Make sure flight exists.
    author = Author.query.get(author_id)
    if author is None:
        return render_template("error.html", message="No such flight.")

    # Get all passengers.
    books = author.books
    return render_template("author.html", author=author, books=books)


@app.route("/api/authors/<int:author_id>")
def author_api(author_id):
    """Return details about a single flight."""

    # Make sure flight exists.
    author = Author.query.get(author_id)
    if author is None:
        return jsonify({"error": "Invalid flight_id"}), 422

    # Get all passengers.
    books = author.books
    names = []
    for book in books:
        names.append(book.name)
    return jsonify({
            "origin": author.name,
            "destination": author.surname,
            "passengers": names
        })
