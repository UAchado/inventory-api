import uvicorn
from fastapi import FastAPI
from api.models.item import Item
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


app = FastAPI()

engine = create_engine("mysql+mysqlconnector://user:password@localhost/database") #TODO
SessionLocal = sessionmaker(autocommit = False, autoflush = False, bind = engine)

@app.get("/items/", response_model = list[Item])
def get_all_items():
    db = SessionLocal()
    items = db.query(Item).all()
    return items

@app.post("/items/add/")
def create_item(item: Item):
    db = SessionLocal()
    db.add(item)
    db.commit()
    db.refresh(item)
    return item

if __name__  == '__main__':
    uvicorn.run(app, host = 'localhost', port = 8000)