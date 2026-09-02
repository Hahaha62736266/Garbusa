import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# ==========================================================
# TASK 3 — Automated Tests: Arrange / Act / Assert
# Per Controller: Happy Path + Validation Failure + Edge Case
# ==========================================================

class MockRequest:
    """Fake request object — simulates what the framework passes"""
    def __init__(self, body=None, params=None, auth_user_id=None):
        self.body = body or {}
        self.params = params or {}
        self.validatedBody = None  # Set by validation middleware
        self.auth = {"user_id": auth_user_id} if auth_user_id else None


# ─── Import ALL layers ───
from middleware.validation import (
    validateCustomerCreate, validateProductCreate,
    validateOrderCreate, validateCollectionCreate,
    authorizeDeleteOrder
)
from controllers.customer_controller import createCustomer
from controllers.product_controller import createProduct
from controllers.order_controller import createOrder, deleteOrder
from controllers.collection_controller import createCollection


# ─── TEST RUNNER: Arrange → Act → Assert ───
def test(name, validation_fn, controller_fn, request_body, expected_status, params=None, auth_user_id=None):
    """
    ARRANGE → prepare request
    ACT     → validate → if valid, call controller
    ASSERT  → check status code matches expected
    """
    print(f"\n{'─'*60}")
    print(f"🧪 TEST: {name}")
    print(f"{'─'*60}")
    print(f"📥 Input: {request_body}")

    # ARRANGE
    req = MockRequest(
        body=request_body,
        params=params or {},
        auth_user_id=auth_user_id
    )

    # ACT
    validation_error = validation_fn(req)
    if validation_error:
        result = validation_error
    else:
        result = controller_fn(req)

    # ASSERT
    actual_status = result.get("status")
    status = "✅ PASS" if actual_status == expected_status else f"❌ FAIL (got {actual_status}, expected {expected_status})"
    print(f"📊 Result: {status}")
    print(f"📦 Full Response: {result}")

    return actual_status == expected_status


