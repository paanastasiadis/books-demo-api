from db import db

book_work_assoc_table = db.Table('book_work_association',
    db.Column('book_id', db.String, db.ForeignKey('books.id')),
    db.Column('work_id', db.String, db.ForeignKey('works.id'))
)
