import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

@ pytest.fixture(autouse=True)
def run_around_tests():
    # reset state before each test
    app.state.contacts = []
    app.state.current_id = 1
    yield

# GET /contacts

def test_get_contacts_empty():
    response = client.get("/contacts")
    assert response.status_code == 200
    assert response.json() == []

def test_get_contacts_wrong_method():
    response = client.post("/contacts")
    assert response.status_code == 422

# GET /contacts/favorites

def test_get_favorites_empty():
    response = client.get("/contacts/favorites")
    assert response.status_code == 200
    assert response.json() == []

def test_get_favorites_wrong_method():
    response = client.delete("/contacts/favorites")
    assert response.status_code == 405

# GET /contacts/{id}

def test_get_contact_success():
    client.post("/contacts", json={"name": "Alice", "phone": "123"})
    response = client.get("/contacts/1")
    assert response.status_code == 200
    assert response.json()["name"] == "Alice"

def test_get_contact_not_found():
    response = client.get("/contacts/999")
    assert response.status_code == 404

# POST /contacts

def test_create_contact_success():
    response = client.post("/contacts", json={"name": "Bob", "phone": "456"})
    assert response.status_code == 201
    data = response.json()
    assert data["id"] == 1
    assert data["name"] == "Bob"

def test_create_contact_validation_error():
    response = client.post("/contacts", json={"phone": "456"})
    assert response.status_code == 422

# DELETE /contacts/{id}

def test_delete_contact_success():
    client.post("/contacts", json={"name": "Charlie", "phone": "789"})
    response = client.delete("/contacts/1")
    assert response.status_code == 200

def test_delete_contact_not_found():
    response = client.delete("/contacts/999")
    assert response.status_code == 404