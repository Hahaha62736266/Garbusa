"""
Shared pytest fixtures.

The Flask app is imported with Supabase DISABLED so tests never touch the real
database — everything runs against the in-memory MOCK_DB.
"""
import os
import sys

import pytest

# Make the project root importable (app.py, controllers/, middleware/)
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

# Must be set BEFORE `import app` — load_dotenv() never overrides existing variables
os.environ["SUPABASE_URL"] = ""
os.environ["SECRET_KEY"] = "test-secret-key"
os.environ["DEMO_MODE"] = "false"
os.environ["ADMIN_EMAIL"] = "admin@test.local"
os.environ["ADMIN_PASSWORD"] = "admin-pass-123"

ADMIN_EMAIL = os.environ["ADMIN_EMAIL"]
ADMIN_PASSWORD = os.environ["ADMIN_PASSWORD"]


@pytest.fixture
def app_module():
    """The app module with a fresh in-memory database and seeded admin."""
    import app as app_module

    assert app_module.supabase is None, "Tests must never use the real Supabase project"
    for table in app_module.MOCK_DB.values():
        table.clear()
    app_module.seed_accounts()
    app_module.app.config["TESTING"] = True
    return app_module


@pytest.fixture
def client(app_module):
    """An anonymous (logged-out) test client."""
    return app_module.app.test_client()


@pytest.fixture
def make_client(app_module):
    """Factory: make_client('admin' | 'delivery' | 'customer') -> logged-in client."""
    counter = {"n": 0}

    def _make(role):
        c = app_module.app.test_client()
        if role == "admin":
            res = c.post("/api/login", json={"email": ADMIN_EMAIL, "password": ADMIN_PASSWORD})
        else:
            counter["n"] += 1
            res = c.post("/api/register", json={
                "email": f"{role}{counter['n']}@test.local",
                "password": "password123",
                "full_name": f"Test {role.title()} {counter['n']}",
                "role": role,
            })
        assert res.status_code in (200, 201), res.get_json()
        c.user = res.get_json()["user"]
        return c

    return _make


@pytest.fixture
def clean_controllers():
    """Reset the in-memory stores used by the controller layer (Task 3 lab code)."""
    from controllers import customer_controller, product_controller, order_controller, collection_controller

    for store in (customer_controller.customers_db, product_controller.products_db,
                  order_controller.orders_db, collection_controller.collections_db):
        store.clear()
