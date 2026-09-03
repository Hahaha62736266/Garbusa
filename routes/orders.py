def createOrder(request):
    data = request.body or {}   # ← YOUR EXISTING LINE
                                #
    # ==================================================
    # ✅ PASTE EVERYTHING BELOW THIS LINE ↓
    # ==================================================

    # 🔒 GUARD CLAUSES — Validation checks FIRST
    import re

    # Check order_id
    if not data.get("order_id"):
        return {"status": 422, "error": "order_id is required", "field": "order_id"}
    if not re.match(r"^O\d{3}$", data["order_id"]):
        return {"status": 422, "error": "order_id must be O followed by 3 digits (e.g. O001)", "field": "order_id"}

    # Check customer_id
    if not data.get("customer_id"):
        return {"status": 422, "error": "customer_id is required", "field": "customer_id"}
    if not re.match(r"^C\d{3}$", data["customer_id"]):
        return {"status": 422, "error": "customer_id must be C followed by 3 digits (e.g. C001)", "field": "customer_id"}

    # Check product_id
    if not data.get("product_id"):
        return {"status": 422, "error": "product_id is required", "field": "product_id"}
    if not re.match(r"^P\d{3}$", data["product_id"]):
        return {"status": 422, "error": "product_id must be P followed by 3 digits (e.g. P001)", "field": "product_id"}

    # Check quantity
    if "quantity" not in data:
        return {"status": 422, "error": "quantity is required", "field": "quantity"}
    if not isinstance(data["quantity"], int) or data["quantity"] < 1 or data["quantity"] > 999:
        return {"status": 422, "error": "quantity must be an integer between 1 and 999", "field": "quantity"}

    # Check status
    if not data.get("status"):
        return {"status": 422, "error": "status is required", "field": "status"}
    if data["status"] not in ["Pending", "Delivered"]:
        return {"status": 422, "error": "status must be either Pending or Delivered", "field": "status"}

    # ✅ ALL VALIDATION PASSED — your existing code below runs now

def updateOrder(request):
    data = request.body or {}
    order_id = request.params.get("order_id", "")  # ← from URL
                                                   #
    # ==================================================
    # ✅ PASTE EVERYTHING BELOW THIS LINE ↓
    # ==================================================

    # 🔒 GUARD CLAUSES — Validation checks FIRST
    import re

    # Validate URL order_id FIRST
    if not re.match(r"^O\d{3}$", order_id):
        return {"status": 422, "error": "order_id must be O followed by 3 digits (e.g. O001)", "field": "order_id"}

    # Validate customer_id IF provided
    if "customer_id" in data:
        if not re.match(r"^C\d{3}$", data["customer_id"]):
            return {"status": 422, "error": "customer_id must be C followed by 3 digits (e.g. C001)", "field": "customer_id"}

    # Validate product_id IF provided
    if "product_id" in data:
        if not re.match(r"^P\d{3}$", data["product_id"]):
            return {"status": 422, "error": "product_id must be P followed by 3 digits (e.g. P001)", "field": "product_id"}

    # Validate quantity IF provided
    if "quantity" in data:
        if not isinstance(data["quantity"], int) or data["quantity"] < 1 or data["quantity"] > 999:
            return {"status": 422, "error": "quantity must be an integer between 1 and 999", "field": "quantity"}

    # Validate status IF provided
    if "status" in data and data["status"] not in ["Pending", "Delivered"]:
        return {"status": 422, "error": "status must be either Pending or Delivered", "field": "status"}

    # ✅ ALL VALIDATION PASSED — your existing code below runs now


# ==========================================================
# ROUTES: Orders
# Pipeline: Validation → Authorization → Controller
# ==========================================================

from middleware.validation import (
    validateOrderCreate,
    validateOrderUpdate,
    authorizeDeleteOrder
)
from controllers.order_controller import (
    listOrders,
    showOrder,
    createOrder,
    updateOrder,
    deleteOrder
)

def GET_orders(request):
    """GET /orders — List all"""
    return listOrders(request)

def GET_order_by_id(request):
    """GET /orders/:order_id — Show one"""
    return showOrder(request)

def POST_orders(request):
    """POST /orders — Create"""
    error = validateOrderCreate(request)
    if error:
        return error
    return createOrder(request)

def PUT_order_by_id(request):
    """PUT /orders/:order_id — Update"""
    error = validateOrderUpdate(request)
    if error:
        return error
    return updateOrder(request)

def DELETE_order_by_id(request):
    """DELETE /orders/:order_id — Delete (PROTECTED by auth)"""
    # Step 1: Authorization check → 403 if forbidden
    authError = authorizeDeleteOrder(request)
    if authError:
        return authError

    # Step 2: Allowed → delete
    return deleteOrder(request)
