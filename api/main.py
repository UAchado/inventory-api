from os import getenv
from typing import List, Optional

from dotenv import load_dotenv
from fastapi import (Depends, FastAPI, File, Form, HTTPException, Request,
                     UploadFile, status)
from fastapi.middleware.cors import CORSMiddleware
from fastapi_pagination import Page, Params
from fastapi_pagination.paginator import paginate as base_paginate
from fastapi_pagination.utils import disable_installed_extensions_check
from sqlalchemy.orm import Session
from uvicorn import run

ENV_FILE_PATH = getenv("ENV_FILE_PATH")
load_dotenv(ENV_FILE_PATH)

from db_info import auth, crud, database, init_db, schemas

database.Base.metadata.create_all(bind = database.engine)

app = FastAPI(title = "Inventory API",
              summary = "Inventory API for UAchado App",
              description = "This API manages the inventory's items in UAchado system. It helps with the logic inside the system.",
              version = "1.0.0",
              openapi_url = "/inventory/v1/openapi.json",
              docs_url="/inventory/v1/docs",
              redoc_url="/inventory/v1/redocs")

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

## HELPER FUNCTIONS

def custom_paginate(items: List[schemas.Item],
                    params: Optional[Params] = None) -> Page[schemas.Item]:
    """
    Custom Paginate. Method used to paginate a list of items based on specific parameters.

    Args:
        items (List[schemas.Item]): A list of items to paginate.
        params (Optional[Params]): Optional. An instance of the Params class containing pagination parameters. If not provided, default parameters will be used.
    
    Return:
        Page[schemas.Item]: A paginated list of items.
    """
    if params is None:
        params = Params(page=1,size=len(items))
    return base_paginate(items, params)

def get_db():
    """
    Get the database session from the SessionLocal object which the API can connect to.

    Return:
        A database session.
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

    Return:
        None
    """
    db = database.SessionLocal()
    try:
        if crud.get_items(db) == []:
            init_db.init(db)
    finally:
        db.close()    
        
## ENDPOINTS

# BASE (UNAUTHENTICATED USER)

@app.get("/inventory/v1",
         response_description = "Root endpoint of the inventory API.",
         response_model = dict,
         tags = ["Items"],
         status_code = status.HTTP_200_OK)
def base() -> dict:
    """
    Root endpoint of the inventory API. Mostly used for testing API connectivity.

    Returns:
        _type_: A dictionary containing the response message.
    """    
    return {"response": "Hello World!"}

# GET ALL ITEMS (UNAUTHENTICATED USER)

@app.get("/inventory/v1/items", 
         response_description = "Get the list of existing items.",
         response_model = Page[schemas.Item],
         tags = ["Items"],
         status_code = status.HTTP_200_OK)
def get_all_items(request: Request,
                  params: Params = Depends(),
                  db: Session = Depends(get_db)) -> Page[schemas.Item]:
    """
    Get the list of existing items.

    Args:
        request (Request): The request object containing information about the request.
        params (Params, optional): Optional additional parameters for pagination. Defaults to Depends().
        db (Session, optional): Optional database session object. If not included the system will connect to the default one. Defaults to Depends(get_db).

    Returns:
        Page[schemas.Item]: The page containing the list of items.
    """    
    auth.verify_access(request)
    return custom_paginate(crud.get_items(db), params)

# GET ITEM BY ID (UNAUTHENTICATED USER)

@app.get("/inventory/v1/items/id/{item_id}",
         response_description = "Get a specific item by its ID.",
         response_model = schemas.Item,
         tags = ["Items"],
         status_code = status.HTTP_200_OK)
def get_item_by_id(item_id: str,
                   db: Session = Depends(get_db)) -> schemas.Item:
    """
    Get a specific item by its ID.

    Args:
        item_id (str): The ID attribute of a specify unique item.
        db (Session, optional): Optional database session object. If not included the system will connect to the default one. Defaults to Depends(get_db).

    Raises:
        HTTPException (HTTP_400_BAD_REQUEST): Error raised if item_id is not numeric.
        HTTPException (HTTP_204_NO_CONTENT): Error raised if there's no stored item with the item_id.

    Returns:
        schemas.Item: The stored item.
    """
    try:
        item_id = int(item_id)
    except ValueError:
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = invalid_id_message)
    
    item = crud.get_item_by_id(db = db, id = item_id)
    if not item:
        raise HTTPException(status_code = status.HTTP_204_NO_CONTENT, detail = item_not_found_message)
    return item

