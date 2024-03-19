from fastapi import FastAPI, Depends, Response, status
from fastapi.responses import RedirectResponse

from sqlalchemy.orm import Session

from app import crud, models, schemas

from .db import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def get_all():
    return {"message": "Hello World"}


@app.get("/services/")
def get_services(db: Session = Depends(get_db)):
    return crud.get_pairs(db)


@app.get("/services/{keyword}")
def get_service(keyword: str, db: Session = Depends(get_db)):
    return crud.get_pair_by_key(db, keyword)


@app.post("/services/")
def create_service(
    pair: schemas.PairCreate,
    db: Session = Depends(get_db)
):
    return crud.create_pair(db, pair)


@app.get("/redirect")
def redirect_service(service: str, db: Session = Depends(get_db)):
    pair = crud.get_pair_by_key(db, service)
    if pair:
        return RedirectResponse(
            url=pair.url,
            status_code=status.HTTP_302_FOUND
        )
    else:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
