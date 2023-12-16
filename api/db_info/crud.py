import boto3
import os
import uuid

from typing import List, Optional
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from botocore.exceptions import NoCredentialsError
from . import models, schemas, contact

def get_s3():
    """
    Returns a boto3 S3 client with the AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY
    environment variables.

    :return: The S3 client
    """
    return boto3.client(
        's3',
        aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
    )

def upload_file_to_s3(file, s3_file_name):
    """
    Uploads a file to an S3 bucket.

    :param file: The file object to be uploaded.
    :param s3_file_name: The desired file name to be used in the S3 bucket.
    :return: Returns the file name if successfully uploaded, otherwise returns None.

    :raises FileNotFoundError: If the file is not found.
    :raises NoCredentialsError: If the AWS credentials are not found.
    :raises Exception: If any other error occurs during file upload.
    """
    s3 = get_s3()
    try:
        bucket_name = os.getenv('AWS_BUCKET_NAME')
        s3.upload_fileobj(file.file, bucket_name, s3_file_name)
        return s3_file_name
    except FileNotFoundError:
        print("ERROR:\tFileNotFoundError")
        return None
    except NoCredentialsError:
        print("ERROR:\tNoCredentialsError")
        return None
    except Exception:
        return None

def delete_file_from_s3(s3_file_name):
    """
    Delete a file from AWS S3.

    :param s3_file_name: The name of the file to be deleted from S3.
    :return: True if the file was successfully deleted, False otherwise.
    """
    s3 = get_s3()
    try:
        s3.delete_object(Bucket=os.getenv('AWS_BUCKET_NAME'), Key=s3_file_name)
        return True
    except Exception:
        print("ERROR:\tException")
        return False

def get_image_from_s3(uuid: str) -> StreamingResponse:
    """
    Get an image from Amazon S3.

    :param uuid: The unique identifier of the image.
    :type uuid: str
    :return: A StreamingResponse object containing the image data.
    :rtype: StreamingResponse
    """
    s3_client = get_s3()
    bucket_name = os.getenv('AWS_BUCKET_NAME')

    response = s3_client.get_object(Bucket=bucket_name, Key=uuid)
    return StreamingResponse(response['Body'], media_type=response['ContentType'])

def update_retrieved_to_archived_items(db: Session, items: List[models.Item]):
    """
    :param db: The database session object.
    :param items: A list of Item objects to be updated.
    :return: A boolean indicating whether any items were updated.

    This method takes in a database session object and a list of Item objects. It iterates through each item in the list and checks if the retrieved_date is not None and if it is older than
    * one week from the current datetime. If both conditions are met, the item's state is set to "archived", removed from the original items list, and added to the update_items list. A flag
    * is set to True if any items were updated.

    If the flag is True, the update_items list is flushed to the database and committed. Finally, the method returns the flag indicating whether any items were updated.
    """
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
    """
    :param db: The database session used for querying items.
    :param update_items: A boolean value indicating whether to update retrieved items to archived items.
    :return: A list of Item objects.

    This method queries the database for all items, ordered by insertion date in descending order. If the update_items parameter is True and there are retrieved items, those items will be
    * updated to archived items using the update_retrieved_to_archived_items() method. After the update, the method queries the database again to retrieve all items.

    Example usage:
        db = get_db_session()
        items = get_items(db, update_items=True)
    """
    items = db.query(models.Item).order_by(models.Item.insertion_date.desc()).all()
    if update_items and any([item.state == "retrieved" for item in items]):
        updating_items = [item for item in items if item.state == "retrieved"]
        if update_retrieved_to_archived_items(db, updating_items):
            items = db.query(models.Item).all()
    return items

def get_item_by_id(db: Session, id: int, update_items: bool = True) -> Optional[models.Item]:
    """
    :param db: The database session object.
    :param id: The ID of the item to retrieve.
    :param update_items: Determines whether to update the retrieved items or not. Defaults to True.
    :return: The item with the specified ID if found, otherwise None.

    This method retrieves an item from the database based on its ID. If the `update_items` parameter is set to True, it checks if the retrieved item's state is "retrieved" and updates it
    * to "archived" using the `update_retrieved_to_archived_items` method. The method then returns the retrieved item.
    """
    item = db.query(models.Item).filter(models.Item.id == id).first()
    if update_items and item != None and item.state == "retrieved":
        if update_retrieved_to_archived_items(db, [item]):
            item.state = "archived"
    return item

