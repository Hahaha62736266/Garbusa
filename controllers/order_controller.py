# ==========================================================
# THIN CONTROLLER: Orders
# ==========================================================
from models.order_model import Order

def listOrders(request):
    orders = Order.all()
    return {"status": 200, "data": orders, "error": None}

def showOrder(request):
    order_id = request.params.get("order_id")
    order = Order.find(order_id)
    return {"status": 200, "data": order, "error": None}

def createOrder(request):
    data = request.validatedBody
    order = Order.save(data)
    return {"status": 201, "data": order, "error": None}

def updateOrder(request):
    order_id = request.params.get("order_id")
    data = request.validatedBody
    order = Order.update(order_id, data)
    return {"status": 200, "data": order, "error": None}

def deleteOrder(request):
    order_id = request.params.get("order_id")
    Order.remove(order_id)
    return {"status": 200, "data": {"deleted_id": order_id}, "error": None}
