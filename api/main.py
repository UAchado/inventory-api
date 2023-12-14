import uvicorn
import os
import requests

from jose import jwt, JWTError
from typing import List, Optional
from fastapi_pagination import Page, Params
from fastapi_pagination.paginator import paginate as base_paginate
from fastapi_pagination.utils import disable_installed_extensions_check
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends, HTTPException, UploadFile, status, File, Form, Request
from dotenv import load_dotenv, dotenv_values

ENV_FILE_PATH = os.getenv("ENV_FILE_PATH")
load_dotenv(ENV_FILE_PATH)

from db_info import crud, database, schemas, auth, init_db
database.Base.metadata.create_all(bind = database.engine)

app = FastAPI(title = "Inventory API", description = "This API manages the inventory's items in UAchado System", version = "1.0.0")

invalid_id_message = "INVALID ID FORMAT"
item_not_found_message = "ITEM NOT FOUND"

disable_installed_extensions_check()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins to make requests
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)
    

def custom_paginate(items, params: Optional[Params] = None):
    """
    Custom Paginate

    Custom Paginate is a method used to paginate a list of items based on specific parameters.

    :param items: A list of items to paginate.
    :param params: Optional. An instance of the Params class containing pagination parameters. If not provided, default parameters will be used.
    :return: A paginated list of items.

    """
    if params is None:
        params = Params(page=1,size=len(items))
    return base_paginate(items, params)

def get_db():
    """
    Get a database session from the SessionLocal object.

    :return: A database session.
    """
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

## INIT DB

@app.on_event("startup")
async def startup_event():
    """
    Startup Event

    This method is an event handler for the "startup" event. It initializes the database if there are no items in it.

    :return: None
    """
    db = database.SessionLocal()
    try:
        if crud.get_items(db) == []:
            init_db.init(db)
    finally:
        db.close()    
        
## ENDPOINTS

@app.get("/inventory/v1")
def base():
    """
    Root endpoint of the inventory API.

    :return: A dictionary containing the response message.
    """
    return {"response": "Hello World!"}

# GET ALL ITEMS

@app.get("/inventory/v1/items", response_description = "Get the list of existing items.",
         response_model = Page[schemas.Item], tags = ["Items"], status_code = status.HTTP_200_OK)
def get_all_items(request: Request,
                  params: Params = Depends(),
                  db: Session = Depends(get_db)) -> Page[schemas.Item]:
    """
    Get the list of existing items.

    :param request: The request object.
    :param params: The parameters object.
    :param db: The database session object.
    :return: The page containing the list of items.
    """
    auth.verify_access(request)
    return custom_paginate(crud.get_items(db), params)

# GET ITEM BY ID

@app.get("/inventory/v1/items/id/{item_id}", response_description = "Get a specific item by its ID.",
         response_model = schemas.Item, tags = ["Items"], status_code = status.HTTP_200_OK)
def get_item_by_id(item_id: str,
                   db: Session = Depends(get_db)) -> schemas.Item:
    """
    :param item_id: The ID of the item to retrieve.
    :param db: The database session to use.
    :return: The retrieved item.
    """
    try:
        item_id = int(item_id)
    except ValueError:
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = invalid_id_message)
    
    item = crud.get_item_by_id(db = db, id = item_id)
    if not item:
        raise HTTPException(status_code = status.HTTP_204_NO_CONTENT, detail = item_not_found_message)
    return item

# GET ITEM TAGS LIST

@app.get("/inventory/v1/items/tags", response_description = "Get the list of all tags.",
         response_model = List[str], tags = ["Items"], status_code = status.HTTP_200_OK)
def get_all_tags() -> List[str]:
    """
    Get the list of all tags.

    :return: A list of strings representing all the available tags.
    :rtype: List[str]
    """
    return ["Todos","Portáteis","Telemóveis","Tablets","Auscultadores/Fones","Carregadores",
            "Pen drives","Câmaras","Livros","Cadernos","Material de escritório","Carteiras",
            "Chaves","Cartão","Óculos","Joalharia","Casacos","Chapéus/Bonés","Cachecóis","Luvas",
            "Mochilas","Equipamento desportivo","Garrafas de água","Guarda-chuvas","Instrumentos musicais",
            "Material de arte","Bagagem","Produtos de maquilhagem","Artigos de higiene","Medicamentos"]

# GET ITEMS BY NOT AUTHENTICATED USER

@app.post("/inventory/v1/items/stored", response_description = "Get currently active items by filter.",
          response_model = Page[schemas.Item], tags = ["Items"], status_code = status.HTTP_200_OK)                                        # UAC-48
def get_stored_items(filter: schemas.InputFilter,
                     params: Params = Depends(), db: Session = Depends(get_db)) -> Page[schemas.Item]:
    """
    Get currently active items by filter.

    :param filter: The filter criteria used to search for items.
    :type filter: schemas.InputFilter
    :param params: Optional additional parameters for pagination.
    :type params: Params
    :param db: The database session object.
    :type db: Session
    :return: A paginated list of currently active items.
    :rtype: Page[schemas.Item]
    """
    return custom_paginate(crud.get_stored_items(db = db, filter = filter.filter), params)

@app.put("/inventory/v1/items/point/{dropoff_point_id}", response_description = "Get items on a drop-off point by filter.",
         response_model = Page[schemas.Item], tags = ["Items"], status_code = status.HTTP_200_OK)                                        # UAC-48
