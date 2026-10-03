"""
API tests for app.py — run against the in-memory store (no Supabase).
Covers authentication, role guards, data scoping, ID generation and input validation.
"""
from conftest import ADMIN_EMAIL, ADMIN_PASSWORD


# ==================================================
# AUTHENTICATION
# ==================================================
def test_health_is_public(client):
    res = client.get("/api/health")
    assert res.status_code == 200
    assert res.get_json()["supabase_connected"] is False


def test_passwords_are_hashed(app_module):
    admin = app_module.find_user(ADMIN_EMAIL)
    assert admin["password_hash"] != ADMIN_PASSWORD
    assert "password" not in admin


def test_login_success_sets_session(client):
    res = client.post("/api/login", json={"email": ADMIN_EMAIL, "password": ADMIN_PASSWORD})
    assert res.status_code == 200
    assert res.get_json()["user"]["role"] == "admin"
    assert "password_hash" not in res.get_json()["user"]
    assert client.get("/api/me").get_json()["user"]["email"] == ADMIN_EMAIL


def test_login_wrong_password(client):
    res = client.post("/api/login", json={"email": ADMIN_EMAIL, "password": "nope"})
    assert res.status_code == 401


def test_login_handles_garbage_body(client):
    assert client.post("/api/login", data="not json").status_code == 401


def test_logout_clears_session(make_client):
    c = make_client("admin")
    assert c.post("/api/logout").status_code == 200
    assert c.get("/api/me").status_code == 401


def test_register_customer_creates_linked_customer_record(client, app_module):
    res = client.post("/api/register", json={
        "email": "Maria@Example.com", "password": "password123", "full_name": "Maria Santos",
        "role": "customer", "contact_number": "0917-123-4567", "address": "Brgy. 25, CdeO",
    })
    assert res.status_code == 201
    user = res.get_json()["user"]
    assert user["email"] == "maria@example.com"
    assert user["customer_id"] == "C001"
    assert app_module.MOCK_DB["customers"][0]["full_name"] == "Maria Santos"


def test_register_admin_is_forbidden(client):
    res = client.post("/api/register", json={
        "email": "hacker@test.local", "password": "password123", "full_name": "Hacker", "role": "admin",
    })
    assert res.status_code == 403


def test_register_unknown_role_rejected(client):
    res = client.post("/api/register", json={
        "email": "x@test.local", "password": "password123", "full_name": "X", "role": "superuser",
    })
    assert res.status_code == 422


def test_register_short_password_rejected(client):
    res = client.post("/api/register", json={
        "email": "short@test.local", "password": "abc", "full_name": "Short", "role": "customer",
    })
    assert res.status_code == 422


def test_register_invalid_email_rejected(client):
    res = client.post("/api/register", json={
        "email": "not-an-email", "password": "password123", "full_name": "Bad", "role": "customer",
    })
    assert res.status_code == 422


def test_register_duplicate_email_rejected(client):
    res = client.post("/api/register", json={
        "email": ADMIN_EMAIL, "password": "password123", "full_name": "Dup", "role": "customer",
    })
    assert res.status_code == 409


# ==================================================
# PAGE ACCESS
# ==================================================
def test_dashboard_redirects_when_logged_out(client):
    res = client.get("/")
    assert res.status_code == 302
    assert res.headers["Location"].endswith("/login")


def test_dashboard_loads_when_logged_in(make_client):
    assert make_client("admin").get("/").status_code == 200


def test_login_page_hides_demo_presets_when_demo_mode_off(client):
    html = client.get("/login").get_data(as_text=True)
    assert "Quick Demo Role Login" not in html


# ==================================================
# ROLE GUARDS
# ==================================================
def test_api_requires_login(client):
    for path in ("/api/customers", "/api/products", "/api/orders", "/api/collections"):
        assert client.get(path).status_code == 401, path


def test_only_admin_can_create_products(make_client):
    body = {"product_name": "5-Gal Purified", "price_per_unit": 35, "stock_available": 120}
    assert make_client("customer").post("/api/products", json=body).status_code == 403
    assert make_client("delivery").post("/api/products", json=body).status_code == 403
    assert make_client("admin").post("/api/products", json=body).status_code == 201


def test_only_admin_can_create_customers(make_client):
    body = {"full_name": "Juan Dela Cruz"}
    assert make_client("delivery").post("/api/customers", json=body).status_code == 403
    assert make_client("admin").post("/api/customers", json=body).status_code == 201


def test_delivery_cannot_place_orders(make_client):
    res = make_client("delivery").post("/api/orders", json={"customer_id": "C001", "product_id": "P001", "quantity": 1})
    assert res.status_code == 403


