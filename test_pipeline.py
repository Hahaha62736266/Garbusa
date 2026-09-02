import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# ==========================================================
# TASK 3 — Automated Tests: Arrange / Act / Assert
# ==========================================================

class MockRequest:
    """Fake request — exactly what your framework passes"""
    def __init__(self, body=None, params=None, auth_user_id=None):
        self.body = body or {}
        self.params = params or {}
        self.validatedBody = None  # set by validation middleware
        self.auth = {"user_id": auth_user_id} if auth_user_id else None


# ─── Import layers ───
from middleware.validation import (
    validateCustomerCreate, validateProductCreate,
    validateOrderCreate, validateCollectionCreate,
    authorizeDeleteOrder
)
from controllers.customer_controller import createCustomer
from controllers.product_controller import createProduct
from controllers.order_controller import createOrder, deleteOrder
from controllers.collection_controller import createCollection


# ─── TEST RUNNER ───
def run_test(test_name, validation_fn, controller_fn, request_body, expected_status, params=None, auth_user_id=None):
    """ARRANGE → ACT → ASSERT"""
    print(f"\n{'─'*60}")
    print(f"🧪 {test_name}")
    print(f"{'─'*60}")

    # ARRANGE
    req = MockRequest(body=request_body, params=params or {}, auth_user_id=auth_user_id)

    # ACT
    validation_error = validation_fn(req)
    if validation_error:
        result = validation_error  # middleware rejected it
    else:
        result = controller_fn(req)  # passed validation → call controller

    # ASSERT
    actual_status = result.get("status")
    passed = actual_status == expected_status
    status_icon = "✅ PASS" if passed else f"❌ FAIL (got {actual_status}, expected {expected_status})"
    print(f"📊 Result: {status_icon}")
    print(f"📦 Response: {result}")
    return passed


