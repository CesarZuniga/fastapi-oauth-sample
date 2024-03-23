from repositories.IBookRepository import IBookRepository
from db.DBContext import engine
from DTOs.Book import Book
from sqlmodel import Session, select




class BookRepository(IBookRepository):

    def get_books_by_id(self, id_book: int):
        with Session(engine) as session:
            book = session.exec(select(Book).where(Book.id == id_book)).first()
            return book

    def get_books(self):
        with Session(engine) as session:
            books = session.exec(select(Book)).all()
            return books

    def create_book(self, data: Book):
        with Session(engine) as session:
            session.add(data)
            session.commit()
            session.refresh(data)


