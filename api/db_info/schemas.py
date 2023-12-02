from pydantic import BaseModel
from typing import Optional

class ItemBase(BaseModel):
    description: str
    tag: str
    image: str
    state: str
    dropoffPoint_id: Optional[int]
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
                "description": "Someone found a amazing pink console wih a sticker",
                "tag": "console",
                "image": "image",
                "state": "stored",
                "dropoffPoint_id": 1,
                "report_email": None,
                "retrieved_email": None,
                "retrieved_date": None,
            },
            "reported_example": {
                "id" : 1,
                "description": "I lost an amazing pink console wih a sticker",
                "tag": "console",
                "image": "image",
                "state": "reported",
                "dropoffPoint_id": None,
                "report_email": "my_mail",
                "retrieved_email": None,
                "retrieved_date": None
            },
            "retrieved_example": {
                "id" : 1,
                "description": "Someone found a amazing pink console wih a sticker",
                "tag": "console",
                "image": "image",
                "state": "retrieved",
                "dropoffPoint_id": 1,
                "report_email": None,
                "retrieved_email": "michelle.diaz@ua.pt",
                "retrieved_date": "today"
            },
            "archived_example": {
                "id" : 1,
                "description": "Someone found a amazing pink console wih a sticker",
                "tag": "console",
                "image": "image",
                "state": "archived",
                "dropoffPoint_id": 1,
                "report_email": None,
                "retrieved_email": "michelle.diaz@ua.pt",
                "retrieved_date": "very long time ago"
            }
        }

class ItemCreate(BaseModel):
    description: str
    tag: str
    image: str
    dropoffPoint_id: int

class ItemReport(BaseModel):
    description: str
    tag: str
    image: str
    report_email: str

class InputFilter(BaseModel):
    filter: dict

class Email(BaseModel):
    email: str