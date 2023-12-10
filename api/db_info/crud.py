import boto3
import os
import uuid

from typing import List, Optional
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from botocore.exceptions import NoCredentialsError
from . import models, schemas

def get_s3():
    return boto3.client(
        's3',
        aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
    )

def upload_file_to_s3(file, s3_file_name):
    s3 = get_s3()
    try:
        bucket_name = os.getenv('AWS_BUCKET_NAME')
        s3.upload_fileobj(file.file, bucket_name, s3_file_name)
        return s3_file_name
    except FileNotFoundError:
        print("ERROR:\t\tFileNotFoundError")
        return None
    except NoCredentialsError:
        print("ERROR:\t\tNoCredentialsError")
        return None
    except Exception:
        return None

def delete_file_from_s3(s3_file_name):
    s3 = get_s3()
    try:
        s3.delete_object(Bucket=os.getenv('AWS_BUCKET_NAME'), Key=s3_file_name)
        return True
    except Exception:
        print("ERROR:\t\tException")
        return False

def get_image_from_s3(uuid: str):
    s3_client = get_s3()
    bucket_name = os.getenv('AWS_BUCKET_NAME')

    response = s3_client.get_object(Bucket=bucket_name, Key=uuid)
    return StreamingResponse(response['Body'], media_type=response['ContentType'])

def update_retrieved_to_archived_items(db: Session, items: List[models.Item]):
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

def get_items(db: Session, update_items: bool = True) -> List[models.Item]:
    items = db.query(models.Item).all()
    if update_items and any([item.state == "retrieved" for item in items]):
        updating_items = [item for item in items if item.state == "retrieved"]
        if update_retrieved_to_archived_items(db, updating_items):
            items = db.query(models.Item).all()
    return items

def get_item_by_id(db: Session, id: int, update_items: bool = True) -> Optional[models.Item]:
    item = db.query(models.Item).filter(models.Item.id == id).first()
    if update_items and item != None and item.state == "retrieved":
        if update_retrieved_to_archived_items(db, [item]):
            item.state = "archived"
    return item

def get_stored_items(db: Session, filter: dict):
    query = db.query(models.Item).filter(models.Item.state == "stored")
    if ("tag" in filter):
        query = query.filter(models.Item.tag == filter["tag"])
    if ("dropoff_point_id" in filter):
        query = query.filter(models.Item.dropoff_point_id == filter["dropoff_point_id"])
    items = query.all()
    return items

def get_dropoff_point_items(db: Session, dropoff_point_id: int, filter: dict, update_items: bool = True):
    query = db.query(models.Item).filter(models.Item.dropoff_point_id == dropoff_point_id)
    if ("tag" in filter):
       query = query.filter(models.Item.tag == filter["tag"])
    if ("state" in filter):
        query = query.filter(models.Item.state == filter["state"])
    items = query.all()
    
    if update_items and any([item.state in ["retrieved", "archived"] for item in items]):
        updating_items = [item for item in items if item.state == "retrieved"]
        update_retrieved_to_archived_items(db, updating_items) 
        items = query.all()
    
    return items

def contact_by_email(db: Session, new_item: schemas.ItemCreate):
    stored_reports = [
        item for item in db.query(models.Item).filter(models.Item.tag == new_item.tag).all()
        if item.report_email != None
    ]
    for report in stored_reports:
        notified_mails = []
        if report.report_email not in notified_mails:
            message = f"A item classified as {new_item.tag} has been found in {new_item.dropoff_point_id}. Take a look it might be yours!"

            # TODO: Contact using e-report_email account

            notified_mails.append(report.report_email)

def create_item(db: Session, new_item: schemas.ItemCreate) -> models.Item:
    
    if new_item.image != None:
        new_item.image = upload_file_to_s3(new_item.image, str(uuid.uuid4()))
    
    db_item = models.Item(description = new_item.description,
                          tag = new_item.tag,
                          image = new_item.image,
                          state = "stored",
                          dropoff_point_id = new_item.dropoff_point_id,
                          report_email = None,
                          retrieved_email = None,
                          retrieved_date = None)
            
    contact_by_email(db, new_item)
        
    db.add(db_item)
    db.commit()
    return db_item

def report_item(db: Session, new_item: schemas.ItemReport) -> models.Item:
    
    if new_item.image != None:
        new_item.image = upload_file_to_s3(new_item.image, str(uuid.uuid4()))
    
    db_item = models.Item(description = new_item.description,
                          tag = new_item.tag,
                          image = new_item.image,
                          state = "reported",
                          dropoff_point_id = None,
                          report_email = new_item.report_email,
                          retrieved_email = None,
                          retrieved_date = None)
            
    db.add(db_item)
    db.commit()
    return db_item

def retrieve_item(db: Session, id: int, retrieved_email: str) -> Optional[models.Item]:
    db_item = get_item_by_id(db, id)
    if db_item == None:
        return None
    if db_item.state == "stored":
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
    if db_item.image != None:
        s3_image_file_name = db_item.image.split('/')[-1]
        delete_file_from_s3(s3_image_file_name)
    db.delete(db_item)
    db.commit()
    return "OK"
