from fastapi import FastAPI, Depends, Response, status, HTTPException
from fastapi.responses import RedirectResponse

from sqlalchemy.orm import Session

from services import crud, models, schemas
from services.db import SessionLocal, engine

import requests

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def exists(
    pair: schemas.PairCreate = None,
    db: Session = Depends(get_db),
):
    if pair:
        if crud.get_pair_by_key(db, pair.keyword):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="This keyword already exists"
            )


@app.get("/")
def get_all():
    return {"message": "xd"}


@app.get("/services/")
def get_services(db: Session = Depends(get_db)):
    """Get all keyword - url pairs"""
    return crud.get_pairs(db)


@app.get("/services/{keyword}")
def get_service(keyword: str, db: Session = Depends(get_db)):
    """Get a keyword - url pair by keyword"""
    return crud.get_pair_by_key(db, keyword)


@app.post("/services/")
def create_service(
    pair: schemas.PairCreate,
    db: Session = Depends(get_db)
):
    """
    Creates a keyword - url pair
    Checks if the url is valid and accessible before saving
    """
    exists(pair, db)
    try:
        response = requests.head(pair.url, timeout=5)
        if response.status_code >= 400 and not response.status_code == 418:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid URL"
            )
    except requests.exceptions.RequestException:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid URL"
        )

    return crud.create_pair(db, pair)


@app.delete("/services/{keyword}")
def delete_service(keyword: str, db: Session = Depends(get_db)):
    return crud.delete_pair_by_keyword(db, keyword)


@app.get("/redirect")
def redirect_service(service: str, db: Session = Depends(get_db)):
    """
    Tries to find a keyword - url pair and redirects to the url if found
    Otherwise returns 404.
    """
    pair = crud.get_pair_by_key(db, service)
    if pair:
        return RedirectResponse(
            url=pair.url,
            status_code=status.HTTP_302_FOUND
        )
    else:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
