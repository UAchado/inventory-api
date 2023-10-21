from pydantic import BaseModel

class Item(BaseModel):
    id: int
    description: str
    image: str
    video: str
    tag: str = None
    dropoffPoint_id: int = None
    mail: str = None