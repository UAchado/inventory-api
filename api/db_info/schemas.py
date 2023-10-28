from pydantic import BaseModel

class ItemBase(BaseModel):
    description: str
    tag: str
    image: str
    mail: str = None
    dropoffPoint_id: int = None
    state: str

class ItemCreate(ItemBase):
    pass

class Item(ItemBase):
    id: int

    class ConfigDict:
        from_attributes = True