# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring

""" Wings assignment """

from flask import Flask, jsonify, request
import requests
from db import db
import requests
from populate_db import (
    store_book_from_openlib,
    get_all_books,
    get_books_by_query,
    create_book,
)
from config.config import config

from sqlalchemy.orm import joinedload

URL_BASE = "https://openlibrary.org{}.json"

app = Flask(__name__)
app.config.update(config)
db.init_app(app)


def fetch_data(code):
    url = URL_BASE.format(code)
    response = requests.get(url)
    response.raise_for_status()  # Raise an exception for non-2xx status codes

    return response.json()


@app.route("/retrieve_openlib_books", methods=["POST"])
def retrieve_books_from_openlib():
    data = request.get_json()

    if "codes" in data:
        skipped_books = []
        added_books = []

        for code in data["codes"]:
            try:
                book = fetch_data("/books/" + code)

                if "authors" in book and "works" in book:
                    authors = []
                    for i in range(0, len(book["authors"])):
                        author = fetch_data(book["authors"][i]["key"])
                        authors.append(author)

                    works = []
                    for i in range(0, len(book["works"])):
                        work = fetch_data(book["works"][i]["key"])
                        works.append(work)
                    msg = store_book_from_openlib(book, authors, works)

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


# Database population script
@app.route("/retrieve_book/<book_code>", methods=["POST"])
def retrieve_book(book_code):
    try:
        data = fetch_data("/books/" + book_code)
        # Process the data returned by fetch_data() if no exception occurred
        return ("Data: \n{}").format(str(data))
    except Exception as e:
        # Handle the exception
        return ("An exception occurred: \n{}").format(str(e))


@app.route("/books", methods=["GET"])
def retrieve_books():
    books = get_all_books()

    return jsonify({"books": books})


@app.route("/books/search", methods=["GET"])
def retrieve_books_by_query():
    author_name = request.args.get("author")
    work_title = request.args.get("work")
    min_pages = request.args.get("min_pages")
    # Check if at least one query parameter is provided
    if not author_name and not work_title and not min_pages:
        return jsonify({"error": "At least one query parameter is required."}), 400

    books = get_books_by_query(author_name, work_title, min_pages)

    return jsonify({"books": books})


def are_fields_valid(request_data):
    # Check if all the required fields are present in the request data
    if (
        "id" in request_data
        and "title" in request_data
        and "authors" in request_data
        and "works" in request_data
    ):
        for author in request_data["authors"]:
            if "id" not in author or "name" not in author:
                return False
        for work in request_data["works"]:
            if "id" not in work or "title" not in work:
                return False
        return True
    else:
        return False


@app.route("/books", methods=["POST"])
def store_book():
    data = request.get_json()
    if are_fields_valid(data):
        try:
            msg = create_book(data)
            return jsonify(msg, 200)
        except Exception as e:
            return jsonify({data.get("id"): "Book was not inserted due to: {}\n".format(e)})
    else:
        return jsonify({"error": "Missing required fields in the request data."}), 400


# Create the database tables if they do not exist
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)

# John%20Doe&work=Python%20Programming
