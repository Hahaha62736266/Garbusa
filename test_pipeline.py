import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# ==========================================================
# TEST SUITE — Arrange / Act / Assert Pattern
# Per Controller: Happy Path + Validation Failure + Edge Case
# ==========================================================

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


# ─── TEST HELPER ───
def run_test(name, request, validation_fn, controller_fn, expected_status):
    print(f"\n{'─'*60}")
    print(f"🧪 {name}")
    print(f"{'─'*60}")

    # ARRANGE
    # (request already prepared above)

    # ACT
    error = validation_fn(request)
    if error:
        result = error
    else:
        result = controller_fn(request)

    # ASSERT
    actual_status = result.get("status")
    status = "✅ PASS" if actual_status == expected_status else f"❌ FAIL (got {actual_status}, expected {expected_status})"
    print(f"   Status: {status}")
    print(f"   Result: {result}")
    return actual_status == expected_status


# ==========================================================
# 🚀 ALL TESTS
# ==========================================================
if __name__ == "__main__":
    print("\n" + "🎯"*25)
    print(" FULL TEST SUITE — ALL CONTROLLERS ")
    print("🎯"*25)

    passed = 0
    total = 0

    # ─── CUSTOMER TESTS ───
    print("\n" + "■"*40)
    print(" 🧾 CUSTOMER CONTROLLER TESTS")
    print("■"*40)

    total +=1
    if run_test("Customer — Happy Path (valid data → 201)",
        MockRequest({"customer_id":"C001","full_name":"Maria Santos","contact_number":"0917-111-2222","address":"Makati City, PH","container_owned":3}),
        validateCustomerCreate, createCustomer, 201): passed +=1

    total +=1
    if run_test("Customer — Validation Fail (missing name → 422)",
        MockRequest({"customer_id":"C002","contact_number":"0917-333-4444","address":"Quezon City","container_owned":1}),
        validateCustomerCreate, createCustomer, 422): passed +=1

    total +=1
    if run_test("Customer — Edge Case (bad ID format → 422)",
        MockRequest({"customer_id":"CUS999","full_name":"Bad Format User","contact_number":"0917-555-6666","address":"Valid Address Here","container_owned":0}),
        validateCustomerCreate, createCustomer, 422): passed +=1


    # ─── PRODUCT TESTS ───
    print("\n" + "■"*40)
    print(" 🧾 PRODUCT CONTROLLER TESTS")
    print("■"*40)

    total +=1
    if run_test("Product — Happy Path (valid data → 201)",
        MockRequest({"product_id":"P001","product_name":"5Gal Purified Water","price_per_unit":85.50,"stock_available":100}),
        validateProductCreate, createProduct, 201): passed +=1

    total +=1
    if run_test("Product — Validation Fail (negative price → 422)",
        MockRequest({"product_id":"P002","product_name":"Invalid Product","price_per_unit":-10.00,"stock_available":50}),
        validateProductCreate, createProduct, 422): passed +=1

    total +=1
    if run_test("Product — Edge Case (zero stock → valid → 201)",
        MockRequest({"product_id":"P003","product_name":"Out of Stock Item","price_per_unit":50.00,"stock_available":0}),
        validateProductCreate, createProduct, 201): passed +=1


    # ─── ORDER TESTS ───
    print("\n" + "■"*40)
    print(" 🧾 ORDER CONTROLLER TESTS")
    print("■"*40)

    total +=1
    if run_test("Order — Happy Path (valid data → 201)",
        MockRequest({"order_id":"O001","customer_id":"C001","product_id":"P001","quantity":3,"status":"Pending"}),
        validateOrderCreate, createOrder, 201): passed +=1

    total +=1
    if run_test("Order — Validation Fail (negative qty → 422)",
        MockRequest({"order_id":"O002","customer_id":"C001","product_id":"P001","quantity":-5,"status":"Pending"}),
        validateOrderCreate, createOrder, 422): passed +=1

    total +=1
    if run_test("Order — Edge Case (invalid status → 422)",
        MockRequest({"order_id":"O003","customer_id":"C001","product_id":"P001","quantity":1,"status":"Cancelled"}),
        validateOrderCreate, createOrder, 422): passed +=1


    # ─── COLLECTION TESTS ───
    print("\n" + "■"*40)
    print(" 🧾 COLLECTION CONTROLLER TESTS")
    print("■"*40)

    total +=1
    if run_test("Collection — Happy Path (valid data → 201)",
        MockRequest({"collection_id":"CL001","customer_id":"C001","order_id":"O001","empty_jugs_returned":2,"filled_jugs_released":3,"container_balance":5,"collected_by":"Delivery Team A"}),
        validateCollectionCreate, createCollection, 201): passed +=1

    total +=1
    if run_test("Collection — Validation Fail (negative balance → 422)",
        MockRequest({"collection_id":"CL002","customer_id":"C001","order_id":"O001","empty_jugs_returned":5,"filled_jugs_released":3,"container_balance":-2,"collected_by":"Team B"}),
        validateCollectionCreate, createCollection, 422): passed +=1

    total +=1
    if run_test("Collection — Edge Case (zero returns → valid → 201)",
        MockRequest({"collection_id":"CL003","customer_id":"C001","order_id":"O001","empty_jugs_returned":0,"filled_jugs_released":10,"container_balance":10,"collected_by":"Team C"}),
        validateCollectionCreate, createCollection, 201): passed +=1


    # ─── AUTHORIZATION TEST ───
    print("\n" + "■"*40)
    print(" 🔐 AUTHORIZATION TEST (DELETE)")
    print("■"*40)

    def test_auth_delete(name, request, expected_status):
        print(f"\n🧪 {name}")
        auth_err = authorizeDeleteOrder(request)
        result = auth_err if auth_err else deleteOrder(request)
        actual = result.get("status")
        ok = "✅ PASS" if actual == expected_status else f"❌ FAIL (got {actual}, expected {expected_status})"
        print(f"   Status: {ok}")
        print(f"   Result: {result}")
        return actual == expected_status

    total +=1
    if test_auth_delete("Delete Order — Wrong User → Forbidden 403",
        MockRequest({}, params={"order_id":"O001"}, auth_user_id="C999"), 403): passed +=1

    total +=1
    if test_auth_delete("Delete Order — Correct Owner → Success 200",
        MockRequest({}, params={"order_id":"O001"}, auth_user_id="C001"), 200): passed +=1


    # ==========================================================
    # 📊 FINAL SUMMARY
    # ==========================================================
    print("\n" + "="*60)
    print(f"📊 FINAL RESULT: {passed}/{total} TESTS PASSED")
    if passed == total:
        print("✅✅✅ ALL TESTS GREEN — FULLY WORKING! ✅✅✅")
    else:
        print(f"⚠️  {total-passed} test(s) failed — check output above")
    print("="*60)
