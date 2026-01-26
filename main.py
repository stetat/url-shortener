from fastapi import FastAPI, Request, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
from datetime import time
import time
from database import create_db_and_tables
from routers import links, users
from dependencies import get_current_user

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("App has started")
    create_db_and_tables()
    yield
    print("App has finished")


description = """
LinkShortener API lets you convert ambigious links into short links.

## Links

You can **shorten links**
        ** and redirect to links based on a short code**

    
## Users

You can **add a user**
"""

tags_metadata = links.links_tags_metadata + users.users_tags_metadata


def create_app() -> FastAPI:
    app = FastAPI(
        lifespan=lifespan,
        redoc_url=None,
        title="LinkShortener",
        description=description,
        summary=" A very primitive link shortener",
        version="0.0.1",
        terms_of_service="http://example.com/terms/",
        contact={
            "name": "Darkhan",
            "url": "https://t.me/bigward1",
            "email": "cryptodarkhan@gmail.com",
        },
        openapi_tags=tags_metadata,
        )

    app.mount("/web", StaticFiles(directory="webpage", html=True), name="webpage")
    app.include_router(users.router)
    app.include_router(links.router)

    return app


app = create_app()


origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def app_process_time_header(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response