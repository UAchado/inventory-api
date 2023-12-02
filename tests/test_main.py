from fastapi.testclient import TestClient
from unittest.mock import patch
from api import main

client = TestClient(main.app)

invalid_id_message = {'detail' : 'INVALID ID FORMAT'}

## UNIT TESTS



## INTEGRATION TESTS

# BASE

def test_base():
    response = client.get("/v1/")
    assert response.status_code == 200
    assert response.json() == {"response": "Hello World!"}

# GET ALL ITEMS

@patch("api.main.crud.get_items")
def test_get_all_items(mock_get_items):
    mock_items = [
        {"id" : 1, "description": "description", "tag": "tag", "image": "image", "state": "stored", "dropoffPoint_id": 1, "report_email": None, "retrieved_email": None, "retrieved_date": None},
        {"id" : 2, "description": "description", "tag": "tag", "image": "image", "state": "reported", "dropoffPoint_id": None, "report_email": "report_email", "retrieved_email": None, "retrieved_date": None},
        {"id" : 3, "description": "description", "tag": "tag", "image": "image", "state": "retrieved", "dropoffPoint_id": 1, "report_email": None, "retrieved_email": "retrieved_email", "retrieved_date": "retrieved_date"},
        {"id" : 4, "description": "description", "tag": "tag", "image": "image", "state": "archived", "dropoffPoint_id": 1, "report_email": None, "retrieved_email": "retrieved_email", "retrieved_date": "retrieved_date"},
    ]

    mock_get_items.return_value = mock_items
    
    response = client.get("/v1/items")
    assert response.status_code == 200
    assert response.json() == mock_items

# GET ITEM BY ID

@patch("api.main.crud.get_item_by_id")
def test_get_item_by_id(mock_get_item_by_id):
    mock_item = {"id" : 1, "description": "description", "tag": "tag", "image": "image", "state": "stored", "dropoffPoint_id": 1, "report_email": None, "retrieved_email": None, "retrieved_date": None}
    mock_get_item_by_id.return_value = mock_item
    
    response = client.get("/v1/items/id/1")
    assert response.status_code == 200
    assert response.json() == mock_item

    response = client.get("/v1/items/id/abc")
    assert response.status_code == 400
    assert response.json() == invalid_id_message

    mock_get_item_by_id.return_value = None
    response = client.get("/v1/items/id/999")
    assert response.status_code == 204

# GET ALL ITEM TAGS

def test_get_all_tags():
    response = client.get("/v1/items/tags")
    assert response.status_code == 200
    assert response.json() == ["Todos","Portáteis","Telemóveis","Tablets","Auscultadores/Fones","Carregadores","Pen drives","Câmaras","Livros","Cadernos","Material de escritório","Carteiras","Chaves","Cartão","Óculos","Joalharia","Casacos","Chapéus/Bonés","Cachecóis","Luvas","Mochilas","Equipamento desportivo","Garrafas de água","Guarda-chuvas","Instrumentos musicais","Material de arte","Bagagem","Produtos de maquilhagem","Artigos de higiene","Medicamentos"]

# GET STORED ITEMS

@patch("api.main.crud.get_stored_items")
def test_get_stored_items(mock_get_stored_items):
    mock_items = [
        {"id" : 1, "description": "description", "tag": "tag1", "image": "image", "state": "stored", "dropoffPoint_id": 1, "report_email": None, "retrieved_email": None, "retrieved_date": None},
        {"id" : 2, "description": "description", "tag": "tag1", "image": "image", "state": "stored", "dropoffPoint_id": 2, "report_email": None, "retrieved_email": None, "retrieved_date": None},
        {"id" : 3, "description": "description", "tag": "tag2", "image": "image", "state": "stored", "dropoffPoint_id": 2, "report_email": None, "retrieved_email": None, "retrieved_date": None},
    ]

    mock_get_stored_items.return_value = mock_items
    response = client.post("/v1/items/stored", json = {"filter": {}})
    assert response.status_code == 200
    assert response.json() == mock_items

    mock_get_stored_items.return_value = [mock_items[0], mock_items[1]]
    response = client.post("/v1/items/stored", json = {"filter": {"tag":"tag1"}})
    assert response.status_code == 200
    assert response.json() == [mock_items[0], mock_items[1]]

    mock_get_stored_items.return_value = [mock_items[1], mock_items[2]]
    response = client.post("/v1/items/stored", json = {"filter": {"dropoffPoint_id":2}})
    assert response.status_code == 200
    assert response.json() == [mock_items[1], mock_items[2]]

    mock_get_stored_items.return_value = [mock_items[2]]
    response = client.post("/v1/items/stored", json = {"filter": {"tag":"tag2", "dropoffPoint_id": 2}})
    assert response.status_code == 200
    assert response.json() == [mock_items[2]]

# GET DROP-OFF POINT ITEMS

