from fastapi.testclient import TestClient
from unittest.mock import patch
from api import main

client = TestClient(main.app)

def test_base():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"response": "Hello World!"}

@patch("api.main.crud.get_items")
def test_get_all_items(mock_get_items):
    mock_items = [
        {"id": 1, "description": "item1", "tag": "tag1", "image": "image1", "state": "state1", "dropoffPoint_id": 1, "mail": "mail1"},
        {"id": 2, "description": "item2", "tag": "tag2", "image": "image2", "state": "state2", "dropoffPoint_id": 2, "mail": "mail2"}
    ]

    mock_get_items.return_value = mock_items
    
    response = client.get("/items/")
    assert response.status_code == 200
    assert response.json() == mock_items

@patch("api.main.crud.get_item_by_id")
@patch("api.main.crud.create_item")
def test_create_item(mock_create_item, mock_get_item_by_id):
    mock_get_item_by_id.return_value = None
    mock_item = {"id": 1, "description": "item1", "tag": "tag1", "image": "image1", "state": "state1", "dropoffPoint_id": 1, "mail": "mail1"}
    mock_create_item.return_value = mock_item
    
    response = client.post("/items/", json = {"description": "item1", "tag": "tag1", "image": "image1", "state": "state1", "dropoffPoint_id": 1, "mail": "mail1"})
    assert response.status_code == 201
    assert response.json() == mock_item

@patch("api.main.crud.get_item_by_id")
@patch("api.main.crud.retrieve_item")
def test_retrieve_item(mock_create_item, mock_get_item_by_id):
    mock_get_item_by_id.return_value = None
    mock_item = {"id": 1, "description": "item1", "tag": "tag1", "image": "image1", "state": "state1", "dropoffPoint_id": 1, "mail": None}
    mock_create_item.return_value = mock_item
    
    response = client.put("/items/retrieve/", json = {"description": "item1", "tag": "tag1", "image": "image1", "state": "retrieved", "dropoffPoint_id": None, "mail": None})
    assert response.status_code == 200
    assert response.json() == mock_item

@patch("api.main.crud.get_item_by_id")
@patch("api.main.crud.delete_item")
def test_delete_item(mock_delete_item, mock_get_item_by_id):
    mock_item = {"id": 1, "description": "item1", "tag": "tag1", "image": "image1", "state": "state1", "dropoffPoint_id": 1, "mail": "mail1"}
    mock_get_item_by_id.return_value = mock_item
    mock_delete_item.return_value = "OK"
    
    response = client.delete("/items/id/1")
    assert response.status_code == 200
    assert response.json() == {"message": "Item deleted"}