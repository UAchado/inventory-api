import os
import smtplib

from typing import List, Optional
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from . import models, schemas

def update_retrieved_to_archived_items(db: Session, items: List[models.Item]):
    print("UPDATING POSSIBLE NOT ARCHIVED ITEMS!")
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
            smtp_server = os.environ.get("SMTP_SERVER")
            smtp_port = int(os.environ.get("SMTP_PORT", int()))
            username = os.environ.get("EMAIL_USERNAME")
            password = os.environ.get("EMAIL_PASSWORD")
            message = f"Um item caracterizado como {new_item.tag} acabou de ser uachado em um dos nossos pontos.\n Dá uma olhada, pode ser que seja teu!\n\nna UA, nada se perde, tudo se UAcha"

            msg = MIMEMultipart()
            msg["From"] = username
            msg["To"] = report.report_email
            msg["Subject"] = "Um item que reportaste, acaba de ser UACHADO!"
            msg.attach(MIMEText(message, "plain"))
            
            send_email(smtp_server, smtp_port, username, password, msg, report.report_email)

            notified_mails.append(report.report_email)
            
def send_email(smtp_server, smtp_port, username, password, msg, report_email):
    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(username, password)
            server.send_message(msg)
            print(f"INFO:\tEMAIL SENT TO: {report_email}")
    except smtplib.SMTPServerDisconnected:
        print("ERROR:\tServer disconnected unexpectedly.")
    except Exception as e:
        print(f"Error:\t{e}")

def create_item(db: Session, new_item: schemas.ItemCreate) -> models.Item:
    
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
    db.delete(db_item)
    db.commit()
    return "OK"
