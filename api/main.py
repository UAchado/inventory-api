import uvicorn
from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.responses import JSONResponse

import os
if os.environ.get("IN_DOCKER_CONTAINER"):
    from db_info import crud, database, schemas, models

    models.Base.metadata.create_all(bind=database.engine)
else:
    from .db_info import crud, database, schemas

app = FastAPI(title = "Inventory API", description = "This API manages the inventory's items in UAchado System", version = "1.0.0")

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/v1/")
def base():
    return {"response": "Hello World!"}

@app.get("/v1/items/", response_description = "Get the list of existing items.", response_model = list[schemas.Item], tags = ["Items"], status_code = status.HTTP_200_OK)               # UAC-44
def get_all_items(db: Session = Depends(get_db)):
    return crud.get_items(db)

@app.get("/v1/items/id/{item_id}", response_description = "Get a specific item by its ID.", response_model = schemas.Item, tags = ["Items"], status_code = status.HTTP_200_OK)
def get_item(item_id: str, db: Session = Depends(get_db)):
    try:
        item_id = int(item_id)
    except ValueError:
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = "INVALID ID FORMAT")
    
    item = crud.get_item_by_id(db = db, id = item_id)
    if not item:
        raise HTTPException(status_code = status.HTTP_204_NO_CONTENT, detail = "ITEM NOT FOUND")
    return item

@app.get("/v1/items/retrieve/{item_id}", response_description = "Marking a specific item as 'retrived' by its ID.", response_model = schemas.Item, tags = ["Items"], status_code = status.HTTP_200_OK)
def retrieve_item(item_id: str, db: Session = Depends(get_db)):
    try:
        item_id = int(item_id)
    except ValueError:
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = "INVALID ID FORMAT")
    
    item = crud.retrieve_item(db = db, id = item_id)
    if not item:
        raise HTTPException(status_code = status.HTTP_204_NO_CONTENT, detail = "ITEM NOT FOUND")
    return item

@app.post("/v1/items/", response_description = "Create/Insert a new item.", response_model = schemas.Item, tags = ["Items"], status_code = status.HTTP_201_CREATED)                                        # UAC-48
def create_item(item: schemas.ItemCreate, db: Session = Depends(get_db)):
    return crud.create_item(db = db, new_item = item)

@app.delete("/v1/items/id/{item_id}", response_description = "Delete a specific item by its ID.", tags = ["Items"], status_code = status.HTTP_200_OK)
def delete_item(item_id: str, db: Session = Depends(get_db)):
    try:
        item_id = int(item_id)
    except:
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = "INVALID ID FORMAT")
    
    if crud.delete_item(db, item_id) == None:
        raise HTTPException(status_code = status.HTTP_204_NO_CONTENT, detail = "ITEM NOT FOUND")
    return {"message": "ITEM DELETED"}

if __name__  == '__main__':
    uvicorn.run(app, host = 'localhost', port = 8000)