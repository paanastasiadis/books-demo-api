# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring

""" Wings assignment """

from flask import Flask, jsonify, request
import requests
from flask_sqlalchemy import SQLAlchemy
from db import db
import requests
from populate_db import populate_db
from config.config import config

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
                    msg = populate_db(book, authors, works)

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


# Create the database tables if they do not exist
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
