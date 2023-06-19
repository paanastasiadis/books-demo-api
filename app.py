"""
Book API.

This Flask application provides endpoints for managing books, including storing books from OpenLibrary, retrieving books, searching books based on criteria, creating new book entries, and deleting books.

Endpoints:

/store_openlib_books: Stores books from OpenLibrary.
/books: Retrieves all books from the database.
/books/search: Searches books based on specified criteria (author, work, number of pages).
/books: Creates a new book entry.
/books/<book_id>: Deletes a book.
"""

from flask import Flask, jsonify, request
from db import db
import db_operations
from utils.app_utils import fetch_data, validate_create_book_req_data
from config.config import config

app = Flask(__name__)
app.config.update(config)
db.init_app(app)


@app.route("/store_openlib_books", methods=["POST"])
def store_openlib_books():
    """
    Endpoint handler for storing books from OpenLibrary.
    """

    # Get the book data from the request
    data = request.get_json()

    if "codes" in data:
        skipped_books = []  # List to store skipped books
        added_books = []  # List to store successfully added books

        for code in data["codes"]:
            try:
                # Fetch data for the book using the provided code
                book = fetch_data("/books/" + code)

                if "authors" in book and "works" in book:
                    authors = []
                    # Fetch data for each author associated with the book
                    for i in range(0, len(book["authors"])):
                        author = fetch_data(book["authors"][i]["key"])
                        authors.append(author)

                    works = []
                    # Fetch data for each work associated with the book
                    for i in range(0, len(book["works"])):
                        work = fetch_data(book["works"][i]["key"])
                        works.append(work)

                    # Update the book data with the fetched author and work data
                    book["authors"] = authors
                    book["works"] = works

                    # Store the book in the database
                    msg = db_operations.store_book(book, from_openlib=True)

                    if "error" in msg:
                        skipped_books.append(
                            {code: "Skipped because of: {}".format(msg["error"])}
                        )
                    else:
                        added_books.append(code)

                else:
                    skipped_books.append({code: "Skipped because of: Missing fields"})

            except Exception as e:
                skipped_books.append({code: "Skipped because of: {}".format(e)})

        return (
            jsonify({"added_books": added_books, "skipped_books": skipped_books}),
            200,
        )
    else:
        return jsonify({"error": "Invalid code list provided."}), 400


@app.route("/books", methods=["GET"])
def get_all_books():
    """
    Endpoint handler for retrieving all books from the database.
    """
    # Retrieve all books from the database
    books = db_operations.retrieve_all_books()

    return jsonify({"books": books})


@app.route("/books/search", methods=["GET"])
def search_books():
    """
    Endpoint handler for searching books based on specified criteria:
        -(author or/and work or/and number of pages)
    """

    # Get the query parameters from the request
    author_name = request.args.get("author")
    work_title = request.args.get("work")
    min_pages = request.args.get("min_pages")

    # Check if at least one query parameter is provided
    if not author_name and not work_title and not min_pages:
        return jsonify({"error": "At least one query parameter is required."}), 400

    # Retrieve books based on the specified criteria
    books = db_operations.retrieve_books_by_criteria(author_name, work_title, min_pages)

    return jsonify({"books": books})


@app.route("/books", methods=["POST"])
def create_book():
    """
    Endpoint handler for creating a new book entry.
    """
    # Get the book data from the request
    data = request.get_json()

    # Check if the required fields are valid
    if validate_create_book_req_data(data):
        try:
            # Store the book in the database
            msg = db_operations.store_book(data, from_openlib=False)
            return jsonify(msg, 200)
        except Exception as e:
            return jsonify(
                {data.get("id"): "Book was not inserted due to: {}".format(e)}
            )
    else:
        return jsonify({"error": "Missing required fields in the request data."}), 400


@app.route("/books/<book_id>", methods=["DELETE"])
def delete_book(book_id):
    """
    Endpoint handler for deleting a book.
    """
    
    # Remove the book from the database
    msg = db_operations.remove_book(book_id)

    if msg == None:
        return jsonify({"error": "Book not found."}), 404

    if msg.get("error"):
        return jsonify(msg), 500
    else:
        return jsonify(msg), 200


# Create the database tables if they do not exist
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(host="0.0.0.0")
