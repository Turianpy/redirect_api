from datetime import datetime

from sqlalchemy import String, DateTime, Column

from .db import Base

class Pair(Base):
    __tablename__ = "pairs"

    key = Column(String, primary_key=True, index=True)
    value = Column(String, index=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
