from datetime import datetime

from pydantic import BaseModel


class PairBase(BaseModel):
    keyword: str
    url: str


class PairCreate(PairBase):
    pass


class PairUpdate(PairBase):
    id: int


class Pair(PairBase):
    id: int
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()

    class Config:
        from_attributes = True
