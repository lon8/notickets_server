import pytest
from main import app
from fastapi.testclient import TestClient

# Set up the TestClient for synchronous testing
client = TestClient(app)

# Use pytest-asyncio for asynchronous tests
@pytest.mark.asyncio
async def test_create_venue():
    payload = {
        "venue": "Test Venue"
    }
    response = await client.post("/create_venue/", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "OK"
    assert "venue_id" in data

@pytest.mark.asyncio
async def test_put_events():
    payload = {
        "name": "Test Event",
        "link": "http://example.com",
        "parser": "Test Parser",
        "date": "2024-01-01 00:00:00",
        "venue_id": 1,
        "image_links": ["http://example.com/image.jpg"]
    }
    response = await client.post("/put_event/", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Event added successfully"

@pytest.mark.asyncio
async def test_clear_events():
    payload = {
        "parser": "Test Parser"
    }
    response = await client.post("/clear_events/", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Events cleared successfully"

@pytest.mark.asyncio
async def test_get_city_events():
    payload = {
        "region": 36
    }
    response = await client.post("/get_city_events/", json=payload)
    assert response.status_code == 200
    events = response.json()
    assert isinstance(events, list)

@pytest.mark.asyncio
async def test_get_events_by_venue():
    payload = {
        "venue_id": 1
    }
    response = await client.post("/get_events_by_venue/", json=payload)
    assert response.status_code == 200
    events = response.json()
    assert isinstance(events, list)

@pytest.mark.asyncio
async def test_get_cities():
    response = await client.get("/get_cities/")
    assert response.status_code == 200
    cities = response.json()
    assert isinstance(cities, dict)

@pytest.mark.asyncio
async def test_get_venues():
    response = await client.get("/get_venues/")
    assert response.status_code == 200
    venues = response.json()
    assert isinstance(venues, dict)
