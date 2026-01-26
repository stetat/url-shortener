from fastapi import APIRouter, HTTPException, status, Depends, Query, BackgroundTasks
from typing import Annotated
from sqlmodel import select
from datetime import timedelta
import re
from models import Token, TokenData, User, Users
from dependencies import (SessionDep, 
                          get_current_user, 
                          authenticate_user, 
                          create_access_token, 
                          password_hash,
                          OAuth2PasswordRequestForm,
                          write_notis,
                         )
from config import ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter()

users_tags_metadata = [
    {
        "name": "authentication",
        "descrtiption": "token operations"
    },
    {
        "name": "users",
        "description": "add a user"
    },
]

@router.post("/token", tags=["authentication"])
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: SessionDep,
) -> Token:
    user = authenticate_user(session=session, username=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


@router.post("/users/new", tags=["users"])
async def add_new_user(
    username: Annotated[str, Query(min_length=1, max_length=50)],
    password: Annotated[str, Query(min_length=8, max_length=100)],
    email: Annotated[str, Query()],
    session: SessionDep
):
    # Validate email format
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.fullmatch(email_pattern, email):
        raise HTTPException(status_code=400, detail="Invalid email format")
    
    # Check if username exists
    existing_user = session.exec(select(Users).where(Users.username==username)).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    
    # Check if email exists
    existing_email = session.exec(select(Users).where(Users.email==email)).first()
    if existing_email:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = password_hash.hash(password)
    user = Users(username=username, email=email, hashed_password=hashed_password)
    session.add(user)
    session.commit()
    session.refresh(user)

    return {
        "status": "New user has been added",
        "user_id": user.id,
        "username": user.username
    }