# ==========================================================
# 🚀 ALL TESTS — RUN SUITE
# ==========================================================
if __name__ == "__main__":
    print("\n" + "🎯"*20)
    print("  TASK 3 — FULL TEST SUITE ")
    print("🎯"*20)

    passed = 0
    total = 0

    # ═══════════════════════════════════════════════════════
    # 🧾 CUSTOMER CONTROLLER TESTS
    # ═══════════════════════════════════════════════════════
    print("\n" + "■"*50)
    print(" 🧾 CUSTOMER TESTS")
    print("■"*50)

    total += 1
    if test(
        "Happy Path: Valid customer → returns 201 Created",
        validateCustomerCreate, createCustomer,
        request_body={
            "customer_id": "C001",
            "full_name": "Juan Dela Cruz",
            "contact_number": "0917-123-4567",
            "address": "Cagayan de Oro, PH",
            "container_owned": 5
        },
        expected_status=201
    ): passed += 1

    total += 1
    if test(
        "Validation Fail: Missing full_name → returns 422",
        validateCustomerCreate, createCustomer,
        request_body={
            "customer_id": "C002",
            "contact_number": "0917-111-2222",
            "address": "Misamis Oriental",
            "container_owned": 2
        },
        expected_status=422
    ): passed += 1

    total += 1
    if test(
        "Edge Case: Invalid customer_id format → returns 422",
        validateCustomerCreate, createCustomer,
        request_body={
            "customer_id": "CUS999",  # ❌ Should be C###
            "full_name": "Invalid Format User",
            "contact_number": "0917-333-4444",
            "address": "CDO, PH",
            "container_owned": 0
        },
        expected_status=422
    ): passed += 1

    # ═══════════════════════════════════════════════════════
    # 🧾 PRODUCT CONTROLLER TESTS
    # ═══════════════════════════════════════════════════════
    print("\n" + "■"*50)
    print(" 🧾 PRODUCT TESTS")
    print("■"*50)

    total += 1
    if test(
        "Happy Path: Valid product → returns 201 Created",
        validateProductCreate, createProduct,
        request_body={
            "product_id": "P001",
            "product_name": "5-Gallon Purified Water",
            "price_per_unit": 85.50,
            "stock_available": 100
        },
        expected_status=201
    ): passed += 1

    total += 1
    if test(
        "Validation Fail: Negative price → returns 422",
        validateProductCreate, createProduct,
        request_body={
            "product_id": "P002",
            "product_name": "Invalid Product",
            "price_per_unit": -10.00,  # ❌ Negative price
            "stock_available": 50
        },
        expected_status=422
    ): passed += 1

    total += 1
    if test(
        "Edge Case: Zero stock available → returns 201 (valid)",
        validateProductCreate, createProduct,
        request_body={
            "product_id": "P003",
            "product_name": "Out-of-Stock Item",
            "price_per_unit": 75.00,
            "stock_available": 0  # ✅ Zero is allowed
        },
        expected_status=201
    ): passed += 1

    # ═══════════════════════════════════════════════════════
    # 🧾 ORDER CONTROLLER TESTS
    # ═══════════════════════════════════════════════════════
    print("\n" + "■"*50)
    print(" 🧾 ORDER TESTS")
    print("■"*50)

    total += 1
    if test(
        "Happy Path: Valid order → returns 201 Created",
        validateOrderCreate, createOrder,
        request_body={
            "order_id": "O001",
            "customer_id": "C001",
            "product_id": "P001",
            "quantity": 3,
            "status": "Pending"
        },
        expected_status=201
    ): passed += 1

    total += 1
    if test(
        "Validation Fail: Negative quantity → returns 422",
        validateOrderCreate, createOrder,
        request_body={
            "order_id": "O002",
            "customer_id": "C001",
            "product_id": "P001",
            "quantity": -5,  # ❌ Negative quantity
            "status": "Pending"
        },
        expected_status=422
    ): passed += 1

    total += 1
    if test(
        "Edge Case: Invalid status value → returns 422",
        validateOrderCreate, createOrder,
        request_body={
            "order_id": "O003",
            "customer_id": "C001",
            "product_id": "P001",
            "quantity": 2,
            "status": "Cancelled"  # ❌ Not allowed
        },
        expected_status=422
    ): passed += 1

    # ═══════════════════════════════════════════════════════
    # 🧾 COLLECTION CONTROLLER TESTS
    # ═══════════════════════════════════════════════════════
    print("\n" + "■"*50)
    print(" 🧾 COLLECTION TESTS")
    print("■"*50)

    total += 1
    if test(
        "Happy Path: Valid collection → returns 201 Created",
        validateCollectionCreate, createCollection,
        request_body={
            "collection_id": "CL001",
            "customer_id": "C001",
            "order_id": "O001",
            "empty_jugs_returned": 2,
            "filled_jugs_released": 5,
            "container_balance": 3,
            "collected_by": "Delivery Team A"
        },
        expected_status=201
    ): passed += 1

    total += 1
    if test(
        "Validation Fail: Negative container balance → returns 422",
        validateCollectionCreate, createCollection,
        request_body={
            "collection_id": "CL002",
            "customer_id": "C001",
            "order_id": "O001",
            "empty_jugs_returned": 5,
            "filled_jugs_released": 3,
            "container_balance": -2,  # ❌ Negative balance
            "collected_by": "Delivery Team B"
        },
        expected_status=422
    ): passed += 1

    total += 1
    if test(
        "Edge Case: Zero jugs returned → returns 201 (valid)",
        validateCollectionCreate, createCollection,
        request_body={
            "collection_id": "CL003",
            "customer_id": "C001",
            "order_id": "O001",
            "empty_jugs_returned": 0,  # ✅ Zero returns allowed
            "filled_jugs_released": 10,
            "container_balance": 10,
            "collected_by": "Delivery Team C"
        },
        expected_status=201
    ): passed += 1

    # ═══════════════════════════════════════════════════════
    # 🔐 AUTHORIZATION TESTS (DELETE Order)
    # ═══════════════════════════════════════════════════════
    print("\n" + "■"*50)
    print(" 🔐 AUTHORIZATION TESTS")
    print("■"*50)

    def test_auth_delete(name, order_exists, requester_user_id, expected_status):
        print(f"\n🧪 TEST: {name}")
        print(f"{'─'*60}")
        print(f"📋 Order exists: {order_exists} | Requester: {requester_user_id}")

        # First create the order so it exists in storage
        if order_exists:
            temp_req = MockRequest({"order_id":"O001","customer_id":"C001","product_id":"P001","quantity":2,"status":"Pending"})
            validateOrderCreate(temp_req)
            createOrder(temp_req)

        # Now attempt delete
        req = MockRequest(params={"order_id":"O001"}, auth_user_id=requester_user_id)
        auth_err = authorizeDeleteOrder(req)
        result = auth_err if auth_err else deleteOrder(req)
        actual = result.get("status")

        status = "✅ PASS" if actual == expected_status else f"❌ FAIL (got {actual}, expected {expected_status})"
        print(f"📊 Result: {status}")
        print(f"📦 Full Response: {result}")
        return actual == expected_status

    total += 1
    if test_auth_delete(
        "Forbidden: Wrong user tries to delete → returns 403",
        order_exists=True,
        requester_user_id="C999",  # ❌ Not the owner
        expected_status=403
    ): passed += 1

    total += 1
    if test_auth_delete(
        "Allowed: Owner deletes own order → returns 200",
        order_exists=True,
        requester_user_id="C001",  # ✅ Matches order's customer_id
        expected_status=200
    ): passed += 1

    # ═══════════════════════════════════════════════════════
    # 📊 FINAL SUMMARY
    # ═══════════════════════════════════════════════════════
    print("\n" + "="*60)
    print(f"📊 FINAL RESULT: {passed}/{total} TESTS PASSED")
    print("="*60)

    if passed == total:
        print("✅✅✅ ALL TESTS GREEN — TASK 3 COMPLETE! ✅✅✅")
    else:
        print(f"⚠️  {total - passed} test(s) failed — review output above")
    print("="*60)
