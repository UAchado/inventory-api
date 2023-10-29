from fastapi.testclient import TestClient
from unittest.mock import patch
from api import main

client = TestClient(main.app)

def test_base():
    response = client.get("/v1/")
    assert response.status_code == 200
    assert response.json() == {"response": "Hello World!"}

@patch("api.main.crud.get_items")
def test_get_all_items(mock_get_items):
    mock_items = [
        {"id": 1, "description": "item1", "tag": "tag1", "image": "image1", "state": "state1", "dropoffPoint_id": 1, "mail": "mail1"},
        {"id": 2, "description": "item2", "tag": "tag2", "image": "image2", "state": "state2", "dropoffPoint_id": 2, "mail": "mail2"}
    ]

    mock_get_items.return_value = mock_items
    
    response = client.get("/v1/items/")
    assert response.status_code == 200
    assert response.json() == mock_items

@patch("api.main.crud.get_item_by_id")
def test_get_item_by_id(mock_get_item_by_id):
    mock_item = {"id": 1, "description": "item1", "tag": "tag1", "image": "image1", "state": "state1", "dropoffPoint_id": 1, "mail": "mail1"}
    mock_get_item_by_id.return_value = mock_item
    
    response = client.get("/v1/items/id/1")
    assert response.status_code == 200
    assert response.json() == mock_item

    response = client.get("/v1/items/id/abc")
    assert response.status_code == 400
    assert response.json() == {"detail": "INVALID ID FORMAT"}

    mock_get_item_by_id.return_value = None
    response = client.get("/v1/items/id/999")
    assert response.status_code == 204


@patch("api.main.crud.get_item_by_id")
@patch("api.main.crud.retrieve_item")
def test_retrieve_item(mock_retrieve_item, mock_get_item_by_id):
    mock_get_item_by_id.return_value = {"id": 1, "description": "item1", "tag": "tag1", "image": "image1", "state": "state1", "dropoffPoint_id": 1, "mail": None}
    
    retrieved_mock_item = {"id": 1, "description": "item1", "tag": "tag1", "image": "image1", "state": "retrieved", "dropoffPoint_id": None, "mail": None}
    mock_retrieve_item.return_value = retrieved_mock_item
    
    response = client.get("/v1/items/retrieve/1")
    assert response.status_code == 200
    assert response.json() == retrieved_mock_item

    response = client.get("/v1/items/retrieve/abc")
    assert response.status_code == 400
    assert response.json() == {"detail": "INVALID ID FORMAT"}

    mock_retrieve_item.return_value = None
    response = client.get("/v1/items/retrieve/999")
    assert response.status_code == 204


@patch("api.main.crud.get_item_by_id")
@patch("api.main.crud.create_item")
def test_create_item(mock_create_item, mock_get_item_by_id):
    mock_get_item_by_id.return_value = None
    mock_item = {"id": 1, "description": "item1", "tag": "tag1", "image": "image1", "state": "state1", "dropoffPoint_id": 1, "mail": "mail1"}
    mock_create_item.return_value = mock_item
    
    response = client.post("/v1/items/", json = {"description": "item1", "tag": "tag1", "image": "image1", "state": "state1", "dropoffPoint_id": 1, "mail": "mail1"})
    assert response.status_code == 201
    assert response.json() == mock_item

@patch("api.main.crud.get_item_by_id")
@patch("api.main.crud.delete_item")
def test_delete_item(mock_delete_item, mock_get_item_by_id):
    mock_item = {"id": 1, "description": "item1", "tag": "tag1", "image": "image1", "state": "state1", "dropoffPoint_id": 1, "mail": "mail1"}
    mock_get_item_by_id.return_value = mock_item
    mock_delete_item.return_value = "OK"
    
    response = client.delete("/v1/items/id/1")
    assert response.status_code == 200
    assert response.json() == {"message": "ITEM DELETED"}

    response = client.delete("/v1/items/id/abc")
    assert response.status_code == 400
    assert response.json() == {"detail": "INVALID ID FORMAT"}

    mock_delete_item.return_value = None
    response = client.delete("/v1/items/id/999")
    assert response.status_code == 204