from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.sql import func

from . import database

class Item(database.Base):
    """

    :class:`Item`

    Represents an item in the database.

    Attributes:
        - `id` (int): The unique identifier of the item.
        - `description` (str): The description of the item.
        - `tag` (str): The tag associated with the item.
        - `image` (str): The string uuid to the image of the item identifying it in the AWS S3 Bucket (nullable).
        - `state` (str): The current state of the item.
        - `dropoff_point_id` (int): The ID of the drop-off point where the item was dropped off (nullable).
        - `insertion_date` (datetime): The insertion date of the item.
        - `report_email` (str): The email address of the person who reported the item (nullable).
        - `retrieved_email` (str): The email address of the person who retrieved the item (nullable).
        - `retrieved_date` (str): The date when the item was retrieved (nullable).

    """
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