from typing import List
from pytest import fixture
from unittest.mock import patch
from sqlalchemy.orm import Session
from api.db_info import schemas, database, crud, models

## HELPER COMPONENTS

item_bucket = [
    models.Item(description = "item_bucket_0", tag = "tag1", image = "image", state = "stored", dropoff_point_id = 2, report_email = None, retrieved_email = None, retrieved_date = None),
    models.Item(description = "item_bucket_1", tag = "tag1", image = "image", state = "reported", dropoff_point_id = None, report_email = "report_email", retrieved_email = None, retrieved_date = None),
    models.Item(description = "item_bucket_2", tag = "tag2", image = "image", state = "retrieved", dropoff_point_id = 2, report_email = None, retrieved_email = "retrieved_email", retrieved_date = "retrieved_date"),
    models.Item(description = "item_bucket_3", tag = "tag2", image = "image", state = "archived", dropoff_point_id = 1, report_email = None, retrieved_email = "retrieved_email", retrieved_date = "retrieved_date"),
]

def add_items_to_db(db: Session, items: List[models.Item]):
    for item in items:
        new_item = models.Item(description = item.description,
                               tag = item.tag,
                               image = item.image,
                               state = item.state,
                               dropoff_point_id = item.dropoff_point_id,
                               report_email = item.report_email,
                               retrieved_email = item.retrieved_email,
                               retrieved_date = item.retrieved_date,
                               )
        db.add(new_item)
    db.commit()

# BEFORE and AFTER

@fixture(scope="function")
def db():
    connection = database.engine.connect()
    transaction = connection.begin()
    session = database.SessionLocal(bind = connection)

    database.Base.metadata.create_all(bind = connection)

    try:
        yield session
    finally:
        transaction.rollback()
        connection.close()

## UNIT TESTS

# FUNCTION get_items

@patch("api.db_info.crud.update_retrieved_to_archived_items")
def test_get_items_no_flag(mock_update_retrieved, db):
    
    items = crud.get_items(db = db, update_items = False)
    assert len(items) == 0
    assert items == []

    add_items_to_db(db, item_bucket)

    items = crud.get_items(db = db, update_items = False)
    assert len(items) == 4
    assert items[0].description == item_bucket[0].description

    mock_update_retrieved.assert_not_called()

@patch("api.db_info.crud.update_retrieved_to_archived_items")
def test_get_items_with_flag(mock_update_retrieved, db):

    # NO ITEMS
    
    items = crud.get_items(db = db, update_items = True)
    assert len(items) == 0
    assert items == []

    mock_update_retrieved.assert_not_called()

    # NO RETRIEVED ITEMS

    add_items_to_db(db, [item_bucket[0]])

    items = crud.get_items(db = db, update_items = True)
    assert len(items) == 1
    assert items[0].state == item_bucket[0].state

    mock_update_retrieved.assert_not_called()

    # RETRIEVED ITEMS TRUE

    add_items_to_db(db, [item_bucket[2]])
    mock_update_retrieved.return_value = True

    items = crud.get_items(db = db, update_items = True)
    assert len(items) == 2
    assert items[1].state == item_bucket[2].state

    mock_update_retrieved.assert_called()

@patch("api.db_info.crud.update_retrieved_to_archived_items")
def test_get_item_by_id(mock_update_retrieved, db):

    item = crud.get_item_by_id(db = db, id = 1, update_items = False)
    assert item == None

    add_items_to_db(db, item_bucket)

    # Retrieve all items to get their IDs
    all_items = crud.get_items(db = db, update_items = False)
    assert len(all_items) != 0

    # Test retrieval of the first item by its actual ID
    first_item_id = all_items[0].id
    item = crud.get_item_by_id(db = db, id = first_item_id, update_items = False)
    assert item != None
    assert item.description == all_items[0].description

    mock_update_retrieved.assert_not_called()

    # FLAG TRUE

    mock_update_retrieved.return_value = True

    item = crud.get_item_by_id(db = db, id = 1, update_items = True)

    mock_update_retrieved.assert_not_called()
    
    # Searching third item (state is retrieved)
    item = crud.get_item_by_id(db = db, id = 3, update_items = True)

    mock_update_retrieved.assert_called()