def get_dropoff_point_items(request: Request,
                            dropoff_point_id: str,
                            filter: schemas.InputFilter,
                            params: Params = Depends(),
                            db: Session = Depends(get_db)) -> Page[schemas.Item]:
    """
    :param request: The request object containing information about the current request
    :type request: Request
    :param dropoff_point_id: The ID of the drop-off point to get items from
    :type dropoff_point_id: str
    :param filter: The filtering criteria to apply when retrieving items
    :type filter: schemas.InputFilter
    :param params: Additional parameters for pagination
    :type params: Params
    :param db: The database session object
    :type db: Session
    :return: A paginated list of items from the drop-off point
    :rtype: Page[schemas.Item]
    """
    auth.verify_access(request)
    try:
        dropoff_point_id = int(dropoff_point_id)
    except ValueError:
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = invalid_id_message)
    
    return custom_paginate(crud.get_dropoff_point_items(db = db, dropoff_point_id = dropoff_point_id, filter = filter.filter), params)

# MARK ITEM AS RETRIEVED

@app.put("/inventory/v1/items/retrieve/{item_id}", response_description = "Marking a specific item as 'retrieved' by its ID.",
         response_model = schemas.Item, tags = ["Items"], status_code = status.HTTP_200_OK)
def retrieve_item(request: Request,
                  item_id: str,
                  email: schemas.Email,
                  db: Session = Depends(get_db)) -> schemas.Item:
    """
    Marking a specific item as 'retrieved' by its ID.

    :param request: The request object.
    :param item_id: The ID of the item to be marked as 'retrieved'.
    :param email: The email of the user who retrieved the item.
    :param db: The database session.
    :return: The retrieved item.
    """
    auth.verify_access(request)
    try:
        item_id = int(item_id)
    except ValueError:
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = invalid_id_message)
    
    item = crud.retrieve_item(db = db, id = item_id, retrieved_email = email.email)
    if not item:
        raise HTTPException(status_code = status.HTTP_204_NO_CONTENT, detail = item_not_found_message)
    return item

# CREATE A NEW ITEM

@app.post("/inventory/v1/items/create", response_description = "Create/Insert a new item.",
          response_model = schemas.Item, tags = ["Items"], status_code = status.HTTP_201_CREATED)

def create_item(request: Request,
                description: str = Form(...),
                tag: str = Form(...),
                image: Optional[UploadFile] = File(...),
                dropoff_point_id: int = Form(...),
                db: Session = Depends(get_db)) -> schemas.Item:
    """
    Create/Insert a new item.

    :param request: The request object.
    :param description: The description of the item.
    :param tag: The tag associated with the item.
    :param image: The image file associated with the item (optional).
    :param dropoff_point_id: The ID of the dropoff point associated with the item.
    :param db: The database session.
    :return: The created item.
    """
    auth.verify_access(request)

    if image == None or image.content_type not in ["image/jpeg", "image/png", "image/jpg"]:
        image = None

    item = schemas.ItemCreate(description=description,
                              tag=tag,
                              image=image,
                              dropoff_point_id=dropoff_point_id
                              )
    return crud.create_item(db = db, new_item = item) 

# REPORT A NEW ITEM

@app.post("/inventory/v1/items/report", response_description = "Report a new item.",
          response_model = schemas.Item, tags = ["Items"], status_code = status.HTTP_201_CREATED)

def report_item(description: str = Form(...),
                tag: str = Form(...),
                image: Optional[UploadFile] = File(...),
                report_email: str = Form(...),
                db: Session = Depends(get_db)) -> schemas.Item:
    """
    :param description: A string representing the description of the item being reported.
    :param tag: A string representing the tag associated with the item.
    :param image: An optional UploadFile object representing the image of the item.
    :param report_email: A string representing the email of the person reporting the item.
    :param db: An instance of the Session class representing the database session.
    :return: An instance of the schemas.Item class representing the newly reported item.

    """
    if image == None or image.content_type not in ["image/jpeg", "image/png", "image/jpg"]:
        image = None

    item = schemas.ItemReport(description=description,
                              tag=tag,
                              image=image,
                              report_email=report_email
                              )
    return crud.report_item(db = db, new_item = item)

# DELETE EXISTING ITEM

@app.delete("/inventory/v1/items/id/{item_id}", response_description = "Delete a specific item by its ID.",
            tags = ["Items"], status_code = status.HTTP_200_OK)
def delete_item(request: Request,
                item_id: str,
                db: Session = Depends(get_db)):
    """
    Delete a specific item by its ID.

    :param request: The HTTP request.
    :param item_id: The ID of the item to delete.
    :param db: The database session.
    :return: A dictionary containing a success message.
    """
    auth.verify_access(request)
    try:
        item_id = int(item_id)
    except ValueError:
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = invalid_id_message)
    
    if crud.delete_item(db, item_id) == None:
        raise HTTPException(status_code = status.HTTP_204_NO_CONTENT, detail = item_not_found_message)
    return {"message": "ITEM DELETED"}

# GET IMAGE FROM S3 BUCKET

@app.get("/inventory/v1/image/{image_uuid}", response_description = "Return the image presigned url from S3 Bucket B.",
            response_model = dict, tags = ["Items"], status_code = status.HTTP_200_OK)
def get_image_from_s3(image_uuid: str):
    """
    Retrieve the image presigned URL from S3 Bucket B.

    :param image_uuid: A string representing the unique identifier for the image.
    :return: A dictionary containing the image's presigned URL and related information.
    """
    return crud.get_image_from_s3(image_uuid)

if __name__  == '__main__':
    uvicorn.run(app, host = '0.0.0.0', port = 8000)