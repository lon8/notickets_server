from app.main import app
from fastapi.testclient import TestClient
import pytest


client = TestClient(app)

def test_read_item():
    response = client.post("/get_cities/")
    assert response.status_code == 200
    assert response.json() == {"id": 1, "name": "Item 1"}