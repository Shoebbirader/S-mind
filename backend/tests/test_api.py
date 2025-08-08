from fastapi.testclient import TestClient
import sys
import os

# Add the backend directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from api.main import app
from utils.state_manager import model_data


client = TestClient(app)


def setup_function():
    """Clear model data before each test."""
    client.post("/clear/")


def test_create_and_get_node():
    """Test creating a node and then retrieving it."""
    # Create a node
    response = client.post("/nodes/", json={"id": 1, "coordinates": [0, 0, 0]})
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert tuple(data["coordinates"]) == (0, 0, 0)

    # Get the node back
    response = client.get("/nodes/1")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert tuple(data["coordinates"]) == (0, 0, 0)

    # Get all nodes
    response = client.get("/nodes/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["id"] == 1

def test_create_node_already_exists():
    """Test creating a node that already exists."""
    client.post("/nodes/", json={"id": 1, "coordinates": [0, 0, 0]})
    response = client.post("/nodes/", json={"id": 1, "coordinates": [1, 1, 1]})
    assert response.status_code == 400
    assert "already exists" in response.json()["detail"]

def test_get_node_not_found():
    """Test getting a node that does not exist."""
    response = client.get("/nodes/999")
    assert response.status_code == 404
