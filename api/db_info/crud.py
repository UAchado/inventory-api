from typing import List, Optional
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from . import models, schemas

def update_retrieved_to_archived_items(db: Session, items: List[models.Item]):
    print("UPDATING POSSIBLE NOT ARCHIEVED ITEMS!")
    flag = False
    update_items = []
    for item in items:
        if item.retrieved_date != None and \
        datetime.strptime(item.retrieved_date, '%Y-%m-%d %H:%M:%S.%f') + timedelta(weeks=1) < datetime.now():
            item.state = "archived"
            items.remove(item)
            update_items.append(item)
            flag = True
    if flag:
        db.flush(update_items)
        db.commit()
    return flag

def get_items(db: Session, filter = True) -> List[models.Item]:
    items = db.query(models.Item).all()
    if filter and any([item.state == "retrieved" for item in items]):
        updating_items = [item for item in items if item.state == "retrieved"]
        if update_retrieved_to_archived_items(db, updating_items):
            items = db.query(models.Item).all()
    return items

def get_item_by_id(db: Session, id: int, filter = True) -> Optional[models.Item]:
    item = db.query(models.Item).filter(models.Item.id == id).first()
    if filter and item != None and item.state == "retrieved":
        if update_retrieved_to_archived_items(db, [item]):
            item.state = "archived"
    return item

def get_items_by_state(db: Session, state: str, filter = True) -> List[models.Item]:
    
    # Check if the list is 
    if filter and (state == "retrieved" or state == "archived"):
        updating_items = db.query(models.Item).filter(models.Item.state == "retrieved").all()
        update_retrieved_to_archived_items(db, updating_items)
    
    return db.query(models.Item).filter(models.Item.state == state).all()

def get_items_by_tag(db: Session, tag: str) -> List[models.Item]:
    items = db.query(models.Item).filter(models.Item.tag == tag).all()
    if filter and any([item.state == "retrieved" for item in items]):
        updating_items = [item for item in items if item.state == "retrieved"]
        if update_retrieved_to_archived_items(db, updating_items):
            items = db.query(models.Item).filter(models.Item.tag == tag).all()
    return items

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

def create_item(db: Session, new_item: schemas.ItemCreate) -> Optional[models.Item]:
    
    # Get all the items with the same tag
    db_item = None

    if new_item.tag != None and new_item.dropoffPoint_id != None :
        contact_by_email(db, new_item)
        db_item = models.Item(description = new_item.description, 
            tag = new_item.tag, 
            image = new_item.image, 
            state = "stored",
            dropoffPoint_id = new_item.dropoffPoint_id, 
            mail = None,
            retrieved_email = None,
            retrieved_date = None)
        
    elif new_item.mail != None and new_item.dropoffPoint_id == None:
        db_item = models.Item(description = new_item.description, 
            tag = new_item.tag, 
            image = new_item.image, 
            state = "reported",
            dropoffPoint_id = None, 
            mail = new_item.mail,
            retrieved_email = None,
            retrieved_date = None)
        
    db.add(db_item)
    db.commit()
    # db.refresh(db_item)
    return db_item

def retrieve_item(db: Session, id: int, retrieved_email: str) -> Optional[models.Item]:
    db_item = get_item_by_id(db, id)
    if db_item == None:
        return None
    if db_item.dropoffPoint_id != None and db_item.mail == None:
        db_item.state = "retrieved"
        db_item.retrieved_email = retrieved_email
        db_item.retrieved_date = str(datetime.now())
        db.flush([db_item])
        db.commit()
    return db_item

def delete_item(db: Session, id: int) -> Optional[str]:
    db_item = get_item_by_id(db, id)
    if db_item == None:
        return None
    db.delete(db_item)
    db.commit()
    return "OK"
