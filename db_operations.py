"""
Database operations for storing, retrieving, and removing books.
"""

from db import db
from models.Book import Book
from models.Author import Author
from models.Work import Work
from utils.db_utils import insert_book_to_db, get_instance, create_book_list_from_query
from sqlalchemy.orm import joinedload

def store_book(book_data, from_openlib=False):
    """Stores a book in the database.

    Args:
        book_data (dict): The data of the book to be stored.
        from_openlib (bool, optional): Indicates if the book data is from OpenLib. Defaults to False.

    Returns:
        dict: A dictionary with the result of the operation.
            If successful, it contains a 'success' message.
            If the book already exists in the database, it contains an 'error' message.
            If an exception occurs, it contains an 'error' message.
    """
    try:
        if from_openlib:
            # Extract the book id from the openlib book data
            book_id = book_data["key"].split("/")[-1]
        else:
            # Get the book id from the book data
            book_id = book_data.get("id")

        # Insert the book into the database
        if insert_book_to_db(
            session=db.session, book_data=book_data, from_openlib=from_openlib
        ):
            return {"success": "Book {} was inserted successfully.".format(book_id)}
        else:
            return {"error": "Book {} already in the database".format(book_id)}
    except Exception as e:
        # Roll back the database session in case of an exception
        db.session.rollback()
        return {"error": str(e)}


def retrieve_all_books():
    """Retrieves all books from the database.

    Returns:
        list: A list of books, including the related authors and works.
    """
    # Query all books from the database and include the related authors and works
    query = db.session.query(Book).options(
        joinedload(Book.authors).load_only(Author.id, Author.name),
        joinedload(Book.works).load_only(Work.id, Work.title),
    )
    # Create and return a list of books from the query results
    return create_book_list_from_query(query)


def retrieve_books_by_criteria(author_name, work_title, min_pages):
    """Retrieves books from the database based on specified criteria.

    Args:
        author_name (str): The name of the author to filter the books by.
        work_title (str): The title of the work to filter the books by.
        min_pages (int): The minimum number of pages a book should have.

    Returns:
        list: A list of books that match the specified criteria.
    """
    # Start with a query for all books
    query = db.session.query(Book)

    # Add filters based on the query parameters
    if author_name:
        # Join the authors table and filter by author name
        query = query.join(Book.authors).filter(Author.name.ilike(f"%{author_name}%"))

    if work_title:
        # Join the works table and filter by work title
        query = query.join(Book.works).filter(Work.title.ilike(f"%{work_title}%"))

    if min_pages:
        # Filter by minimum number of pages
        query = query.filter(Book.number_of_pages >= int(min_pages))

    # Execute the query and retrieve the results
    books_query = query.all()

    # Convert and the query results to a list of books and return the results
    return create_book_list_from_query(books_query)


def remove_book(book_id):
    """Removes a book from the database.

    Args:
        book_id (int): The ID of the book to be removed.

    Returns:
        None: If no book was found, it returns None

        dict: A dictionary indicating the result of the operation. If the book
        is successfully deleted, it contains a 'success' key with a success message.
        If the book doesn't exist or an error occurs, it contains an 'error' key
        with an error message.
    """

    # Retrieve the book instance from the database
    book = get_instance(db.session, Book, id=book_id)
    # If the book doesn't exist, return None

    if not book:
        return None

    try:
        # Get the associated authors and works of the book
        authors = [author for author in book.authors]
        works = [work for work in book.works]

        # Remove the book from its associated authors
        for author in authors:
            author.books.remove(book)

            # If an author has no more associated books, delete the author
            if len(author.books) < 1:
                db.session.delete(author)

        # Remove the book from its associated works
        for work in works:
            work.books.remove(book)

            # If a work has no more associated books, delete the work
            if len(work.books) < 1:
                db.session.delete(work)

        # Delete the book from the database
        db.session.delete(book)
        db.session.commit()
        return {"success": "Book {} was deleted successfully.".format(book.get("id"))}
    except Exception as e:
        # Roll back the database session in case of an exception
        db.session.rollback()
        return {"error": "Book was not deleted. Reason: {}.".format(e)}
