from fastapi import APIRouter, Depends, Query, HTTPException, responses, BackgroundTasks
from typing import Annotated
from sqlmodel import select
from sqlalchemy.exc import IntegrityError
from models import redirect_db, User
from dependencies import encode_link, SessionDep, write_notis
from config import ALPHABET, BASE_URL
from .users import get_current_user
import redis

r = redis.Redis(host='localhost', port=6379, decode_responses=True)
#r.bf().reserve("original_urls", 0.01, 100000000)


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
    original_url: str,
    session: SessionDep,
    # user: Annotated[User, Depends(get_current_user)],
    background_tasks: BackgroundTasks,
):
    
    if not original_url.startswith(('http://', 'https://')):
        raise HTTPException(status_code=400, detail="Invalid URL")

    
    if r.bf().exists("original_urls", original_url):
        exists = session.exec(select(redirect_db).where(redirect_db.original_url==original_url)).first()
        if exists:
            return {
                "original_url": original_url,
                "short_url": f"http://127.0.0.1:8080/{exists.short_code}"
            }
    
    new_pair = redirect_db(short_code="", original_url=original_url)
    session.add(new_pair)
    session.commit()
    session.refresh(new_pair)
    r.bf().add("original_urls", original_url)

    generated_code = encode_link(new_pair.id)
    new_pair.short_code = generated_code
    session.commit()

    background_tasks.add_task(write_notis, "no email", f"{original_url} has been shortened into {BASE_URL+generated_code}\n\n")
    return {
        "original_url": original_url,
        "short_url": f"http://127.0.0.1:8080/{generated_code}"
    }

@router.get("/test")
async def test_api():
    return {"response" : "works well"}

@router.get("/{short_code}", tags=["links"])
async def redirect_to_original(
    short_code: str,
    session: SessionDep,
):
    resp = session.exec(select(redirect_db).where(redirect_db.short_code==short_code)).first()

    if not resp:
        raise HTTPException(status_code=404, detail="Link not found")

    return responses.RedirectResponse(url=resp.original_url, status_code=302)