# ==========================================================
# 🚀 ALL TESTS
# ==========================================================
if __name__ == "__main__":
    print("\n" + "🎯"*15 + "  TASK 3 — FULL TEST SUITE  " + "🎯"*15)
    passed = 0
    total = 0

    # ═══════════════════════════════════════════════════════
    # 🧾 CUSTOMER CONTROLLER
    # ═══════════════════════════════════════════════════════
    print("\n" + "■"*55)
    print(" 🧾 CUSTOMER TESTS")
    print("■"*55)

    total += 1
    if run_test(
        "Happy Path: Valid customer → returns 201 Created",
        validateCustomerCreate, createCustomer,
        {"customer_id":"C001","full_name":"Maria Santos","contact_number":"0917-123-4567","address":"Cagayan de Oro City","container_owned":5},
        expected_status=201
    ): passed += 1

    total += 1
    if run_test(
        "Validation Fail: Missing full_name → returns 422",
        validateCustomerCreate, createCustomer,
        {"customer_id":"C002","contact_number":"0917-111-2222","address":"Misamis Oriental","container_owned":2},
        expected_status=422
    ): passed += 1

    total += 1
    if run_test(
        "Edge Case: Invalid ID format → returns 422",
        validateCustomerCreate, createCustomer,
        {"customer_id":"CUS999","full_name":"Invalid ID User","contact_number":"0917-333-4444","address":"CDO City","container_owned":0},
        expected_status=422
    ): passed += 1

    # ═══════════════════════════════════════════════════════
    # 🧾 PRODUCT CONTROLLER
    # ═══════════════════════════════════════════════════════
    print("\n" + "■"*55)
    print(" 🧾 PRODUCT TESTS")
    print("■"*55)

    total += 1
    if run_test(
        "Happy Path: Valid product → returns 201 Created",
        validateProductCreate, createProduct,
        {"product_id":"P001","product_name":"5-Gallon Purified Water","price_per_unit":85.50,"stock_available":100},
        expected_status=201
    ): passed += 1

    total += 1
    if run_test(
        "Validation Fail: Negative price → returns 422",
        validateProductCreate, createProduct,
        {"product_id":"P002","product_name":"Invalid Product","price_per_unit":-10.00,"stock_available":50},
        expected_status=422
    ): passed += 1

    total += 1
    if run_test(
        "Edge Case: Zero stock → still valid → returns 201",
        validateProductCreate, createProduct,
        {"product_id":"P003","product_name":"Out-of-Stock Item","price_per_unit":75.00,"stock_available":0},
        expected_status=201
    ): passed += 1

    # ═══════════════════════════════════════════════════════
    # 🧾 ORDER CONTROLLER
    # ═══════════════════════════════════════════════════════
    print("\n" + "■"*55)
    print(" 🧾 ORDER TESTS")
    print("■"*55)

    total += 1
    if run_test(
        "Happy Path: Valid order → returns 201 Created",
        validateOrderCreate, createOrder,
        {"order_id":"O001","customer_id":"C001","product_id":"P001","quantity":3,"status":"Pending"},
        expected_status=201
    ): passed += 1

    total += 1
    if run_test(
        "Validation Fail: Negative quantity → returns 422",
        validateOrderCreate, createOrder,
        {"order_id":"O002","customer_id":"C001","product_id":"P001","quantity":-5,"status":"Pending"},
        expected_status=422
    ): passed += 1

    total += 1
    if run_test(
        "Edge Case: Invalid status value → returns 422",
        validateOrderCreate, createOrder,
        {"order_id":"O003","customer_id":"C001","product_id":"P001","quantity":2,"status":"Cancelled"},
        expected_status=422
    ): passed += 1

    # ═══════════════════════════════════════════════════════
    # 🧾 COLLECTION CONTROLLER
    # ═══════════════════════════════════════════════════════
    print("\n" + "■"*55)
    print(" 🧾 COLLECTION TESTS")
    print("■"*55)

    total += 1
    if run_test(
        "Happy Path: Valid collection → returns 201 Created",
        validateCollectionCreate, createCollection,
        {"collection_id":"CL001","customer_id":"C001","order_id":"O001","empty_jugs_returned":2,"filled_jugs_released":5,"container_balance":3,"collected_by":"Delivery Team A"},
        expected_status=201
    ): passed += 1

    total += 1
    if run_test(
        "Validation Fail: Negative balance → returns 422",
        validateCollectionCreate, createCollection,
        {"collection_id":"CL002","customer_id":"C001","order_id":"O001","empty_jugs_returned":5,"filled_jugs_released":3,"container_balance":-2,"collected_by":"Delivery Team B"},
        expected_status=422
    ): passed += 1

    total += 1
    if run_test(
        "Edge Case: Zero returns → still valid → returns 201",
        validateCollectionCreate, createCollection,
        {"collection_id":"CL003","customer_id":"C001","order_id":"O001","empty_jugs_returned":0,"filled_jugs_released":10,"container_balance":10,"collected_by":"Delivery Team C"},
        expected_status=201
    ): passed += 1

    # ═══════════════════════════════════════════════════════
    # 🔐 AUTHORIZATION TESTS (Delete Order)
    # ═══════════════════════════════════════════════════════
    print("\n" + "■"*55)
    print(" 🔐 AUTHORIZATION TESTS")
    print("■"*55)

    def auth_test(name, owner_user_id, requester_user_id, expected_status):
        print(f"\n🧪 {name}")
        print(f"{'─'*60}")
        # First create the order so it exists
        temp_req = MockRequest({"order_id":"O001","customer_id":owner_user_id,"product_id":"P001","quantity":2,"status":"Pending"})
        validateOrderCreate(temp_req)
        createOrder(temp_req)
        # Now attempt delete as different user
        req = MockRequest(params={"order_id":"O001"}, auth_user_id=requester_user_id)
        auth_err = authorizeDeleteOrder(req)
        result = auth_err if auth_err else deleteOrder(req)
        actual = result.get("status")
        ok = "✅ PASS" if actual == expected_status else f"❌ FAIL (got {actual}, expected {expected_status})"
        print(f"📊 Result: {ok}")
        print(f"📦 Response: {result}")
        return actual == expected_status

    total += 1
    if auth_test("Wrong user deletes → Forbidden 403", "C001", "C999", 403): passed += 1

    total += 1
    if auth_test("Owner deletes own order → Success 200", "C001", "C001", 200): passed += 1

    # ═══════════════════════════════════════════════════════
    # 📊 FINAL SUMMARY
    # ═══════════════════════════════════════════════════════
    print("\n" + "="*60)
    print(f"📊 FINAL RESULT: {passed}/{total} TESTS PASSED")
    print("="*60)

    if passed == total:
        print("\n✅✅✅ ALL TESTS GREEN — TASK 3 COMPLETE! ✅✅✅")
    else:
        print(f"\n⚠️  {total - passed} test(s) failed — see above")
