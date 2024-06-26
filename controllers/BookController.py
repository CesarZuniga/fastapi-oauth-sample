from fastapi import HTTPException, Depends,status,APIRouter
from services.UserService import UserService
from services.BookService import BookService
from DTOs.Book import Book
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login")

book_controller_router = APIRouter()
bookService = BookService()
userService = UserService()
class BookController:
    #def __init__(self):
        

    @book_controller_router.get("/all")
    def get_books(token: str = Depends(oauth2_scheme)):
        try:
            usr = userService.authenticate(token)
            if usr is not False:
                return bookService.get_books()
            else:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User Unauthorized")
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=repr(e))

    @book_controller_router.get("/{id_book}")
    def get_book_by_id(id_book: int, token: str = Depends(oauth2_scheme)):
        try:
            usr = userService.authenticate(token)
            if usr is not False:
                return bookService.get_books_by_id(id_book)
            else:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User Unauthorized")
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=repr(e))

    @book_controller_router.post("/")
    def create_book(book: Book, token: str = Depends(oauth2_scheme)):
        try:
            usr = userService.authenticate(token)
            if usr is not False:
                bookService.create_book(book)
                return book
            else:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User Unauthorized")
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=repr(e))

