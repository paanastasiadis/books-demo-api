from db import db
from models.Book import Book
from models.Author import Author
from models.Work import Work
from utils.db.get_or_create import get_or_create, get_instance


def populate_db(book, authors, works):
    try:
        book_key = book["key"].split("/")[-1]

        # check if the book already exists
        existing_book = get_instance(db.session, Book, id=book_key)

        if existing_book != None:
            return {"error": "Book already in the database"}
        else:
            if "number_of_pages" in book:
                number_of_pages = book["number_of_pages"]
            else:
                number_of_pages = None

            new_book = Book(
                id=book_key, title=book["title"], number_of_pages=number_of_pages
            )

            # Add the book to the session
            db.session.add(new_book)

            for author in authors:
                author_key = author["key"].split("/")[-1]

                new_author = get_or_create(
                    db.session, Author, id=author_key, name=author["name"]
                )
                new_book.authors.append(new_author)

                # Add the author to the session
                db.session.add(new_author)

            for work in works:
                work_key = work["key"].split("/")[-1]

                new_work = get_or_create(
                    db.session, Work, id=work_key, title=work["title"]
                )
                new_book.works.append(new_work)

                # Add the author to the session
                db.session.add(new_work)

            db.session.commit()  # Commit after adding each author
            return {"success": "Book {} was inserted successfully.".format(book_key)}
    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}
