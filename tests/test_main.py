import requests

# Define the base URL for the FastAPI application
BASE_URL = "http://localhost:8000"                  #TODO MockItems

# Test GET request for all items                    #TODO MockItems
def test_get_all_items():
    response = requests.get(f"{BASE_URL}/items")
    assert response.status_code == 200

# Test POST request for creating an item            #TODO MockItems
def test_create_item_personnel():
    data = {
        "description": "description1",
        "image": "image1.jpg",
        "video": "video1.mp4",
        "tag": "tag1",
        "dropoffPoint_id": 1,
        "mail": None
    }
    response = requests.post(f"{BASE_URL}/items", json=data)
    assert response.status_code == 200
    assert response.json()["description"] == data["description"]
    assert response.json()["image"] == data["image"]
    assert response.json()["video"] == data["video"]
    assert response.json()["tag"] == data["tag"]
    assert response.json()["dropoffPoint_id"] == data["dropoffPoint_id"]
    assert response.json()["mail"] == data["mail"]

# def test_create_item_user():                      #TODO MockItems
#     data = {
#         "description": "description1",
#         "image": "image1.jpg",
#         "video": "video1.mp4",
#         "tag": "tag1",
#         "dropoffPoint_id": None,
#         "mail": "mail1"
#     }
#     response = requests.post(f"{BASE_URL}/items", json=data)
#     assert response.status_code == 200
#     assert response.json()["description"] == data["description"]
#     assert response.json()["image"] == data["image"]
#     assert response.json()["video"] == data["video"]
#     assert response.json()["tag"] == data["tag"]
#     assert response.json()["dropoffPoint_id"] == data["dropoffPoint_id"]
#     assert response.json()["mail"] == data["mail"]

# Run the tests
if __name__ == "__main__":
    test_get_all_items()
    test_create_item_personnel()
    # test_create_item_user()
