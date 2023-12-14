from datetime import datetime
from fastapi import UploadFile
from pydantic import BaseModel
from typing import Optional

description_created = "Someone found a amazing pink console wih a sticker"
description_reported = "I lost an amazing pink console wih a sticker"
date_example = "2023-01-01T00:00:00"
class ItemBase(BaseModel):
    """

    A base class for representing an item.

    Attributes:
        description (str): The description of the item.
        tag (str): The tag associated with the item.
        image (Optional[str]): The string uuid to the image of the item identifying it in the AWS S3 Bucket. Defaults to None.
        state (str): The state of the item.
        dropoff_point_id (Optional[int]): The ID of the drop-off point. Defaults to None.
        insertion_date (Optional[datetime]): The insertion date of the item. Defaults to None.
        report_email (Optional[str]): The email to report the item. Defaults to None.
        retrieved_email (Optional[str]): The email to retrieve the item. Defaults to None.
        retrieved_date (Optional[str]): The date the item was retrieved. Defaults to None.

    """
    description: str
    tag: str
    image: Optional[str]
    state: str
    dropoff_point_id: Optional[int]
    insertion_date: Optional[datetime]
    report_email: Optional[str]
    retrieved_email: Optional[str]
    retrieved_date: Optional[str]

class Item(ItemBase):
    """
    Class representing an item.

    Attributes:
        id (int): The id of the item.

    """
    id: int

    class ConfigDict:
        from_attributes = True
        schema_extra = {
            "stored_example": {
                "id" : 1,
                "description": description_created,
                "tag": "console",
                "image": "image",
                "state": "stored",
                "dropoff_point_id": 1,
                "insertion_date": date_example,
                "report_email": None,
                "retrieved_email": None,
                "retrieved_date": None,
            },
            "reported_example": {
                "id" : 1,
                "description": description_reported,
                "tag": "console",
                "image": "image",
                "state": "reported",
                "dropoff_point_id": None,
                "insertion_date": date_example,
                "report_email": "my_mail",
                "retrieved_email": None,
                "retrieved_date": None
            },
            "retrieved_example": {
                "id" : 1,
                "description": description_created,
                "tag": "console",
                "image": "image",
                "state": "retrieved",
                "dropoff_point_id": 1,
                "insertion_date": date_example,
                "report_email": None,
                "retrieved_email": "michelle.diaz@ua.pt",
                "retrieved_date": "today"
            },
            "archived_example": {
                "id" : 1,
                "description": description_created,
                "tag": "console",
                "image": "image",
                "state": "archived",
                "dropoff_point_id": 1,
                "insertion_date": date_example,
                "report_email": None,
                "retrieved_email": "michelle.diaz@ua.pt",
                "retrieved_date": "very long time ago"
            }
        }

class ItemCreate(BaseModel):
    """
    Represents an item to be created.

    :param description: The description of the item.
    :type description: str
    :param tag: The tag associated with the item.
    :type tag: str
    :param image: Optional image file associated with the item.
    :type image: Optional[UploadFile]
    :param dropoff_point_id: The ID of the drop-off point for the item.
    :type dropoff_point_id: int
    """
    description: str
    tag: str
    image: Optional[UploadFile]
    dropoff_point_id: int

class ItemReport(BaseModel):
    """
    Represents an item report.

    :param description: The description of the item report.
    :type description: str
    :param tag: The tag associated with the item report.
    :type tag: str
    :param image: Optional image file associated with the item report.
    :type image: Optional[UploadFile]
    :param report_email: The email address of the person making the item report.
    :type report_email: str
    """
    description: str
    tag: str
    image: Optional[UploadFile]
    report_email: str

class InputFilter(BaseModel):
    """
    Class to represent an input filter.

    :param filter: A dictionary representing the filter to be applied.
    """
    filter: dict

class Email(BaseModel):
    """Represents an email address."""
    email: str