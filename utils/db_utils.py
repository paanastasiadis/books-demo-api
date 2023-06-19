"""
Utility functions for the database operations.

Functions:
- get_or_create_instance: Retrieve an instance from the session or create a new instance if not found.
- get_instance: Retrieve an instance from the session based on the provided kwargs.
- insert_book_to_db: Insert a book into the database with the associated authors and works if it doesn't already exist.
- create_book_list_from_query: Convert a query result of books into a list of book data dictionaries.
"""

from models.Book import Book
from models.Author import Author
from models.Work import Work

def get_or_create_instance(session, model, **kwargs):
    # Check if an instance with the given kwargs exists in the session
    instance = session.query(model).filter_by(**kwargs).first()

    if instance:
        # If an instance exists, return it
        return instance
    else:
        # If an instance doesn't exist, create a new instance with the given kwargs
        instance = model(**kwargs)
        session.add(instance)

        return instance


def get_instance(session, model, **kwargs):
    # Retrieve an instance with the given kwargs from the session
    instance = session.query(model).filter_by(**kwargs).first()
    return instance


def insert_book_to_db(session, book_data, from_openlib=False):
    if from_openlib:
        # Extract the book id from the openlib book data
        book_id = book_data["key"].split("/")[-1]
    else:
        # Get the book id from the book data
        book_id = book_data.get("id")

    title = book_data.get("title")
    number_of_pages = book_data.get("number_of_pages")
    authors = book_data.get("authors", [])
    works = book_data.get("works", [])

    existing_book = get_instance(session, Book, id=book_id)

    if existing_book != None:
        # If the book already exists in the database, return False
        return False
    else:
        new_book = Book(id=book_id, title=title, number_of_pages=number_of_pages)

        for author in authors:
            if from_openlib:
                # Extract the author id from the openlib author data
                author_id = author["key"].split("/")[-1]
            else:
                # Get the author id from the author data
                author_id = author.get("id")

            author_name = author.get("name")

            # Get or create an author instance with the given data
            new_author = get_or_create_instance(
                session, Author, id=author_id, name=author_name
            )
            new_book.authors.append(new_author)

            # Add the author to the session
            session.add(new_author)

        for work in works:
            if from_openlib:
                # Extract the work id from the openlib work data
                work_id = work["key"].split("/")[-1]
            else:
                # Get the work id from the work data
                work_id = work.get("id")
            work_title = work.get("title")

            # Get or create a work instance with the given data
            new_work = get_or_create_instance(
                session, Work, id=work_id, title=work_title
            )
            new_book.works.append(new_work)

            # Add the author to the session
            session.add(new_work)

        # Add the book to the session
        session.add(new_book)
        session.commit()
        return True


def create_book_list_from_query(books_query):
    book_list = []
    for book in books_query:
        authors = [{"id": author.id, "name": author.name} for author in book.authors]
        works = [{"id": work.id, "title": work.title} for work in book.works]

        book_data = {
            "id": book.id,
            "title": book.title,
            "authors": authors,
            "works": works,
        }
        if book.number_of_pages is not None:
            book_data["number_of_pages"] = book.number_of_pages

        book_list.append(book_data)
    return book_list
