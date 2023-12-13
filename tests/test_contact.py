import datetime
from pytest import fixture
from unittest.mock import patch
from api.db_info import schemas, database, crud, contact, models

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


@patch("api.db_info.contact.send_email")
def test_contact_reported_email(mock_send_email, db):
    mock_send_email.return_value = None
    
    new_item = schemas.ItemReport(
        description = "new_item_description",
        tag = "new_item_tag",
        image = None,
        report_email = "new_item_report_email"
    )
    
    crud.report_item(db = db, new_item = new_item)
    
    new_item = schemas.ItemCreate(
        description = "new_item_description",
        tag = "new_item_tag",
        image = None,
        dropoff_point_id = 1
    )
    
    crud.create_item(db = db, new_item = new_item)
    
    mock_send_email.assert_called()
    
@patch("api.db_info.contact.send_email")
def test_contact_new_report(mock_send_email):
    mock_send_email.return_value = None
    
    dummy_item = schemas.ItemReport(
        description = "new_item_description",
        tag = "new_item_tag",
        image = None,
        report_email = "new_item_report_email"
    )

    contact.contact_new_report(dummy_item)
    
    mock_send_email.assert_called()
    
@patch("api.db_info.contact.send_email")
def test_contact_netrieved_email(mock_send_email):
    mock_send_email.return_value = None
    
    item = schemas.Item(id = 1,
        description = "item_bucket_0",
        tag = "tag1",
        image = "image",
        state = "stored", 
        dropoff_point_id = 2,
        insertion_date = datetime.datetime.now(),
        report_email = None,
        retrieved_email = "dummy_email", 
        retrieved_date = "dummy_datetime")
    
    contact.contact_netrieved_email(item)
    
    mock_send_email.assert_called()