# ===================================
# Order Stub Handlers
# ===================================

def listOrders(request):
    """GET /orders — List all orders"""
    return {
        "status": 200,
        "data": { "message": "listOrders stub" },
        "error": None
    }


def showOrder(request):
    """GET /orders/:order_id — View one order"""
    order_id = request.params.get("order_id")
    return {
        "status": 200,
        "data": {
            "message": "showOrder stub",
            "order_id": order_id
        },
        "error": None
    }


def createOrder(request):
    """POST /orders — Create new order"""
    return {
        "status": 201,
        "data": { "message": "createOrder stub" },
        "error": None
    }


def updateOrder(request):
    """PUT /orders/:order_id — Update order"""
    order_id = request.params.get("order_id")
    return {
        "status": 200,
        "data": {
            "message": "updateOrder stub",
            "order_id": order_id
        },
        "error": None
    }


def deleteOrder(request):
    """DELETE /orders/:order_id — Delete order"""
    order_id = request.params.get("order_id")
    return {
        "status": 200,
        "data": {
            "message": "deleteOrder stub",
            "order_id": order_id
        },
        "error": None
    }