# GET ITEM TAGS LIST (UNAUTHENTICATED USER)

@app.get("/inventory/v1/items/tags",
         response_description = "Get the list of all tags.",
         response_model = List[str],
         tags = ["Items"],
         status_code = status.HTTP_200_OK)
def get_all_tags() -> List[str]:
    """
    Get the list of all tags the system currently supports.

    Returns:
        List[str]: the list of strings representing all the available tags.
    """    
    return ["Todos","Portáteis","Telemóveis","Tablets","Auscultadores/Fones","Carregadores",
            "Pen drives","Câmaras","Livros","Cadernos","Material de escritório","Carteiras",
            "Chaves","Cartão","Óculos","Joalharia","Casacos","Chapéus/Bonés","Cachecóis","Luvas",
            "Mochilas","Equipamento desportivo","Garrafas de água","Guarda-chuvas","Instrumentos musicais",
            "Material de arte","Bagagem","Produtos de maquilhagem","Artigos de higiene","Medicamentos"]

# GET ITEMS BY NOT AUTHENTICATED USER

@app.post("/inventory/v1/items/stored",
          response_description = "Get currently 'stored' items using optional filter",
          response_model = Page[schemas.Item],
          tags = ["Items"],
          status_code = status.HTTP_200_OK)
def get_stored_items(filter: schemas.InputFilter,
                     params: Params = Depends(),
                     db: Session = Depends(get_db)) -> Page[schemas.Item]:
    """
    Get currently 'stored' items using optional filter.

    Args:
        filter (schemas.InputFilter): The filter criteria used to search for items.
        params (Params, optional): Optional additional parameters for pagination. Defaults to Depends().
        db (Session, optional): Optional database session object. If not included the system will connect to the default one. Defaults to Depends(get_db).

    Returns:
        Page[schemas.Item]: A paginated list of current items containing the 'stored' state.
    """    
    return custom_paginate(crud.get_stored_items(db = db, filter = filter.filter), params)

# GET ITEMS BY AUTHENTICATED USER

@app.put("/inventory/v1/items/point/{dropoff_point_id}",
         response_description = "Get items on a drop-off point by filter.",
         response_model = Page[schemas.Item],
         tags = ["Items"],
         status_code = status.HTTP_200_OK)
def get_dropoff_point_items(request: Request,
                            dropoff_point_id: str,
                            filter: schemas.InputFilter,
                            params: Params = Depends(),
                            db: Session = Depends(get_db)) -> Page[schemas.Item]:
    """
    Get items on a drop-off point by filter.

    Args:
        request (Request): The request object containing information about the request.
        dropoff_point_id (str): The ID of the drop-off point to get items from.
        filter (schemas.InputFilter): The filter criteria used to search for items.
        params (Params, optional): Additional parameters for pagination Defaults to Depends().
        db (Session, optional): Optional database session object. If not included the system will connect to the default one. Defaults to Depends(get_db).

    Raises:
        HTTPException (HTTP_400_BAD_REQUEST): Error raised if dropoff_point_id is not numeric.

    Returns:
        Page[schemas.Item]: A paginated list of items from the drop-off point.
    """    
    auth.verify_access(request)
    try:
        dropoff_point_id = int(dropoff_point_id)
    except ValueError:
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = invalid_id_message)
    
    return custom_paginate(crud.get_dropoff_point_items(db = db, dropoff_point_id = dropoff_point_id, filter = filter.filter), params)

# MARK ITEM AS RETRIEVED (AUTHENTICATED USER)

@app.put("/inventory/v1/items/retrieve/{item_id}",
         response_description = "Marking a specific item as 'retrieved' by its ID.",
         response_model = schemas.Item,
         tags = ["Items"],
         status_code = status.HTTP_200_OK)
