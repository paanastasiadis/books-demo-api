from db import db
from models.associations.book_author_association import book_author_assoc_table
from models.associations.book_work_association import book_work_assoc_table


class Book(db.Model):
    __tablename__ = "books"
    id = db.Column(db.String, primary_key=True)
    title = db.Column(db.String, nullable=False)
    number_of_pages = db.Column(db.Integer)
    authors = db.relationship(
        "Author",
        secondary=book_author_assoc_table,
        back_populates="books",
        cascade="all, delete",
    )
    works = db.relationship(
        "Work",
        back_populates="books",
        secondary=book_work_assoc_table,
        cascade="all, delete",
    )

    def __init__(self, id, title, number_of_pages):
        self.id = id
        self.title = title
        self.number_of_pages = number_of_pages

    def __repr__(self):
        return f"({self.id}) {self.title} {self.number_of_pages}"
