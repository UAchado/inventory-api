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

def test_get_items_no_flag(db):
    
    items = crud.get_items(db = db, update_items = False)
    assert len(items) == 0
    assert items == []

    add_items_to_db(db, item_bucket)

    items = crud.get_items(db = db, update_items = False)
    print(items)
    assert len(items) == 4
    assert items[0].description == "item_bucket_0"

@patch("api.db_info.crud.update_retrieved_to_archived_items")
def test_get_items_with_flag(mock_update_retrieved, db):
    items = crud.get_items(db = db, update_items = True)
    assert len(items) == 0
    assert items == []

    add_items_to_db(db, [item_bucket[2]])

    mock_update_retrieved.return_value = True
    items = crud.get_items(db = db, update_items = True)
    print(items)
    mock_update_retrieved.assert_called()
    assert len(items) == 1
    mock_update_retrieved.assert_called()
    assert items[0].state == "retrieved"

# def test_get_items_no_flag(db):

# def test_create_item(db):
#     # Create a new item using your CRUD function
#     new_item_data = schemas.ItemCreate(description="Test item",
#                                        tag="test",
#                                        image="image.jpg",
#                                        dropoff_point_id=1)
#     created_item = crud.create_item(db=db, new_item=new_item_data)
#     assert created_item.description == "Test item"

#     # Verify that the item was added to the database
#     items = crud.get_items(db=db)
#     assert len(items) == 1
#     assert items[0].description == "Test item"

