from pydantic import BaseModel

class ItemBase(BaseModel):
    description: str
    tag: str
    image: str
    mail: str = None
    dropoffPoint_id: str = None
    state: str

class ItemCreate(ItemBase):
    pass

class Item(ItemBase):
    id: int

    class Config:
        orm_mode = True