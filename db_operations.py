from db import db
from models.Book import Book
from models.Author import Author
from models.Work import Work
from utils.db_utils import insert_book_to_db, get_instance, create_book_list_from_query
from sqlalchemy.orm import joinedload


def store_book_from_openlib(book):
    try:
        book_id = book["key"].split("/")[-1]

        if insert_book_to_db(session=db.session, book_data=book, from_openlib=True):
            return {"success": "Book {} was inserted successfully.".format(book_id)}
        else:
            return {"error": "Book {} already in the database".format(book_id)}
    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}


def get_all_books():
    query = db.session.query(Book).options(
        joinedload(Book.authors).load_only(Author.id, Author.name),
        joinedload(Book.works).load_only(Work.id, Work.title),
    )

    return create_book_list_from_query(query)


def get_books_by_query(author_name, work_title, min_pages):
    query = db.session.query(Book)

    if author_name:
        query = query.join(Book.authors).filter(Author.name.ilike(f"%{author_name}%"))

    if work_title:
        query = query.join(Book.works).filter(Work.title.ilike(f"%{work_title}%"))

    if min_pages:
        query = query.filter(Book.number_of_pages >= int(min_pages))

    books_query = query.all()

    return create_book_list_from_query(books_query)


def create_book(book_data):
    try:
        book_id = book_data.get("id")

        if insert_book_to_db(
            session=db.session, book_data=book_data, from_openlib=False
        ):
            return {"success": "Book {} was inserted successfully.".format(book_id)}
        else:
            return {"error": "Book {} already in the database".format(book_id)}
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
