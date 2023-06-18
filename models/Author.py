from db import db
from models.associations.book_author_association import book_author_assoc_table


class Author(db.Model):
    __tablename__ = "authors"
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String, nullable=False)
    books = db.relationship(
        "Book", secondary=book_author_assoc_table, back_populates="authors"
    )

    def __init__(self, id, name):
        self.id = id
        self.name = name

    def __repr__(self):
        return f"({self.id}) {self.name}"
