from sqlalchemy.orm import Session

from . import models, schemas

def get_items(db: Session):
    return db.query(models.Item).all()

def get_item_by_id(db: Session, id: int):
    return db.query(models.Item).filter(models.Item.id == id).first()

def get_items_by_tag(db: Session, tag: str):
    return db.query(models.Item).filter(models.Item.tag == tag).all()

def contact_by_email(db: Session, new_item: schemas.ItemCreate):
    items = [
        item for item in get_items_by_tag(db, new_item.tag)
        if item.dropoffPoint_id == None and item.mail != None
    ]
    for item in items:
        notified_mails = []
        if item.mail not in notified_mails:
            message = f"A item classified as {new_item.tag} has been found in {new_item.dropoffPoint_id}. Take a look it might be yours!"

            # TODO: Contact using e-mail account

            notified_mails.append(item.mail)

def create_item(db: Session, new_item: schemas.ItemCreate):
    
    # Get all the items with the same tag
    db_item = None

    if new_item.tag != None and new_item.dropoffPoint_id != None :
        contact_by_email(db, new_item)

        # Inset the new item in the database

        db_item = models.Item(description = new_item.description, 
            tag = new_item.tag, 
            image = new_item.image, 
            state = "stored",
            dropoffPoint_id = new_item.dropoffPoint_id, 
            mail = None)
        
    elif new_item.mail != None and new_item.dropoffPoint_id == None:
        db_item = models.Item(description = new_item.description, 
            tag = new_item.tag, 
            image = new_item.image, 
            state = "reported",
            dropoffPoint_id = None, 
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