def retrieve_item(request: Request,
                  item_id: str,
                  email: schemas.Email,
                  db: Session = Depends(get_db)) -> schemas.Item:
    """
    Marking a specific item as 'retrieved' by its ID.

    Args:
        request (Request): The request object containing information about the request.
        item_id (str): The ID of the item to be marked as 'retrieved'.
        email (schemas.Email): The email of the user who retrieved the item.
        db (Session, optional): Optional database session object. If not included the system will connect to the default one. Defaults to Depends(get_db).

    Raises:
        HTTPException (HTTP_400_BAD_REQUEST): Error raised if item_id is not numeric.
        HTTPException (HTTP_204_NO_CONTENT): Error raised if there's no stored item with the item_id.

    Returns:
        schemas.Item: The item with the updated state 'retrieved'.
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

# CREATE A NEW ITEM (AUTHENTICATED USER)

@app.post("/inventory/v1/items/create",
          response_description = "Create a new found item.",
          response_model = schemas.Item,
          tags = ["Items"], 
          status_code = status.HTTP_201_CREATED)
def create_item(request: Request,
                description: str = Form(...),
                tag: str = Form(...),
                image: Optional[UploadFile] = File(...),
                dropoff_point_id: int = Form(...),
                db: Session = Depends(get_db)) -> schemas.Item:
    """
    Create a new found item. Insert it in the database.

    Args:
        request (Request): The request object containing information about the request.
        description (str, optional): The description of the item. Defaults to Form(...).
        tag (str, optional): The tag associated with the item. Defaults to Form(...).
        image (Optional[UploadFile], optional): The image file associated with the item (optional). The image will be stored in the associated AWS S3 Bucket. Defaults to File(...).
        dropoff_point_id (int, optional): The ID of the drop-off point associated with the item. Defaults to Form(...).
        db (Session, optional): Optional database session object. If not included the system will connect to the default one. Defaults to Depends(get_db).

    Returns:
        schemas.Item: The created item.
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

# REPORT A NEW ITEM (UNAUTHENTICATED USER)

@app.post("/inventory/v1/items/report",
          response_description = "Report a new lost item.",
          response_model = schemas.Item,
          tags = ["Items"],
          status_code = status.HTTP_201_CREATED)
def report_item(description: str = Form(...),
                tag: str = Form(...),
                image: Optional[UploadFile] = File(...),
                report_email: str = Form(...),
                db: Session = Depends(get_db)) -> schemas.Item:
    """
    Report a new lost item.

    Args:
        description (str, optional): The description of the item. Defaults to Form(...).
        tag (str, optional): The tag associated with the item. Defaults to Form(...).
        image (Optional[UploadFile], optional): The image file associated with the item (optional). The image will be stored in the associated AWS S3 Bucket. Defaults to File(...).
        report_email (str, optional): The email of the person reporting the item. Defaults to Form(...).
        db (Session, optional): Optional database session object. If not included the system will connect to the default one. Defaults to Depends(get_db).

    Returns:
        schemas.Item: The reported item.
    """    
    if image == None or image.content_type not in ["image/jpeg", "image/png", "image/jpg"]:
        image = None

    item = schemas.ItemReport(description=description,
                              tag=tag,
                              image=image,
                              report_email=report_email
                              )
    return crud.report_item(db = db, new_item = item)

# DELETE EXISTING ITEM (AUTHENTICATED USER)

@app.delete("/inventory/v1/items/id/{item_id}",
            response_description = "Delete a specific item by its ID.",
            response_model = dict,
            tags = ["Items"],
            status_code = status.HTTP_200_OK)
def delete_item(request: Request,
                item_id: str,
                db: Session = Depends(get_db)):
    """
    Delete a specific item by its ID.

    Args:
        request (Request): The request object containing information about the request.
        item_id (str): The ID of the item to be deleted.
        db (Session, optional): Optional database session object. If not included the system will connect to the default one. Defaults to Depends(get_db).

    Raises:
        HTTPException (HTTP_400_BAD_REQUEST): Error raised if item_id is not numeric.
        HTTPException (HTTP_204_NO_CONTENT): Error raised if there's no stored item with the item_id.

    Returns:
        _type_: A dictionary containing a success message.
    """    
    auth.verify_access(request)
    try:
        item_id = int(item_id)
    except ValueError:
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = invalid_id_message)
    
    if crud.delete_item(db, item_id) == None:
        raise HTTPException(status_code = status.HTTP_204_NO_CONTENT, detail = item_not_found_message)
    return {"message": "ITEM DELETED"}

# GET IMAGE FROM S3 BUCKET (UNAUTHENTICATED USER)

@app.get("/inventory/v1/image/{image_uuid}",
         response_description = "A StreamingResponse object containing the image data.",
         tags = ["Items"],
         status_code = status.HTTP_200_OK)
def get_image_from_s3(image_uuid: str):
    """
    Retrieve the image presigned URL from S3 Bucket B.

    Args:
        image_uuid (str): A string representing the unique identifier for the image.

    Returns:
        StreamingResponse: Object containing the image data.
    """    
    return crud.get_image_from_s3(image_uuid)

if __name__  == '__main__':
    run(app, host = '0.0.0.0', port = 8000)