"""Order Routes — Validation → Authorization → Controller pipeline"""
import re
from flask import request
# In-memory "database" — shared with controller or use controller functions
orders_db = {}

# ==================================================
# CREATE Order
# ==================================================
def createOrder(request):
    data = request.body or {}

    # 🔒 Validation checks FIRST
    if not data.get("order_id"):
        return {"status": 422, "error": "order_id is required", "field": "order_id"}
    if not re.match(r"^O\d{3}$", data["order_id"]):
        return {"status": 422, "error": "order_id must be O followed by 3 digits (e.g. O001)", "field": "order_id"}

    if not data.get("customer_id"):
        return {"status": 422, "error": "customer_id is required", "field": "customer_id"}
    if not re.match(r"^C\d{3}$", data["customer_id"]):
        return {"status": 422, "error": "customer_id must be C followed by 3 digits (e.g. C001)", "field": "customer_id"}

    if not data.get("product_id"):
        return {"status": 422, "error": "product_id is required", "field": "product_id"}
    if not re.match(r"^P\d{3}$", data["product_id"]):
        return {"status": 422, "error": "product_id must be P followed by 3 digits (e.g. P001)", "field": "product_id"}

    if "quantity" not in data:
        return {"status": 422, "error": "quantity is required", "field": "quantity"}
    if not isinstance(data["quantity"], int) or data["quantity"] < 1 or data["quantity"] > 999:
        return {"status": 422, "error": "quantity must be an integer between 1 and 999", "field": "quantity"}

    if not data.get("status"):
        return {"status": 422, "error": "status is required", "field": "status"}
    if data["status"] not in ["Pending", "Delivered"]:
        return {"status": 422, "error": "status must be either Pending or Delivered", "field": "status"}

    # ✅ ALL VALIDATION PASSED → Call Controller
    from controllers.order_controller import createOrder as controller_createOrder
    return controller_createOrder(request)


# ==================================================
# UPDATE Order
# ==================================================
def updateOrder(request):
    data = request.body or {}
    order_id = request.params.get("order_id", "")

    # 🔒 Validation checks FIRST
    if not re.match(r"^O\d{3}$", order_id):
        return {"status": 422, "error": "order_id must be O followed by 3 digits (e.g. O001)", "field": "order_id"}

    if "customer_id" in data and not re.match(r"^C\d{3}$", data["customer_id"]):
        return {"status": 422, "error": "customer_id must be C followed by 3 digits (e.g. C001)", "field": "customer_id"}

    if "product_id" in data and not re.match(r"^P\d{3}$", data["product_id"]):
        return {"status": 422, "error": "product_id must be P followed by 3 digits (e.g. P001)", "field": "product_id"}

    if "quantity" in data:
        if not isinstance(data["quantity"], int) or data["quantity"] < 1 or data["quantity"] > 999:
            return {"status": 422, "error": "quantity must be an integer between 1 and 999", "field": "quantity"}

    if "status" in data and data["status"] not in ["Pending", "Delivered"]:
        return {"status": 422, "error": "status must be either Pending or Delivered", "field": "status"}

    # ✅ ALL VALIDATION PASSED → Call Controller
    from controllers.order_controller import updateOrder as controller_updateOrder
    return controller_updateOrder(request)


# ==================================================
# ROUTE HANDLERS
# Pipeline: Validation → Authorization → Controller
# ==================================================
from middleware.validation import (
    validateOrderCreate,
    validateOrderUpdate,
    authorizeDeleteOrder
)
from controllers.order_controller import (
    listOrders,
    showOrder,
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
    # ✅ Step 1: Authorization check FIRST → returns 403 if forbidden
    authError = authorizeDeleteOrder(request)
    if authError:
        return authError
    # ✅ Step 2: Allowed → proceed to delete
    return deleteOrder(request)

