from fastapi import HTTPException, Depends, Header,Response,status,APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from services.UserService import UserService
from DTOs.User import User

user_controller_router = APIRouter()
userService = UserService()

class UserController:
    # def __init__(self):
    #     self.userService = UserService()

    @user_controller_router.post("/register")
    def register(user: User):
        try:
            usr = userService.register(user)
            if usr is not False:
                return Response(status_code=status.HTTP_200_OK, content=f"User {user.username} registered successfully.")
            else:
                raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="User already exists")
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=repr(e))

    @user_controller_router.post("/login")
    def get_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
        try:
            access_token = userService.get_access_token(form_data)
            if access_token["access_token"] is None:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect username or password")
            return access_token
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=repr(e))

    @user_controller_router.post("/logout")
    def logout(token: str = Header(None)):
        try:
            if token is None: raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
            userService.logout(token)
            return Response(status_code=status.HTTP_200_OK, content="Logged out successfully")
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=repr(e))