def get_stored_items(db: Session, filter: dict):
    """
    :param db: The database session object
    :param filter: A dictionary containing filter criteria for the query
    :return: A list of stored items that match the filter criteria

    This method retrieves stored items from the database based on the provided filter criteria. The method takes a database session object and a filter dictionary as parameters, and returns
    * a list of stored items.

    The filter dictionary can contain the following keys:
    - "tag": Specifies a particular tag value that the items must have
    - "dropoff_point_id": Specifies a particular dropoff point ID that the items must belong to

    If the filter dictionary contains the key "tag", the method filters the items by matching the tag value. If the filter dictionary contains the key "dropoff_point_id", the method filters
    * the items by matching the dropoff point ID. If no filter criteria are provided, all stored items are returned.

    The items are retrieved from the database using a query with the following conditions:
    - The item state must be "stored"
    - If the key "tag" is present in the filter dictionary, the item tag must match the specified tag value
    - If the key "dropoff_point_id" is present in the filter dictionary, the item dropoff point ID must match the specified ID

    The items are sorted in descending order based on the insertion date and returned as a list.
    """
    query = db.query(models.Item).filter(models.Item.state == "stored")
    if ("tag" in filter):
        query = query.filter(models.Item.tag == filter["tag"])
    if ("dropoff_point_id" in filter):
        query = query.filter(models.Item.dropoff_point_id == filter["dropoff_point_id"])
    items = query.order_by(models.Item.insertion_date.desc()).all()
    return items

def get_dropoff_point_items(db: Session, dropoff_point_id: int, filter: dict, update_items: bool = True):
    """

    This method retrieves items associated with a specific dropoff point.

    :param db: The database session object.
    :param dropoff_point_id: The ID of the dropoff point.
    :param filter: A dictionary specifying filters for the items. Supported filters are "tag" and "state".
    :param update_items: A boolean value indicating whether to update retrieved items to archived state. Defaults to True.
    :return: A list of items matching the specified criteria.

    Example usage:

    ```python
    db = get_database_session()
    dropoff_point_id = 123
    filter = {
        "tag": "example",
        "state": "retrieved"
    }
    items = get_dropoff_point_items(db, dropoff_point_id, filter, update_items=True)
    for item in items:
        print(item.name)
    ```

    """
    query = db.query(models.Item).filter(models.Item.dropoff_point_id == dropoff_point_id)
    if ("tag" in filter):
       query = query.filter(models.Item.tag == filter["tag"])
    if ("state" in filter):
        query = query.filter(models.Item.state == filter["state"])
    items = query.all()
    
    if update_items and any([item.state in ["retrieved", "archived"] for item in items]):
        updating_items = [item for item in items if item.state == "retrieved"]
        update_retrieved_to_archived_items(db, updating_items) 
        items = query.order_by(models.Item.insertion_date.desc()).all()
    
    return items

def create_item(db: Session, new_item: schemas.ItemCreate) -> models.Item:
    """
    Create an item in the database.

    :param db: The database session to use.
    :param new_item: The item to create, defined by the schemas.ItemCreate model.
    :return: The created item, defined by the models.Item model.
    """
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

    contact.contact_reported_email(db, new_item)
        
    db.add(db_item)
    db.commit()
    return db_item

def report_item(db: Session, new_item: schemas.ItemReport) -> models.Item:
    """
    This method `report_item` is used to report a new item and store it in the database. It receives two parameters, `db` and `new_item`, and returns an instance of the `Item` model.

    :param db: The database session object.
    :type db: Session
    :param new_item: The item to be reported.
    :type new_item: ItemReport
    :return: The newly created item.
    :rtype: Item
    """
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
    
    contact.contact_new_report(db_item)
    
    return db_item

def retrieve_item(db: Session, id: int, retrieved_email: str) -> Optional[models.Item]:
    """
    :param db: The session object for database operations.
    :param id: The ID of the item to retrieve.
    :param retrieved_email: The email of the person retrieving the item.
    :return: The retrieved item if it exists, otherwise None.

    This method retrieves an item from the database using the provided ID. If the item is found and its state is "stored", the state is changed to "retrieved" and the retrieved email and
    * date are updated. The changes are then flushed and committed to the database.

    After retrieving the item, the contact.contact_netrieved_email method is called to perform additional actions related to the retrieval.

    Finally, the retrieved item is returned.
    """
    db_item = get_item_by_id(db, id)
    if db_item == None:
        return None
    if db_item.state == "stored":
        db_item.state = "retrieved"
        db_item.retrieved_email = retrieved_email
        db_item.retrieved_date = str(datetime.now())
        db.flush([db_item])
        db.commit()
        
    contact.contact_netrieved_email(db_item)
    
    return db_item

def delete_item(db: Session, id: int) -> Optional[str]:
    """
    Deletes an item from the database by its ID.

    :param db: The database session.
    :param id: The ID of the item to be deleted.
    :return: Returns "OK" if the item is deleted successfully, otherwise returns None.
    """
    db_item = get_item_by_id(db, id)
    if db_item == None:
        return None
    if db_item.image != None:
        s3_image_file_name = db_item.image.split('/')[-1]
        delete_file_from_s3(s3_image_file_name)
    db.delete(db_item)
    db.commit()
    return "OK"
