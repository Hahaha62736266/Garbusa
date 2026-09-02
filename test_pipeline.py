
# ==========================================================
# TEST RUNNER — Full Pipeline Verification
# Simulates: Request → Validation → Authorization → Controller → Model
# ==========================================================

# ─── Mock Request Object ───
class MockRequest:
    def __init__(self, body=None, params=None, auth_user_id=None):
        self.body = body or {}
        self.params = params or {}
        self.validatedBody = None  # Set by validation middleware
        self.auth = {"user_id": auth_user_id} if auth_user_id else None


# ─── Import ALL layers ───
from middleware.validation import (
    validateCustomerCreate, validateCustomerUpdate,
    validateProductCreate,
    validateOrderCreate, authorizeDeleteOrder,
    validateCollectionCreate
)
from controllers.customer_controller import createCustomer
from controllers.product_controller import createProduct
from controllers.order_controller import createOrder, deleteOrder
from controllers.collection_controller import createCollection


# ─── Test Helper ───
def run_test(name, request, validation_fn=None, auth_fn=None, controller_fn=None):
    print(f"\n{'='*60}")
    print(f"🧪 TEST: {name}")
    print(f"{'='*60}")
    print(f"📥 Input body: {request.body}")
    print(f"🔑 Params: {request.params}")
    print(f"👤 Auth User: {request.auth.get('user_id') if request.auth else 'None'}")

    result = None
    step = "STARTED"

    try:
        # Step 1: VALIDATION
        if validation_fn:
            step = "VALIDATION"
            error = validation_fn(request)
            if error:
                print(f"❌ {step} FAILED → {error}")
                result = error
                return result
            print(f"✅ {step} PASSED → validatedBody set")

        # Step 2: AUTHORIZATION
        if auth_fn:
            step = "AUTHORIZATION"
            error = auth_fn(request)
            if error:
                print(f"❌ {step} FAILED → {error}")
                result = error
                return result
            print(f"✅ {step} PASSED → permission granted")

        # Step 3: CONTROLLER → MODEL
        if controller_fn:
            step = "CONTROLLER+MODEL"
            result = controller_fn(request)
            print(f"✅ {step} PASSED → {result}")

    except Exception as e:
        print(f"💥 EXCEPTION in {step}: {type(e).__name__}: {e}")
        result = {"status": 500, "error": str(e), "field": None}

    return result


# ==========================================================
# 🚀 RUN ALL TESTS
# ==========================================================
if __name__ == "__main__":
    print("\n" + "🎯"*30)
    print(" FULL PIPELINE TEST: Validation → Auth → Controller → Model ")
    print("🎯"*30)

    # ─── TEST 1: Create Customer — VALID DATA ───
    run_test(
        "Create Customer — VALID DATA",
        MockRequest({
            "customer_id": "C001",
            "full_name": "Juan Dela Cruz",
            "contact_number": "0917-123-4567",
            "address": "Manila City, PH",
            "container_owned": 5
        }),
        validation_fn=validateCustomerCreate,
        controller_fn=createCustomer
    )

    # ─── TEST 2: Create Customer — INVALID (missing field) ───
    run_test(
        "Create Customer — MISSING full_name → should return 422",
        MockRequest({
            "customer_id": "C002",
            "contact_number": "0917-123-4567",
            "address": "Cebu City",
            "container_owned": 2
        }),
        validation_fn=validateCustomerCreate,
        controller_fn=createCustomer
    )

    # ─── TEST 3: Create Customer — WRONG FORMAT → should return 422 ───
    run_test(
        "Create Customer — BAD ID FORMAT → should return 422",
        MockRequest({
            "customer_id": "CUS999",  # ❌ Should be C###
            "full_name": "Valid Name",
            "contact_number": "0917-123-4567",
            "address": "Valid Address Here",
            "container_owned": 1
        }),
        validation_fn=validateCustomerCreate,
        controller_fn=createCustomer
    )

    # ─── TEST 4: Create Product — VALID DATA ───
    run_test(
        "Create Product — VALID DATA",
        MockRequest({
            "product_id": "P001",
            "product_name": "Purified Water 5Gal",
            "price_per_unit": 85.50,
            "stock_available": 50
        }),
        validation_fn=validateProductCreate,
        controller_fn=createProduct
    )

    # ─── TEST 5: Create Order — VALID DATA ───
    run_test(
        "Create Order — VALID DATA",
        MockRequest({
            "order_id": "O001",
            "customer_id": "C001",
            "product_id": "P001",
            "quantity": 3,
            "status": "Pending"
        }),
        validation_fn=validateOrderCreate,
        controller_fn=createOrder
    )

    # ─── TEST 6: Create Order — INVALID STATUS → should return 422 ───
    run_test(
        "Create Order — INVALID STATUS → should return 422",
        MockRequest({
            "order_id": "O002",
            "customer_id": "C001",
            "product_id": "P001",
            "quantity": 2,
            "status": "Cancelled"  # ❌ Only Pending/Delivered allowed
        }),
        validation_fn=validateOrderCreate,
        controller_fn=createOrder
    )

    # ─── TEST 7: DELETE Order — WRONG USER → should return 403 ───
    run_test(
        "DELETE Order — WRONG USER → should return 403 Forbidden",
        MockRequest(
            body={},
            params={"order_id": "O001"},
            auth_user_id="C999"  # ❌ Different user from owner C001
        ),
        auth_fn=authorizeDeleteOrder,
        controller_fn=deleteOrder
    )

    # ─── TEST 8: DELETE Order — CORRECT OWNER → should PASS ───
    run_test(
        "DELETE Order — CORRECT OWNER → should PASS",
        MockRequest(
            body={},
            params={"order_id": "O001"},
            auth_user_id="C001"  # ✅ Matches order's customer_id
        ),
        auth_fn=authorizeDeleteOrder,
        controller_fn=deleteOrder
    )

    # ─── TEST 9: Create Collection — VALID DATA ───
    run_test(
        "Create Collection — VALID DATA",
        MockRequest({
            "collection_id": "CL001",
            "customer_id": "C001",
            "order_id": "O001",
            "empty_jugs_returned": 2,
            "filled_jugs_released": 3,
            "container_balance": 5,
            "collected_by": "Juan Dela Cruz"
        }),
        validation_fn=validateCollectionCreate,
        controller_fn=createCollection
    )

    print("\n" + "="*60)
    print("✅ ALL TESTS COMPLETE — Review output above!")
    print("="*60)
