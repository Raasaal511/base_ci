import pytest
from fastapi.testclient import TestClient

from app.main import app, items


@pytest.fixture(autouse=True)
def clear_items():
    items.clear()
    yield
    items.clear()


client = TestClient(app)


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello, World!"}


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_create_item():
    response = client.post("/items/1", json={"name": "Book", "price": 9.99})
    assert response.status_code == 201
    assert response.json() == {"name": "Book", "price": 9.99}


def test_create_duplicate_item():
    client.post("/items/1", json={"name": "Book", "price": 9.99})
    response = client.post("/items/1", json={"name": "Pen", "price": 1.5})
    assert response.status_code == 409


def test_read_item():
    client.post("/items/1", json={"name": "Book", "price": 9.99})
    response = client.get("/items/1")
    assert response.status_code == 200
    assert response.json() == {"name": "Book", "price": 9.99}


def test_read_missing_item():
    response = client.get("/items/999")
    assert response.status_code == 404


def test_create_item_validation_error():
    response = client.post("/items/1", json={"name": "Book"})
    assert response.status_code == 422
