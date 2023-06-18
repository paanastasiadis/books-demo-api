from db import db
from models.associations.book_work_association import book_work_assoc_table


class Work(db.Model):
    __tablename__ = "works"
    id = db.Column(db.String, primary_key=True)
    title = db.Column(db.String, nullable=False)
    books = db.relationship(
        "Book", secondary=book_work_assoc_table, back_populates="works"
    )

    def __init__(self, id, title):
        self.id = id
        self.title = title

    def __repr__(self):
        return f"({self.id}) {self.title}"
