from fastapi import APIRouter, Depends, Query, Body, HTTPException, responses, BackgroundTasks
from typing import Annotated
from sqlmodel import select
from sqlalchemy.exc import IntegrityError
from models import redirect_db, User, UrlRequest
from database import SessionDep
from dependencies import encode_link, write_notis
from config import ALPHABET, BASE_URL
from .users import get_current_user
import asyncio




links_tags_metadata = [
    {
        "name": "links",
        "description": "links operations"
    }
]

router = APIRouter(
    prefix="/links",
    tags=["links"],
    responses={
        404: {"description": "Link not found"},
        400: {"description": "Invalid URL"},
    }
)


@router.post("/shorten/", tags=["links"])
async def shorten_link(
    data: UrlRequest,
    session: SessionDep,
    # user: Annotated[User, Depends(get_current_user)],
    background_tasks: BackgroundTasks,
):
    original_url = data.original_url
    if not original_url.startswith(('http://', 'https://')):
        raise HTTPException(status_code=400, detail="Invalid URL")

    
    
    response = await session.execute(select(redirect_db).where(redirect_db.original_url==original_url))
    exists = response.scalars().first()

    if exists:
        return {
            "original_url": original_url,
            "short_url": f"{BASE_URL}/{exists.short_code}"
        }
    
    new_pair = redirect_db(short_code=None, original_url=original_url)
    session.add(new_pair)
    
    await session.flush()
    await session.refresh(new_pair)

    generated_code = encode_link(int(new_pair.id))
    new_pair.short_code = generated_code
    
    await session.commit()

    background_tasks.add_task(write_notis, f"{original_url} has been shortened into {BASE_URL+generated_code}\n\n")
    return {
        "original_url": original_url,
        "short_url": f"{BASE_URL}/links/{generated_code}"
    }

@router.get("/test")
async def test_api():
    return {"response" : "works well"}

@router.get("/{short_code}", tags=["links"])
async def redirect_to_original(
    short_code: str,
    session: SessionDep,
):
    response = await session.execute(select(redirect_db).where(redirect_db.short_code==short_code))

    resp = response.scalar().first()
    if not resp:
        raise HTTPException(status_code=404, detail="Link not found")

    return responses.RedirectResponse(url=resp.original_url, status_code=302)


