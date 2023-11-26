import uvicorn
import os

from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends, HTTPException, status
from dotenv import load_dotenv, dotenv_values

ENV_FILE_PATH = os.getenv("ENV_FILE_PATH")
load_dotenv(ENV_FILE_PATH)

from db_info import crud, database, schemas, models
database.Base.metadata.create_all(bind = database.engine)

app = FastAPI(title = "Inventory API", description = "This API manages the inventory's items in UAchado System", version = "1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Allows all origins to make requests
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

invalid_id_message = "INVALID ID FORMAT"
item_not_found_message = "ITEM NOT FOUND"

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
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = invalid_id_message)
    
    item = crud.get_item_by_id(db = db, id = item_id)
    if not item:
        raise HTTPException(status_code = status.HTTP_204_NO_CONTENT, detail = item_not_found_message)
    return item

@app.get("/v1/items/tags", response_description = "Get the list of possible tags.", response_model = list[str], tags = ["Items"], status_code = status.HTTP_200_OK)               # UAC-44
def get_all_tags():
    return ["Todos","Portáteis","Telemóveis","Tablets","Auscultadores/Fones","Carregadores","Pen drives","Câmaras","Livros","Cadernos","Material de escritório","Carteiras","Chaves","Cartão","Óculos","Joalharia","Casacos","Chapéus/Bonés","Cachecóis","Luvas","Mochilas","Equipamento desportivo","Garrafas de água","Guarda-chuvas","Instrumentos musicais","Material de arte","Bagagem","Produtos de maquilhagem","Artigos de higiene","Medicamentos"]

@app.get("/v1/items/tag/{item_tag}", response_description = "Get items by tag.", response_model = list[schemas.Item], tags = ["Items"], status_code = status.HTTP_200_OK)
def get_item(item_tag: str, db: Session = Depends(get_db)):
    return crud.get_items_by_tag(db = db, tag = item_tag)

@app.get("/v1/items/retrieve/{item_id}", response_description = "Marking a specific item as 'retrived' by its ID.", response_model = schemas.Item, tags = ["Items"], status_code = status.HTTP_200_OK)
def retrieve_item(item_id: str, db: Session = Depends(get_db)):
    try:
        item_id = int(item_id)
    except ValueError:
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = invalid_id_message)
    
    item = crud.retrieve_item(db = db, id = item_id)
    if not item:
        raise HTTPException(status_code = status.HTTP_204_NO_CONTENT, detail = item_not_found_message)
    return item

@app.post("/v1/items/", response_description = "Create/Insert a new item.", response_model = schemas.Item, tags = ["Items"], status_code = status.HTTP_201_CREATED)                                        # UAC-48
def create_item(item: schemas.ItemCreate, db: Session = Depends(get_db)):
    return crud.create_item(db = db, new_item = item)

@app.delete("/v1/items/id/{item_id}", response_description = "Delete a specific item by its ID.", tags = ["Items"], status_code = status.HTTP_200_OK)
def delete_item(item_id: str, db: Session = Depends(get_db)):
    try:
        item_id = int(item_id)
    except:
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = invalid_id_message)
    
    if crud.delete_item(db, item_id) == None:
        raise HTTPException(status_code = status.HTTP_204_NO_CONTENT, detail = item_not_found_message)
    return {"message": "ITEM DELETED"}

if __name__  == '__main__':
    uvicorn.run(app, host = '0.0.0.0', port = 8000)