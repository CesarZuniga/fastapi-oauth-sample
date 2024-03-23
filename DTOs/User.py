from sqlmodel import SQLModel, Field
from typing import Optional
import datetime


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str
    password: str


class ActiveSession(SQLModel, table=True):
    access_token: str = Field(default=None, primary_key=True)
    username: str
    expiry_time: datetime.datetime