def test_customer_orders_are_forced_to_own_account(make_client):
    customer = make_client("customer")
    res = customer.post("/api/orders", json={"product_id": "P001", "quantity": 2})
    assert res.status_code == 201
    assert res.get_json()["data"]["customer_id"] == customer.user["customer_id"]


def test_customer_cannot_order_for_someone_else(make_client):
    res = make_client("customer").post("/api/orders", json={"customer_id": "C999", "product_id": "P001", "quantity": 1})
    assert res.status_code == 403


def test_customers_only_see_their_own_records(make_client):
    alice = make_client("customer")
    bob = make_client("customer")
    alice.post("/api/orders", json={"product_id": "P001", "quantity": 1})
    bob.post("/api/orders", json={"product_id": "P001", "quantity": 1})

    alice_orders = alice.get("/api/orders").get_json()["data"]
    assert len(alice_orders) == 1
    assert alice_orders[0]["customer_id"] == alice.user["customer_id"]
    assert len(alice.get("/api/customers").get_json()["data"]) == 1
    assert len(make_client("admin").get("/api/orders").get_json()["data"]) == 2


def test_customer_cannot_update_order_status(make_client):
    customer = make_client("customer")
    order_id = customer.post("/api/orders", json={"product_id": "P001", "quantity": 1}).get_json()["data"]["order_id"]
    assert customer.patch(f"/api/orders/{order_id}", json={"status": "Delivered"}).status_code == 403


# ==================================================
# ORDERS — status rules
# ==================================================
def test_delivery_can_mark_order_delivered(make_client):
    order_id = make_client("customer").post("/api/orders", json={"product_id": "P001", "quantity": 1}).get_json()["data"]["order_id"]
    res = make_client("delivery").patch(f"/api/orders/{order_id}", json={"status": "Delivered"})
    assert res.status_code == 200


def test_order_status_cancelled_rejected_consistently(make_client):
    """App and validation middleware agree: only Pending / Delivered."""
    order_id = make_client("customer").post("/api/orders", json={"product_id": "P001", "quantity": 1}).get_json()["data"]["order_id"]
    res = make_client("admin").patch(f"/api/orders/{order_id}", json={"status": "Cancelled"})
    assert res.status_code == 422


def test_patch_unknown_order_returns_404(make_client):
    assert make_client("admin").patch("/api/orders/O999", json={"status": "Delivered"}).status_code == 404


def test_patch_without_body_returns_422(make_client):
    assert make_client("admin").patch("/api/orders/O001").status_code == 422


# ==================================================
# INPUT VALIDATION
# ==================================================
def test_order_quantity_must_be_whole_number(make_client):
    customer = make_client("customer")
    for bad in ("abc", 1.5, 0, -3, None):
        res = customer.post("/api/orders", json={"product_id": "P001", "quantity": bad})
        assert res.status_code == 422, bad


def test_product_price_must_be_numeric(make_client):
    admin = make_client("admin")
    assert admin.post("/api/products", json={"product_name": "X", "price_per_unit": "cheap"}).status_code == 422
    assert admin.post("/api/products", json={"product_name": "X", "price_per_unit": -1}).status_code == 422


def test_collection_negative_balance_rejected(make_client):
    res = make_client("delivery").post("/api/collections", json={
        "customer_id": "C001", "empty_jugs_returned": 5, "filled_jugs_released": 3,
    })
    assert res.status_code == 422


def test_collection_defaults_collected_by_to_current_user(make_client):
    delivery = make_client("delivery")
    res = delivery.post("/api/collections", json={"customer_id": "C001", "filled_jugs_released": 2})
    assert res.status_code == 201
    assert res.get_json()["data"]["collected_by"] == delivery.user["name"]


# ==================================================
# ID GENERATION
# ==================================================
def test_next_id_uses_highest_existing_number(app_module):
    app_module.MOCK_DB["customers"].extend([{"customer_id": "C001"}, {"customer_id": "C005"}])
    # Old count-based logic would have returned C003 here (a future duplicate of C003)
    assert app_module.get_next_id("customers", "C") == "C006"


def test_next_id_after_delete_never_reuses_ids(app_module):
    app_module.MOCK_DB["orders"].extend([{"order_id": "O001"}, {"order_id": "O002"}, {"order_id": "O003"}])
    app_module.MOCK_DB["orders"].pop(0)  # delete O001
    # Old count-based logic would return O003 -> duplicate!
    assert app_module.get_next_id("orders", "O") == "O004"