def get_stored_items(db):
    
    add_items_to_db(db, item_bucket)
    filter = {}
    
    items = crud.get_stored_items(db = db, filter = filter)
    assert len(items) == 1
    assert all(item.state == "stored" for item in items)
    
    filter = {
        "tag": "tag1"
    }
    
    items = crud.get_stored_items(db = db, filter = filter)
    assert len(items) == 1
    assert all(item.state == "stored" for item in items)
    
    filter = {
        "dropoff_point_id": 2
    }
    
    items = crud.get_stored_items(db = db, filter = filter)
    assert len(items) == 0
    assert all(item.state == "stored" for item in items)

@patch("api.db_info.crud.update_retrieved_to_archived_items")
def test_get_dropoff_point_items(mock_update_retrieved, db):
    
    add_items_to_db(db, item_bucket)
    filter = {}
    
    items = crud.get_dropoff_point_items(db = db, dropoff_point_id = 2, filter = filter, update_items = False)
    assert len(items) == 2
    assert all(item.dropoff_point_id == 2 for item in items)
    
    filter = {
        "tag": "tag2"
    }
    
    items = crud.get_dropoff_point_items(db = db, dropoff_point_id = 2, filter = filter, update_items = False)
    assert len(items) == 1
    assert all(item.dropoff_point_id == 2 for item in items)
    
    filter = {
        "state": "stored"
    }
    
    items = crud.get_dropoff_point_items(db = db, dropoff_point_id = 2, filter = filter, update_items = False)
    assert len(items) == 1
    assert all(item.dropoff_point_id == 2 for item in items)
    
    filter = {
        "tag": "tag2",
        "state": "stored"
    }
    
    items = crud.get_dropoff_point_items(db = db, dropoff_point_id = 2, filter = filter, update_items = False)
    assert len(items) == 0
    
    mock_update_retrieved.assert_not_called()
    
    # Flag
    
    mock_update_retrieved.return_value = True
    
    filter = {
        "state": "stored"
    }
    items = crud.get_dropoff_point_items(db = db, dropoff_point_id = 2, filter = filter, update_items = True)
    mock_update_retrieved.assert_not_called()
    
    filter = {}
    items = crud.get_dropoff_point_items(db = db, dropoff_point_id = 2, filter = filter, update_items = True)
    mock_update_retrieved.assert_called()
    

@patch("api.db_info.crud.contact_by_email")
def test_create_item(mock_contact_by_email, db):
    mock_contact_by_email.return_value = None
    
    new_item = schemas.ItemCreate(
        description = "new_item_description",
        tag = "new_item_tag",
        image = "new_item_image",
        dropoff_point_id = 1
    )
    
    item = crud.create_item(db = db, new_item = new_item)
    assert item != None
    assert item.description == new_item.description
    assert item.report_email == None
    
def test_report_item(db):
    
    new_item = schemas.ItemReport(
        description = "new_item_description",
        tag = "new_item_tag",
        image = "new_item_image",
        report_email = "new_item_report_email"
    )
    
    item = crud.report_item(db = db, new_item = new_item)
    assert item != None
    assert item.report_email == new_item.report_email
    assert item.dropoff_point_id == None
    
def test_retrieve_item(db):
    
    add_items_to_db(db, [item_bucket[0]])
    
    items = crud.get_items(db = db)
    assert len(items) == 1
    
    item_in_db = items[0]
    assert item_in_db.state == "stored"
    assert item_in_db.retrieved_email == None
    assert item_in_db.retrieved_date == None
    
    item = crud.retrieve_item(db = db, id = item_in_db.id, retrieved_email = "retrieved_email")
    assert item.state == "retrieved"
    assert item.retrieved_email == "retrieved_email"
    assert item.retrieved_date != None
    
    save_item = item
    
    item = crud.retrieve_item(db = db, id = item_in_db.id, retrieved_email = "retrieved_email")
    assert item.retrieved_date == save_item.retrieved_date
    
def test_delete_item(db):
    
    items = crud.get_items(db = db)
    assert len(items) == 0
    
    return_value = crud.delete_item(db = db, id = 1)
    assert return_value == None
    
    add_items_to_db(db, [item_bucket[0]])
    
    items = crud.get_items(db = db)
    assert len(items) == 1
    
    item_in_db = items[0]
    return_value = crud.delete_item(db = db, id = item_in_db.id)
    assert return_value == "OK"
    
    items = crud.get_items(db = db)
    assert len(items) == 0