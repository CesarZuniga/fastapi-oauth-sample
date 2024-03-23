from abc import abstractmethod
from DTOs.Book import Book


class IBookRepository:

    @abstractmethod
    def create_book(self, data: Book): pass

    @abstractmethod
    def get_books(self): pass

    @abstractmethod
    def get_books_by_id(self, id_book: int): pass
