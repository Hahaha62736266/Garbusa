"""
Task 3 — Validation → Controller pipeline (pytest version of test_pipeline.py).
Arrange / Act / Assert, same 14 cases as the original script.
"""
import pytest

from middleware.validation import (
    validateCustomerCreate, validateProductCreate,
    validateOrderCreate, validateCollectionCreate,
    authorizeDeleteOrder,
)
from controllers.customer_controller import createCustomer
from controllers.product_controller import createProduct
from controllers.order_controller import createOrder, deleteOrder
from controllers.collection_controller import createCollection


class MockRequest:
    """Fake request — exactly what the framework passes"""
    def __init__(self, body=None, params=None, auth_user_id=None):
        self.body = body or {}
        self.params = params or {}
        self.validatedBody = None  # set by validation middleware
        self.auth = {"user_id": auth_user_id} if auth_user_id else None


def run_pipeline(validation_fn, controller_fn, body):
    req = MockRequest(body=body)                      # ARRANGE
    return validation_fn(req) or controller_fn(req)   # ACT


CASES = [
    # --- Customers ---
    ("customer happy path", validateCustomerCreate, createCustomer,
     {"customer_id": "C001", "full_name": "Maria Santos", "contact_number": "0917-123-4567",
      "address": "Cagayan de Oro City", "container_owned": 5}, 201),
    ("customer missing full_name", validateCustomerCreate, createCustomer,
     {"customer_id": "C002", "contact_number": "0917-111-2222", "address": "Misamis Oriental",
      "container_owned": 2}, 422),
    ("customer invalid id format", validateCustomerCreate, createCustomer,
     {"customer_id": "CUS999", "full_name": "Invalid ID User", "contact_number": "0917-333-4444",
      "address": "CDO City", "container_owned": 0}, 422),
    # --- Products ---
    ("product happy path", validateProductCreate, createProduct,
     {"product_id": "P001", "product_name": "5-Gallon Purified Water", "price_per_unit": 85.50,
      "stock_available": 100}, 201),
    ("product negative price", validateProductCreate, createProduct,
     {"product_id": "P002", "product_name": "Invalid Product", "price_per_unit": -10.00,
      "stock_available": 50}, 422),
    ("product zero stock is valid", validateProductCreate, createProduct,
     {"product_id": "P003", "product_name": "Out-of-Stock Item", "price_per_unit": 75.00,
      "stock_available": 0}, 201),
    # --- Orders ---
    ("order happy path", validateOrderCreate, createOrder,
     {"order_id": "O001", "customer_id": "C001", "product_id": "P001", "quantity": 3,
      "status": "Pending"}, 201),
    ("order negative quantity", validateOrderCreate, createOrder,
     {"order_id": "O002", "customer_id": "C001", "product_id": "P001", "quantity": -5,
      "status": "Pending"}, 422),
    ("order invalid status", validateOrderCreate, createOrder,
     {"order_id": "O003", "customer_id": "C001", "product_id": "P001", "quantity": 2,
      "status": "Cancelled"}, 422),
    # --- Collections ---
    ("collection happy path", validateCollectionCreate, createCollection,
     {"collection_id": "CL001", "customer_id": "C001", "order_id": "O001", "empty_jugs_returned": 2,
      "filled_jugs_released": 5, "container_balance": 3, "collected_by": "Delivery Team A"}, 201),
    ("collection negative balance", validateCollectionCreate, createCollection,
     {"collection_id": "CL002", "customer_id": "C001", "order_id": "O001", "empty_jugs_returned": 5,
      "filled_jugs_released": 3, "container_balance": -2, "collected_by": "Delivery Team B"}, 422),
    ("collection zero returns is valid", validateCollectionCreate, createCollection,
     {"collection_id": "CL003", "customer_id": "C001", "order_id": "O001", "empty_jugs_returned": 0,
      "filled_jugs_released": 10, "container_balance": 10, "collected_by": "Delivery Team C"}, 201),
]


@pytest.mark.usefixtures("clean_controllers")
@pytest.mark.parametrize("name, validation_fn, controller_fn, body, expected", CASES,
                         ids=[c[0] for c in CASES])
def test_validation_pipeline(name, validation_fn, controller_fn, body, expected):
    result = run_pipeline(validation_fn, controller_fn, body)
    assert result.get("status") == expected, result   # ASSERT


@pytest.mark.usefixtures("clean_controllers")
@pytest.mark.parametrize("requester, expected", [("C999", 403), ("C001", 200)],
                         ids=["wrong user deletes -> 403", "owner deletes -> 200"])
def test_delete_order_authorization(requester, expected):
    # ARRANGE — an order owned by C001
    create_req = MockRequest({"order_id": "O001", "customer_id": "C001", "product_id": "P001",
                              "quantity": 2, "status": "Pending"})
    assert validateOrderCreate(create_req) is None
    createOrder(create_req)

    # ACT
    req = MockRequest(params={"order_id": "O001"}, auth_user_id=requester)
    result = authorizeDeleteOrder(req) or deleteOrder(req)

    # ASSERT
    assert result.get("status") == expected, result
