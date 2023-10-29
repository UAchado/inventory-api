from sqlalchemy.orm import Session

from . import models, schemas

def get_items(db: Session):
    return db.query(models.Item).all()

def get_item_by_id(db: Session, id: int):
    return db.query(models.Item).filter(models.Item.id == id).first()

def create_item(db: Session, new_item: schemas.ItemCreate):
    db_item = models.Item(description = new_item.description, 
                          tag = new_item.tag, 
                          image = new_item.image, 
                          state = new_item.state,
                          dropoffPoint_id = new_item.dropoffPoint_id, 
                          mail = new_item.mail)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def retrieve_item(db: Session, id: int):
    db_item = get_item_by_id(db, id)
    if db_item == None:
        return None
    if db_item.dropoffPoint_id != None and db_item.mail == None:
        db_item.state = "retrieved"
        db_item.dropoffPoint_id = None
        db.flush()
        db.commit()
    return db_item

def delete_item(db: Session, id: int):
    db_item = get_item_by_id(db, id)
    if db_item == None:
        return None
    db.delete(db_item)
    db.commit()
    return "OK"