@patch("api.main.crud.get_dropoffPoint_items")
def test_get_dropoffPoint_items(mock_get_dropoffPoint_items):
    mock_items = [
        {"id" : 1, "description": "description", "tag": "tag1", "image": "image", "state": "stored", "dropoffPoint_id": 2, "report_email": None, "retrieved_email": None, "retrieved_date": None},
        {"id" : 2, "description": "description", "tag": "tag1", "image": "image", "state": "reported", "dropoffPoint_id": None, "report_email": "report_email", "retrieved_email": None, "retrieved_date": None},
        {"id" : 3, "description": "description", "tag": "tag2", "image": "image", "state": "retrieved", "dropoffPoint_id": 2, "report_email": None, "retrieved_email": "retrieved_email", "retrieved_date": "retrieved_date"},
        {"id" : 4, "description": "description", "tag": "tag2", "image": "image", "state": "archived", "dropoffPoint_id": 1, "report_email": None, "retrieved_email": "retrieved_email", "retrieved_date": "retrieved_date"},
    ]

    mock_get_dropoffPoint_items.return_value = mock_items
    response = client.put("/v1/items/point/1", json = {"filter": {}})
    assert response.status_code == 200
    assert response.json() == mock_items

    mock_get_dropoffPoint_items.return_value = [mock_items[0], mock_items[1]]
    response = client.put("/v1/items/point/1", json = {"filter": {"tag":"tag1"}})
    assert response.status_code == 200
    assert response.json() == [mock_items[0], mock_items[1]]

    mock_get_dropoffPoint_items.return_value = [mock_items[0], mock_items[2]]
    response = client.put("/v1/items/point/1", json = {"filter": {"dropoffPoint_id":2}})
    assert response.status_code == 200
    assert response.json() == [mock_items[0], mock_items[2]]

    for index, state in enumerate(["stored", "reported", "retrieved", "archived"]):
        mock_get_dropoffPoint_items.return_value = [mock_items[index]]
        response = client.put("/v1/items/point/1", json = {"filter": {"state":state}})
        assert response.status_code == 200
        assert response.json() == [mock_items[index]]

    mock_get_dropoffPoint_items.return_value = [mock_items[2]]
    response = client.put("/v1/items/point/1", json = {"filter": {"tag": "tag2", "state": "retrieved", "dropoffPoint_id": 2}})
    assert response.status_code == 200
    assert response.json() == [mock_items[2]]

# RETRIEVE ITEM

@patch("api.main.crud.retrieve_item")
def test_retrieve_item(mock_retrieve_item):
    
    retrieved_mock_item = {"id" : 1, "description": "description", "tag": "tag", "image": "image", "state": "retrieved", "dropoffPoint_id": 1, "report_email": None, "retrieved_email": "retrieved_email", "retrieved_date": "retrieved_date"}
    mock_retrieve_item.return_value = retrieved_mock_item
    
    response = client.put("/v1/items/retrieve/1", json = {"email": "retrieved_email"})
    assert response.status_code == 200
    assert response.json() == retrieved_mock_item

    response = client.put("/v1/items/retrieve/abc", json = {"email":"retrieved_email"})
    assert response.status_code == 400
    assert response.json() == invalid_id_message

    mock_retrieve_item.return_value = None
    response = client.put("/v1/items/retrieve/999", json = {"email":"retrieved_email"})
    assert response.status_code == 204

# CREATE NEW ITEM

@patch("api.main.crud.create_item")
def test_create_item(mock_create_item):
    mock_item = {"id" : 1, "description": "description", "tag": "tag", "image": "image", "state": "stored", "dropoffPoint_id": 1, "report_email": None, "retrieved_email": None, "retrieved_date": None}
    mock_create_item.return_value = mock_item
    
    response = client.post("/v1/items/create", json = {"description": "description", "tag": "tag", "image": "image", "dropoffPoint_id": 1})
    assert response.status_code == 201
    assert response.json() == mock_item

# REPORT NEW ITEM

@patch("api.main.crud.report_item")
def test_report_item(mock_report_item):
    mock_item = {"id" : 1, "description": "description", "tag": "tag", "image": "image", "state": "reported", "dropoffPoint_id": None, "report_email": "report_email", "retrieved_email": None, "retrieved_date": None}
    mock_report_item.return_value = mock_item
    
    response = client.post("/v1/items/report", json = {"description": "description", "tag": "tag", "image": "image", "report_email": "report_email"})
    assert response.status_code == 201
    assert response.json() == mock_item

# DELETE EXISTING ITEM

@patch("api.main.crud.delete_item")
def test_delete_item(mock_delete_item):
    mock_delete_item.return_value = "OK"
    
    response = client.delete("/v1/items/id/1")
    assert response.status_code == 200
    assert response.json() == {"message": "ITEM DELETED"}

    response = client.delete("/v1/items/id/abc")
    assert response.status_code == 400
    assert response.json() == invalid_id_message

    mock_delete_item.return_value = None
    response = client.delete("/v1/items/id/999")
    assert response.status_code == 204