from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.sql import func

from . import database

class Item(database.Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key = True, index = True)
    description = Column(String(500))
    tag = Column(String(50))
    image = Column(String(500), nullable = True)
    state = Column(String(50))
    dropoff_point_id = Column(Integer, nullable = True)
    insertion_date = Column(DateTime(timezone=True), default=func.now())
    report_email = Column(String(100), nullable = True)
    retrieved_email = Column(String(100), nullable = True)
    retrieved_date = Column(String(100), nullable = True)