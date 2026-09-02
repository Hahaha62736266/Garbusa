import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

class MockRequest:
    def __init__(self, body=None, params=None, auth_user_id=None):
        self.body = body or {}
        self.params = params or {}
        self.validatedBody = None
        self.auth = {"user_id": auth_user_id} if auth_user_id else None

from middleware.validation import (
    validateCustomerCreate, validateProductCreate,
    validateOrderCreate, validateCollectionCreate,
    authorizeDeleteOrder
)
from controllers.customer_controller import createCustomer
from controllers.product_controller import createProduct
from controllers.order_controller import createOrder, deleteOrder
from controllers.collection_controller import createCollection

def test(name, validation_fn, controller_fn, body, expected_status, params=None, auth_user_id=None):
    print(f"\n{'─'*60}")
    print(f"🧪 {name}")
    req = MockRequest(body=body, params=params or {}, auth_user_id=auth_user_id)
    err = validation_fn(req)
    result = err if err else controller_fn(req)
    actual = result.get("status")
    ok = "✅ PASS" if actual == expected_status else f"❌ FAIL (got {actual}, expected {expected_status})"
    print(f"📊 {ok}")
    return actual == expected_status

if __name__ == "__main__":
    passed = total = 0

    # CUSTOMER TESTS
    total +=1; passed += test("Customer — Happy Path → 201", validateCustomerCreate, createCustomer,
        {"customer_id":"C001","full_name":"Juan Dela Cruz","contact_number":"0917-123-4567","address":"CDO, PH","container_owned":5}, 201)
    total +=1; passed += test("Customer — Missing name → 422", validateCustomerCreate, createCustomer,
        {"customer_id":"C002","contact_number":"0917-111-2222","address":"CDO","container_owned":2}, 422)
    total +=1; passed += test("Customer — Bad ID format → 422", validateCustomerCreate, createCustomer,
        {"customer_id":"CUS999","full_name":"Name","contact_number":"0917-333-4444","address":"Addr","container_owned":0}, 422)

    # PRODUCT TESTS
    total +=1; passed += test("Product — Happy Path → 201", validateProductCreate, createProduct,
        {"product_id":"P001","product_name":"5Gal Water","price_per_unit":85.50,"stock_available":100}, 201)
    total +=1; passed += test("Product — Negative price → 422", validateProductCreate, createProduct,
        {"product_id":"P002","product_name":"Bad Item","price_per_unit":-10,"stock_available":50}, 422)
    total +=1; passed += test("Product — Zero stock → 201", validateProductCreate, createProduct,
        {"product_id":"P003","product_name":"Out of Stock","price_per_unit":75,"stock_available":0}, 201)

    # ORDER TESTS
    total +=1; passed += test("Order — Happy Path → 201", validateOrderCreate, createOrder,
        {"order_id":"O001","customer_id":"C001","product_id":"P001","quantity":3,"status":"Pending"}, 201)
    total +=1; passed += test("Order — Negative qty → 422", validateOrderCreate, createOrder,
        {"order_id":"O002","customer_id":"C001","product_id":"P001","quantity":-5,"status":"Pending"}, 422)
    total +=1; passed += test("Order — Invalid status → 422", validateOrderCreate, createOrder,
        {"order_id":"O003","customer_id":"C001","product_id":"P001","quantity":2,"status":"Cancelled"}, 422)

    # COLLECTION TESTS
    total +=1; passed += test("Collection — Happy Path → 201", validateCollectionCreate, createCollection,
        {"collection_id":"CL001","customer_id":"C001","order_id":"O001","empty_jugs_returned":2,"filled_jugs_released":5,"container_balance":3,"collected_by":"Team A"}, 201)
    total +=1; passed += test("Collection — Negative balance → 422", validateCollectionCreate, createCollection,
        {"collection_id":"CL002","customer_id":"C001","order_id":"O001","empty_jugs_returned":5,"filled_jugs_released":3,"container_balance":-2,"collected_by":"Team B"}, 422)
    total +=1; passed += test("Collection — Zero returns → 201", validateCollectionCreate, createCollection,
        {"collection_id":"CL003","customer_id":"C001","order_id":"O001","empty_jugs_returned":0,"filled_jugs_released":10,"container_balance":10,"collected_by":"Team C"}, 201)

    # AUTH TESTS
    def auth_test(name, owner_id, requester_id, expect_status):
        print(f"\n{'─'*60}\n🧪 {name}")
        MockRequest({"order_id":"O001","customer_id":owner_id,"product_id":"P001","quantity":2,"status":"Pending"})
        from models.order_model import Order
        Order.save({"order_id":"O001","customer_id":owner_id,"product_id":"P001","quantity":2,"status":"Pending"})
        req = MockRequest(params={"order_id":"O001"}, auth_user_id=requester_id)
        err = authorizeDeleteOrder(req)
        res = err if err else deleteOrder(req)
        ok = "✅ PASS" if res.get("status") == expect_status else f"❌ FAIL"
        print(f"📊 {ok}")
        return res.get("status") == expect_status

    total +=1; passed += auth_test("Delete — Wrong User → 403", "C001", "C999", 403)
    total +=1; passed += auth_test("Delete — Owner → 200", "C001", "C001", 200)

    print(f"\n{'='*60}\n📊 {passed}/{total} PASSED")
    print("✅ ALL GREEN ✅" if passed==total else f"⚠️ {total-passed} FAILED")
