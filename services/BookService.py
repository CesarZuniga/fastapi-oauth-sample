from repositories.BookRepository import BookRepository
from DTOs.Book import Book


class BookService:
    def __init__(self):
        self.bookRepository = BookRepository()

    def get_books_by_id(self, id_book: int):
        return self.bookRepository.get_books_by_id(id_book=id_book)

    def get_books(self):
        return self.bookRepository.get_books()

    def create_book(self, data: Book):
        return self.bookRepository.create_book(data)
