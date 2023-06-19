from db import db
from models.Book import Book
from models.Author import Author
from models.Work import Work
from utils.db.get_or_create import get_or_create, get_instance
from sqlalchemy.orm import joinedload


def store_book_from_openlib(book, authors, works):
    try:
        book_key = book["key"].split("/")[-1]

        # check if the book already exists
        existing_book = get_instance(db.session, Book, id=book_key)

        if existing_book != None:
            return {"error": "Book already in the database"}
        else:
            number_of_pages = book.get("number_of_pages")

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


def construct_book_list(books_query):
    book_list = []
    for book in books_query:
        authors = [{"id": author.id, "name": author.name} for author in book.authors]
        works = [{"id": work.id, "title": work.title} for work in book.works]

        print(book.number_of_pages)

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


def get_all_books():
    query = db.session.query(Book).options(
        joinedload(Book.authors).load_only(Author.id, Author.name),
        joinedload(Book.works).load_only(Work.id, Work.title),
    )

    return construct_book_list(query)


def get_books_by_query(author_name, work_title, min_pages):
    query = db.session.query(Book)

    if author_name:
        query = query.join(Book.authors).filter(Author.name.ilike(f"%{author_name}%"))

    if work_title:
        query = query.join(Book.works).filter(Work.title.ilike(f"%{work_title}%"))

    if min_pages:
        query = query.filter(Book.number_of_pages >= int(min_pages))

    books_query = query.all()

    return construct_book_list(books_query)


def create_book(data):
    try:
        # Extract the necessary fields for creating a new book
        book_id = data.get("id")
        title = data.get("title")
        number_of_pages = data.get("number_of_pages")
        authors = data.get("authors", [])
        works = data.get("works", [])

        # Create a new Book instance
        new_book = Book(id=book_id, title=title, number_of_pages=number_of_pages)

        # check if the book already exists
        existing_book = get_instance(db.session, Book, id=book_id)

        if existing_book != None:
            return {"error": "Book already in the database"}
        else:
            # Add authors to the new book
            for author in authors:
                author_id = author.get("id")
                author_name = author.get("name")

                new_author = get_or_create(
                    db.session, Author, id=author_id, name=author_name
                )
                new_book.authors.append(new_author)

                # Add the author to the session
                db.session.add(new_author)

            # Add works to the new book
            for work in works:
                work_id = work.get("id")
                work_title = work.get("title")

                new_work = get_or_create(db.session, Work, id=work_id, title=work_title)
                new_book.works.append(new_work)

                # Add the author to the session
                db.session.add(new_work)

            # Add the new book to the database session
            db.session.add(new_book)
            db.session.commit()

            return {"success": "Book {} was inserted successfully.".format(book_id)}
    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}


def delete_book_from_db(book_id):
    book = get_instance(db.session, Book, id=book_id)

    if not book:
        return None

    try:
        authors = [author for author in book.authors]
        works = [work for work in book.works]
        # Remove the book from its associated authors
        for author in authors:
            author.books.remove(book)
            if len(author.books) < 1:
                db.session.delete(author)

        for work in works:
            work.books.remove(book)
            if len(work.books) < 1:
                db.session.delete(work)

        # Delete the book from the database
        db.session.delete(book)
        db.session.commit()
        return {"success": "Book deleted successfully."}
    except Exception as e:
        db.session.rollback()
        return {"error": "Book was not deleted. Reason: {}.".format(e)}
