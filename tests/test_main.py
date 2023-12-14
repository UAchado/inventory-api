from io import BytesIO
from fastapi.testclient import TestClient
from unittest.mock import patch
from api import main

## HELPER COMPONENTS

client = TestClient(main.app)

date_mock_element = "2023-01-01T00:00:00"
first_page = "?page=1&size=1"
invalid_id_message = {'detail' : 'INVALID ID FORMAT'}

urls = {
    "base": "/inventory/v1",
    "get_all_items": "/inventory/v1/items",
    "get_item_by_id": "/inventory/v1/items/id",
    "get_all_tags": "/inventory/v1/items/tags",
    "get_stored_items": "/inventory/v1/items/stored",
    "get_dropoff_point_items": "/inventory/v1/items/point",
    "get_dropoff_point_items_1": "/inventory/v1/items/point/1",
    "retrieve_item": "/inventory/v1/items/retrieve",
    "create_item": "/inventory/v1/items/create",
    "report_item": "/inventory/v1/items/report",
    "delete_item": "/inventory/v1/items/id",
    "get_image": "/inventory/v1/image/uuid"
}

## INTEGRATION TESTS

# BASE


def test_base():
    response = client.get(urls["base"])
    assert response.status_code == 200
    assert response.json() == {"response": "Hello World!"}

# GET ALL ITEMS

@patch("api.main.auth.verify_access")
@patch("api.main.crud.get_items")
def test_get_all_items(mock_get_items, mock_verify_access):
    mock_verify_access.return_value = {"user": "dummy_user"}
    mock_items = [
        {"id" : 1, "description": "description", "tag": "tag", "image": "image", "state": "stored", "dropoff_point_id": 1, "insertion_date": date_mock_element, "report_email": None, "retrieved_email": None, "retrieved_date": None},
        {"id" : 2, "description": "description", "tag": "tag", "image": "image", "state": "reported", "dropoff_point_id": None, "insertion_date": date_mock_element, "report_email": "report_email", "retrieved_email": None, "retrieved_date": None},
        {"id" : 3, "description": "description", "tag": "tag", "image": "image", "state": "retrieved", "dropoff_point_id": 1, "insertion_date": date_mock_element, "report_email": None, "retrieved_email": "retrieved_email", "retrieved_date": "retrieved_date"},
        {"id" : 4, "description": "description", "tag": "tag", "image": "image", "state": "archived", "dropoff_point_id": 1, "insertion_date": date_mock_element, "report_email": None, "retrieved_email": "retrieved_email", "retrieved_date": "retrieved_date"},
    ]

    mock_get_items.return_value = mock_items
    
    response = client.get(urls["get_all_items"])
    assert response.status_code == 200
    assert response.json()["items"] == mock_items
    
    response = client.get(urls["get_all_items"]+first_page)
    assert response.status_code == 200
    assert response.json()["items"] == [mock_items[0]]

# GET ITEM BY ID

@patch("api.main.crud.get_item_by_id")
def test_get_item_by_id(mock_get_item_by_id):
    mock_item = {"id" : 1, "description": "description", "tag": "tag", "image": "image", "state": "stored", "dropoff_point_id": 1, "insertion_date": date_mock_element, "report_email": None, "retrieved_email": None, "retrieved_date": None}
    mock_get_item_by_id.return_value = mock_item
    
    response = client.get(urls["get_item_by_id"] + "/1")
    assert response.status_code == 200
    assert response.json() == mock_item

    response = client.get(urls["get_item_by_id"] + "/abc")
    assert response.status_code == 400
    assert response.json() == invalid_id_message

    mock_get_item_by_id.return_value = None
    response = client.get(urls["get_item_by_id"] + "/999")
    assert response.status_code == 204

# GET ALL ITEM TAGS

def test_get_all_tags():
    response = client.get(urls["get_all_tags"])
    assert response.status_code == 200
    assert response.json() == ["Todos","Portáteis","Telemóveis","Tablets","Auscultadores/Fones","Carregadores","Pen drives","Câmaras","Livros","Cadernos","Material de escritório","Carteiras","Chaves","Cartão","Óculos","Joalharia","Casacos","Chapéus/Bonés","Cachecóis","Luvas","Mochilas","Equipamento desportivo","Garrafas de água","Guarda-chuvas","Instrumentos musicais","Material de arte","Bagagem","Produtos de maquilhagem","Artigos de higiene","Medicamentos"]

# GET STORED ITEMS

