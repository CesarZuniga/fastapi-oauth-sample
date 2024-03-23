from repositories.IUserRepository import IUserRepository
from db.DBContext import engine
from DTOs.User import User, ActiveSession
import os
from dotenv import load_dotenv
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import Depends,status
from passlib.context import CryptContext
from datetime import timedelta
from datetime import datetime
from jose import JWTError, jwt
from fastapi import HTTPException
from sqlmodel import Session, select, delete

dotenv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
load_dotenv(dotenv_path=dotenv_path)

# CryptContext for hashing passwords
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login")

class UserRepository(IUserRepository):
    def __init__(self):
        print("")


    def register(self, user: User):
        with Session(engine) as session:
            usr = session.exec(select(User).where(User.username == user.username)).first()
            if usr is None:
                user.password = pwd_context.hash(user.password)
                session.add(user)
                session.commit()
                session.refresh(user)
                return user
            else:
                return False

    def create_access_token(self, data: dict, expires_delta):
        to_encode = data.copy()
        expire = datetime.utcnow() + expires_delta
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, os.environ.get("SECRET_KEY"), algorithm=os.environ.get("ALGORITHM"))
        return encoded_jwt

    def get_user(self, username: str):
        with Session(engine) as session:
            usr = session.exec(select(User).where(User.username == username)).first()

        if usr is not None:
            return usr
        return None

    def is_password_correct(self, form_data: OAuth2PasswordRequestForm = Depends()) -> bool:
        user = self.get_user(form_data.username)

        if user is None or not pwd_context.verify(form_data.password, user.password):
            return False

        return True

    def get_access_token(self, form_data: OAuth2PasswordRequestForm = Depends()):
        access_token_expires = timedelta(minutes=int(os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES")))
        access_token = self.create_access_token(
            data={"sub": form_data.username}, expires_delta=access_token_expires
        )
        return access_token

    def authenticate(self, token: str):
        try:
            payload = jwt.decode(token, os.environ.get("SECRET_KEY"), algorithms=[os.environ.get("ALGORITHM")])
            username: str = payload.get("sub")
            if username is None:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Could not validate credentials, user not found.")

            # Check if the token has expired
            expiry_time = payload.get("exp")
            if expiry_time is None or expiry_time < datetime.utcnow().timestamp():
                with Session(engine) as session:
                    statement = delete(ActiveSession).where(ActiveSession.username == username)
                    session.exec(statement)
                    session.commit()
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication failed, invalid or expired token.")

            # Check if the username exists in the active sessions
            with Session(engine) as session:
                session = session.exec(select(ActiveSession).where(ActiveSession.username == username)).first()
            if not session:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User session not found.")

        except JWTError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication failed, invalid or expired token.")

    def register_token_in_session(self, token: str):
        try:
            payload = jwt.decode(token, os.environ.get("SECRET_KEY"), algorithms=[os.environ.get("ALGORITHM")])
            user, expiration_time = payload.get("sub"), payload.get("exp")
            expiration_datetime = datetime.utcfromtimestamp(expiration_time)

            new_active_session = ActiveSession(
                username=user,
                access_token=token,
                expiry_time=expiration_datetime
            )

            with Session(engine) as session:
                session.add(new_active_session)
                session.commit()
                session.refresh(new_active_session)
        except JWTError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication failed, invalid or expired token.")

    def logout(self, token: str):
        with Session(engine) as session:
            statement = delete(ActiveSession).where(ActiveSession.access_token == token)
            session.exec(statement)
            session.commit()

    def is_session_active(self, username: str):
        # First, check if the user has an active session
        with Session(engine) as session:
            existing_session = session.exec(select(ActiveSession).where(ActiveSession.username == username)).first()
        if not existing_session:
            return False

        # If an active session exists, check if the token is still valid
        try:
            payload = jwt.decode(existing_session.access_token, os.environ.get("SECRET_KEY"),
                                 algorithms=[os.environ.get("ALGORITHM")])
            expiry_time = payload.get("exp")
            current_time = datetime.utcnow().timestamp()

            if expiry_time is None or expiry_time < current_time:
                # Token has expired
                with Session(engine) as session:
                    statement = delete(ActiveSession).where(ActiveSession.username == username)
                    session.exec(statement)
                    session.commit()
                return False

        except JWTError:
            # there was an error in processing the token, delete the session and return false as session is no longer active.
            with Session(engine) as session:
                statement = delete(ActiveSession).where(ActiveSession.username == username)
                session.exec(statement)
                session.commit()
            return False

        return True

    def get_access_token_from_active_session(self, username: str):
        with Session(engine) as session:
            existing_session = session.exec(select(ActiveSession).where(ActiveSession.username == username)).first()
        if existing_session is not None:
            return existing_session.access_token
        return None