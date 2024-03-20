from sqlalchemy.orm import Session
from . import models, schemas


def get_pairs(db: Session):
    return db.query(models.Pair).all()


def get_pair_by_key(db: Session, key: str):
    return db.query(models.Pair).filter(models.Pair.keyword == key).first()


def get_pair_by_id(db: Session, id: int):
    return db.query(models.Pair).filter(models.Pair.id == id).first()


def create_pair(db: Session, pair: schemas.PairCreate):
    db_pair = models.Pair(**pair.model_dump())
    db.add(db_pair)
    db.commit()
    db.refresh(db_pair)
    return db_pair


def update_pair(db: Session, pair: schemas.PairUpdate):
    db_pair = db.query(models.Pair).filter(models.Pair.id == pair.id).first()
    db_pair.key = pair.keyword
    db_pair.value = pair.url
    db.commit()
    db.refresh(db_pair)
    return db_pair


def delete_pair_by_keyword(db: Session, keyword: str):
    db_pair = db.query(models.Pair).filter(
        models.Pair.keyword == keyword
    ).first()
    db.delete(db_pair)
    db.commit()
    return db_pair


def delete_pair(db: Session, id: int):
    db_pair = db.query(models.Pair).filter(models.Pair.id == id).first()
    db.delete(db_pair)
    db.commit()
    return db_pair
