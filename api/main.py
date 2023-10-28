import uvicorn
from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends, HTTPException, status

import os
if os.environ.get("IN_DOCKER_CONTAINER"):
    from db_info import crud, database, schemas, models

    models.Base.metadata.create_all(bind=database.engine)
else:
    from .db_info import crud, database, schemas

app = FastAPI()

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def base():
    return {"response": "Hello World!"}

@app.get("/items/", response_model = list[schemas.Item], status_code = status.HTTP_200_OK)               # UAC-44
def get_all_items(db: Session = Depends(get_db)):
    items = crud.get_items(db)
    return items

@app.post("/items/", response_model = schemas.Item, status_code = status.HTTP_201_CREATED)                                        # UAC-48
def create_item(item: schemas.ItemCreate, db: Session = Depends(get_db)):
    return crud.create_item(db = db, new_item = item)

@app.delete("/items/id/{item_id}", status_code = status.HTTP_200_OK)
def delete_item(item_id: str, db: Session = Depends(get_db)):
    try:
        item_id = int(item_id)
        item = crud.get_item_by_id(db, id = item_id)
        if crud.delete_item(db, item) == "OK":
            return {"message": "Item deleted"}
        return {"message": "Item doesn't exist!"}
    except:
        return {"message": "Error"}

if __name__  == '__main__':
    uvicorn.run(app, host = 'localhost', port = 8000)