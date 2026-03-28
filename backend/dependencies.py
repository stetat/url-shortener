from fastapi import Depends, HTTPException, status
import jwt
from jwt.exceptions import InvalidTokenError
from pwdlib import PasswordHash
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from typing import Annotated, Union
from datetime import datetime, timezone, timedelta
from sqlmodel import select, Session
from database import engine
import time
from models import Users, User, TokenData
from config import ALPHABET, ALGORITHM, SECRET_KEY
from database import SessionDep

password_hash = PasswordHash.recommended()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def verify_password(plain_password, hashed_password):
    return password_hash.verify(plain_password, hashed_password)

def get_password_hash(password):
    return password_hash.hash(password)

def authenticate_user(session: SessionDep, username: str, password: str):
    user = session.exec(select(Users).where(Users.username==username)).first()
    if user is None:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc)
    if expires_delta:
        expire += expires_delta
    else:
        expire += timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_user(session: SessionDep, username: str):
    user = session.exec(select(Users).where(Users.username==username)).first()
    if user:
        return User(username=user.username, hashed_password=user.hashed_password)
    return None

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], session: SessionDep):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Couldn't validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception
    
    user = get_user(session=session, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


def encode_link(num: int) -> str:
    if num == 0:
        return ALPHABET[0]
    
    result = ""
    while num > 0:
        num, remainder = divmod(num, 62)
        result = ALPHABET[remainder] + result
    return result


def write_notis(message: str):
    with open("log.txt", mode="a") as email_file:
        email_file.write(message)

