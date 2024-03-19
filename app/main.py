from fastapi import FastAPI, Depends

from sqlalchemy.orm import Session

from app import crud, models, schemas

from .crud import get_pair_by_key
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


@app.get("/services/{keyword}")
def get_service(keyword: str, db: Session = Depends(get_db)):
    return get_pair_by_key(db, keyword)
