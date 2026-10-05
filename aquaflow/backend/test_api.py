import pytest
from app import app as flask_app

@pytest.fixture
def app():
    flask_app.config.update({"TESTING": True})
    yield flask_app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def runner(app):
    return app.test_cli_runner()

# --- Actual tests ---

def test_endpoint_customers_get(client):
    """GET /api/customers returns 200 and list"""
    resp = client.get("/api/customers")
    assert resp.status_code == 200
    assert isinstance(resp.get_json(), list)

def test_endpoint_orders_empty_payload(client):
    """POST /api/orders with empty body returns 400"""
    resp = client.post("/api/orders", json={})
    assert resp.status_code == 400
    data = resp.get_json()
    assert "error" in data

def test_endpoint_orders_missing_fields(client):
    """POST /api/orders missing required fields returns 400"""
    resp = client.post("/api/orders", json={"note": "test"})
    assert resp.status_code == 400
    assert "error" in resp.get_json()

def test_endpoint_orders_valid_payload(client):
    """POST /api/orders with valid data returns 201"""
    payload = {
        "customer_id": "CUST-001",
        "product_id": "P002",
        "quantity": 2
    }
    resp = client.post("/api/orders", json=payload)
    assert resp.status_code == 201
    data = resp.get_json()
    assert "id" in data
    assert data["status"] == "Pending"