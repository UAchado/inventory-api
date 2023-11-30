from pydantic import BaseModel
from typing import Optional

class ItemBase(BaseModel):
    description: str
    tag: str
    image: str
    state: str
    dropoffPoint_id: Optional[int]
    mail: Optional[str]
    retrieved_email: Optional[str]
    retrieved_date: Optional[str]

class ItemCreate(BaseModel):
    description: str
    tag: str
    image: str
    dropoffPoint_id: Optional[int]
    mail: Optional[str]

class Email(BaseModel):
    email: str

class Item(ItemBase):
    id: int

    class ConfigDict:
        from_attributes = True
        schema_extra = {
            "example_1": {
                "id" : 1,
                "description": "Someone found a amazing pink console wih a sticker",
                "tag": "console",
                "image": "link_to_image",
                "state": "retrieved",
                "dropoffPoint_id": 1,
                "mail": None,
                "retrieved_email": "michelle.diaz@ua.pt",
                "retrieved_date": None,
            },
            "example_2": {
                "id" : 1,
                "description": "I lost an amazing pink console wih a sticker",
                "tag": "console",
                "image": "link_to_image",
                "state": "reported",
                "dropoffPoint_id": None,
                "mail": "my_mail",
                "retrieved_email": None,
                "retrieved_date": None
            }
        }