@patch("api.main.crud.get_stored_items")
def test_get_stored_items(mock_get_stored_items):
    mock_items = [
        {"id" : 1, "description": "description", "tag": "tag1", "image": "image", "state": "stored", "dropoff_point_id": 1, "insertion_date": date_mock_element, "report_email": None, "retrieved_email": None, "retrieved_date": None},
        {"id" : 2, "description": "description", "tag": "tag1", "image": "image", "state": "stored", "dropoff_point_id": 2, "insertion_date": date_mock_element, "report_email": None, "retrieved_email": None, "retrieved_date": None},
        {"id" : 3, "description": "description", "tag": "tag2", "image": "image", "state": "stored", "dropoff_point_id": 2, "insertion_date": date_mock_element, "report_email": None, "retrieved_email": None, "retrieved_date": None},
    ]

    mock_get_stored_items.return_value = mock_items
    response = client.post(urls["get_stored_items"], json = {"filter": {}})
    assert response.status_code == 200
    assert response.json()["items"] == mock_items
    
    response = client.post(urls["get_stored_items"]+first_page, json = {"filter": {}})
    assert response.status_code == 200
    assert response.json()["items"] == [mock_items[0]]

    mock_get_stored_items.return_value = [mock_items[0], mock_items[1]]
    response = client.post(urls["get_stored_items"], json = {"filter": {"tag":"tag1"}})
    assert response.status_code == 200
    assert response.json()["items"] == [mock_items[0], mock_items[1]]

    mock_get_stored_items.return_value = [mock_items[1], mock_items[2]]
    response = client.post(urls["get_stored_items"], json = {"filter": {"dropoff_point_id":2}})
    assert response.status_code == 200
    assert response.json()["items"] == [mock_items[1], mock_items[2]]

    mock_get_stored_items.return_value = [mock_items[2]]
    response = client.post(urls["get_stored_items"], json = {"filter": {"tag":"tag2", "dropoff_point_id": 2}})
    assert response.status_code == 200
    assert response.json()["items"] == [mock_items[2]]
    
    

# GET DROP-OFF POINT ITEMS

@patch("api.main.auth.verify_access")
@patch("api.main.crud.get_dropoff_point_items")
def test_get_dropoff_point_items(mock_get_dropoff_point_items, mock_verify_access):
    mock_verify_access.return_value = {"user": "dummy_user"}
    mock_items = [
        {"id" : 1, "description": "description", "tag": "tag1", "image": "image", "state": "stored", "dropoff_point_id": 2, "insertion_date": date_mock_element, "report_email": None, "retrieved_email": None, "retrieved_date": None},
        {"id" : 2, "description": "description", "tag": "tag1", "image": "image", "state": "reported", "dropoff_point_id": None, "insertion_date": date_mock_element, "report_email": "report_email", "retrieved_email": None, "retrieved_date": None},
        {"id" : 3, "description": "description", "tag": "tag2", "image": "image", "state": "retrieved", "dropoff_point_id": 2, "insertion_date": date_mock_element, "report_email": None, "retrieved_email": "retrieved_email", "retrieved_date": "retrieved_date"},
        {"id" : 4, "description": "description", "tag": "tag2", "image": "image", "state": "archived", "dropoff_point_id": 1, "insertion_date": date_mock_element, "report_email": None, "retrieved_email": "retrieved_email", "retrieved_date": "retrieved_date"},
    ]

    mock_get_dropoff_point_items.return_value = mock_items
    response = client.put(urls["get_dropoff_point_items_1"], json = {"filter": {}})
    assert response.status_code == 200
    assert response.json()["items"] == mock_items
    
    response = client.put(urls["get_dropoff_point_items_1"]+first_page, json = {"filter": {}})
    assert response.status_code == 200
    assert response.json()["items"] == [mock_items[0]]

    mock_get_dropoff_point_items.return_value = [mock_items[0], mock_items[1]]
    response = client.put(urls["get_dropoff_point_items_1"], json = {"filter": {"tag":"tag1"}})
    assert response.status_code == 200
    assert response.json()["items"] == [mock_items[0], mock_items[1]]

    mock_get_dropoff_point_items.return_value = [mock_items[0], mock_items[2]]
    response = client.put(urls["get_dropoff_point_items_1"], json = {"filter": {"dropoff_point_id":2}})
    assert response.status_code == 200
    assert response.json()["items"] == [mock_items[0], mock_items[2]]

    for index, state in enumerate(["stored", "reported", "retrieved", "archived"]):
        mock_get_dropoff_point_items.return_value = [mock_items[index]]
        response = client.put(urls["get_dropoff_point_items_1"], json = {"filter": {"state":state}})
        assert response.status_code == 200
        assert response.json()["items"] == [mock_items[index]]

    mock_get_dropoff_point_items.return_value = [mock_items[2]]
    response = client.put(urls["get_dropoff_point_items_1"], json = {"filter": {"tag": "tag2", "state": "retrieved", "dropoff_point_id": 2}})
    assert response.status_code == 200
    assert response.json()["items"] == [mock_items[2]]

    response = client.put(urls["get_dropoff_point_items"] + "/abc", json =  {"filter": {}})
    assert response.status_code == 400
    assert response.json() == invalid_id_message

