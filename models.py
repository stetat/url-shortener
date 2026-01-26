from pydantic import BaseModel
from sqlmodel import SQLModel, Field
from sqlalchemy import Column, String

class Users(SQLModel, table=True):
    id: int = Field(primary_key=True)
    username: str
    email: str
    hashed_password: str

class User(BaseModel):
    username: str
    hashed_password: str

class redirect_db(SQLModel, table=True):
    id: int = Field(primary_key=True)
    short_code: str = Field(sa_column=Column(String, unique=True, index=True))
    original_url: str = Field(sa_column=Column(String, unique=True, index=True))

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str