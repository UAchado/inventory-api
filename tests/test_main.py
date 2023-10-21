import requests

# Define the base URL for the FastAPI application
BASE_URL = "http://localhost:8000"

# Test GET request for all items
def test_get_all_items():
    response = requests.get(f"{BASE_URL}/items")
    assert response.status_code == 200

# Test POST request for creating an item
def test_create_item():
    data = {
        "description": "description1",
        "image": "image1.jpg",
        "video": "video1.mp4",
        "tag": "tag1",
        "dropoffPoint_id": 1
    }
    response = requests.post(f"{BASE_URL}/items", json=data)
    assert response.status_code == 200
    assert response.json()["description"] == data["description"]

# Run the tests
if __name__ == "__main__":
    test_get_all_items()
    test_create_item()