# RETRIEVE ITEM

@patch("api.main.auth.verify_access")
@patch("api.main.crud.retrieve_item")
def test_retrieve_item(mock_retrieve_item, mock_verify_access):
    mock_verify_access.return_value = {"user": "dummy_user"}
    
    retrieved_mock_item = {"id" : 1, "description": "description", "tag": "tag", "image": "image", "state": "retrieved", "dropoff_point_id": 1, "insertion_date": date_mock_element, "report_email": None, "retrieved_email": "retrieved_email", "retrieved_date": "retrieved_date"}
    mock_retrieve_item.return_value = retrieved_mock_item
    
    response = client.put(urls["retrieve_item"] + "/1", json = {"email": "retrieved_email"})
    assert response.status_code == 200
    assert response.json() == retrieved_mock_item

    response = client.put(urls["retrieve_item"] + "/abc", json = {"email":"retrieved_email"})
    assert response.status_code == 400
    assert response.json() == invalid_id_message

    mock_retrieve_item.return_value = None
    response = client.put(urls["retrieve_item"] + "/999", json = {"email":"retrieved_email"})
    assert response.status_code == 204

# CREATE NEW ITEM

@patch("api.main.auth.verify_access")
@patch("api.main.crud.create_item")
def test_create_item(mock_create_item, mock_verify_access):
    mock_verify_access.return_value = {"user": "dummy_user"}
    mock_item = {"id" : 1, "description": "description", "tag": "tag", "image": None, "state": "stored", "dropoff_point_id": 1, "insertion_date": date_mock_element, "report_email": None, "retrieved_email": None, "retrieved_date": None}
    mock_create_item.return_value = mock_item
    
    fake_file = BytesIO(b"fake image content")
    fake_file.name = "test.jpg"
    
    data = {
        "description": (None, "description"),
        "tag": (None, "tag"),
        "image": (fake_file.name, fake_file, "image/jpeg"),
        "dropoff_point_id": (None, "1"),
    }
    
    response = client.post(urls["create_item"], files = data)
    assert response.status_code == 201
    assert response.json() == mock_item
    
    fake_file.name = "test.docx"
    
    data = {
        "description": (None, "description"),
        "tag": (None, "tag"),
        "image": (fake_file.name, fake_file, "image/docx"),
        "dropoff_point_id": (None, "1"),
    }
    
    response = client.post(urls["create_item"], files = data)
    assert response.status_code == 201
    assert response.json() == mock_item
    

# REPORT NEW ITEM

@patch("api.main.crud.report_item")
def test_report_item(mock_report_item):
    mock_item = {"id" : 1, "description": "description", "tag": "tag", "image": None, "state": "reported", "dropoff_point_id": None, "insertion_date": date_mock_element, "report_email": "report_email", "retrieved_email": None, "retrieved_date": None}
    mock_report_item.return_value = mock_item
    
    fake_file = BytesIO(b"fake image content")
    fake_file.name = "test.jpg"
    
    data = {
        "description": (None, "description"),
        "tag": (None, "tag"),
        "image": (fake_file.name, fake_file, "image/jpeg"),
        "report_email": (None, "report_email"),
    }
    
    response = client.post(urls["report_item"], files = data)
    assert response.status_code == 201
    assert response.json() == mock_item
    
    fake_file.name = "test.docx"
    
    data = {
        "description": (None, "description"),
        "tag": (None, "tag"),
        "image": (fake_file.name, fake_file, "image/docx"),
        "report_email": (None, "report_email"),
    }
    
    response = client.post(urls["report_item"], files = data)
    assert response.status_code == 201
    assert response.json() == mock_item

# DELETE EXISTING ITEM

@patch("api.main.auth.verify_access")
@patch("api.main.crud.delete_item")
def test_delete_item(mock_delete_item, mock_verify_access):
    mock_verify_access.return_value = {"user": "dummy_user"}
    mock_delete_item.return_value = "OK"
    
    response = client.delete(urls["delete_item"] + "/1")
    assert response.status_code == 200
    assert response.json() == {"message": "ITEM DELETED"}

    response = client.delete(urls["delete_item"] + "/abc")
    assert response.status_code == 400
    assert response.json() == invalid_id_message

    mock_delete_item.return_value = None
    response = client.delete(urls["delete_item"] + "/999")
    assert response.status_code == 204
    
# GET IMAGE FROM S3 BUCKET

@patch("api.main.crud.get_image_from_s3")
def test_get_image_from_s3(mock_get_image_from_s3):
    mock_get_image_from_s3.return_value = {"body": "StreamingResponse_template"}
    
    response = client.get(urls["get_image"])
    assert response.status_code == 200
    assert response.json() == {"body": "StreamingResponse_template"}