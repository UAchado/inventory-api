from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from .database import Base


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key = True, index = True)
    description = Column(String(500))
    tag = Column(String(50))
    image = Column(String(500))
    state = Column(String(50))
    dropoffPoint_id = Column(Integer, nullable = True)
    mail = Column(String(100), nullable = True)