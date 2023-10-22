from fastapi import FastAPI, Depends, HTTPException
import uvicorn

from sqlalchemy.orm import Session

from db_info import crud, models, schemas, database 

models.Base.metadata.create_all(bind=database.engine)

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

@app.get("/items/", response_model = list[schemas.Item])                # UAC-44
def get_all_items(db: Session = Depends(get_db)):
    items = crud.get_items(db)
    return items

@app.post("/items/", response_model=schemas.Item)                                        # UAC-48
def create_item(item: schemas.ItemCreate, db: Session = Depends(get_db)):
    db_item = crud.get_item_by_id(db, id=item.id)
    if db_item:
        raise HTTPException(status_code=400, detail="Item already registered")
    return crud.create_item(db=db, new_item=item)

if __name__  == '__main__':
    uvicorn.run(app, host = 'localhost', port = 8000)