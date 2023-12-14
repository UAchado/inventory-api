from datetime import datetime
from fastapi import UploadFile
from pydantic import BaseModel
from typing import Optional

description_created = "Someone found a amazing pink console wih a sticker"
description_reported = "I lost an amazing pink console wih a sticker"
date_example = "2023-01-01T00:00:00"
class ItemBase(BaseModel):
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
    description: str
    tag: str
    image: Optional[UploadFile]
    dropoff_point_id: int

class ItemReport(BaseModel):
    description: str
    tag: str
    image: Optional[UploadFile]
    report_email: str

class InputFilter(BaseModel):
    filter: dict

class Email(BaseModel):
    email: str