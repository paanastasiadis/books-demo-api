from db import db

book_author_assoc_table = db.Table('book_author_association',
    db.Column('book_id', db.String, db.ForeignKey('books.id')),
    db.Column('author_id', db.String, db.ForeignKey('authors.id'))
)
