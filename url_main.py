from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from url_database import Base, engine, get_db
from url_models import URLModel
from url_schemas import URLCreate, URLResponse

from url_service import (
    create_short_url,
    get_url_by_code,
    get_all_urls
)


@asynccontextmanager
async def lifespan(app: FastAPI):

    Base.metadata.create_all(bind=engine)

    yield


app = FastAPI(
    title="QuickURL API",
    lifespan=lifespan
)


@app.get("/")
def home():

    return {
        "message": "Welcome to QuickURL API"
    }


@app.post("/shorten", response_model=URLResponse)
def shorten_url(
    data: URLCreate,
    db: Session = Depends(get_db)
):

    original_url = str(data.original_url)

    try:
        new_url = create_short_url(original_url, db)
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=503,
            detail="Unable to generate short URL"
        )

    return {
        "original_url": new_url.original_url,
        "short_code": new_url.short_code,
        "short_url": f"http://127.0.0.1:8000/{new_url.short_code}"
    }


@app.get("/{short_code}")
def redirect_url(
    short_code: str,
    db: Session = Depends(get_db)
):

    url = get_url_by_code(short_code, db)

    if url is None:
        raise HTTPException(
            status_code=404,
            detail="Short URL not found"
        )

    return RedirectResponse(
        url=url.original_url,
        status_code=307
    )


@app.get("/api/urls")
def list_urls(db: Session = Depends(get_db)):

    return get_all_urls(db)