from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from .database import Base


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String(500), unique=True)
    tag = Column(String(50))
    mail = Column(String(100), nullable=True)
    image = Column(String(500), unique=True)
    dropoffPoint_id = Column(String(50), nullable=True)
    state = Column(String(50))