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
