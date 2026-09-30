"""Order Controller — MockRequest compatible"""
from datetime import date

orders_db = {}

def listOrders():
    return {
        "status": 200,
        "message": "Orders retrieved successfully",
        "data": list(orders_db.values())
    }

def showOrder(order_id):
    """Get single order by ID — accepts string ID OR request object"""
    # ✅ Handle BOTH: string ID from middleware, OR request object from routes
    if not isinstance(order_id, str):
        # It's a request object → extract ID from params
        order_id = getattr(order_id, 'params', {}).get("order_id", "")
    
    if order_id not in orders_db:
        return {"status": 404, "error": "Not Found", "message": "Order not found"}
    return {
        "status": 200,
        "message": "Order retrieved",
        "data": orders_db[order_id]
    }

def createOrder(data):
    # ✅ Read from __dict__ — gets ALL fields reliably
    if hasattr(data, '__dict__'):
        payload = data.__dict__
    elif hasattr(data, 'json') and data.json is not None:
        payload = data.json
    else:
        payload = data if isinstance(data, dict) else {}

    new_id = f"O{len(orders_db)+1:03d}"
    order = {
        "order_id": new_id,
        "customer_id": payload.get("customer_id"),
        "product_id": payload.get("product_id"),
        "quantity": payload.get("quantity", 1),
        "status": payload.get("status", "Pending"),
        "owned_by_user_id": payload.get("owned_by_user_id", "admin")  # ✅ CRITICAL FOR AUTH
    }
    orders_db[new_id] = order

    return {
        "status": 201,
        "message": "Order created",
        "data": {
            "id": len(orders_db),
            "order_id": new_id,
            "customer_id": order["customer_id"],
            "product_id": order["product_id"],
            "quantity": order["quantity"],
            "status": order["status"]
        }
    }
    if hasattr(data, 'json'):
        payload = data.json
    else:
        payload = data
    if order_id not in orders_db:
        return {"status": 404, "error": "Not Found", "message": "Order not found"}
    for k, v in payload.items():
        if k != "order_id":
            orders_db[order_id][k] = v
    return {"status": 200, "message": "Order updated", "data": orders_db[order_id]}

def deleteOrder(order_id):
    if order_id not in orders_db:
        return {"status": 404, "error": "Not Found", "message": "Order not found"}
    deleted = orders_db.pop(order_id)
    return {"status": 200, "message": "Order deleted", "data": deleted}