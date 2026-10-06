"""Order Controller — MockRequest compatible"""
from datetime import date

# In-memory "database"
orders_db = {}

def _extract_payload(data):
    if hasattr(data, 'validatedBody') and data.validatedBody is not None:
        return data.validatedBody
    if hasattr(data, 'body') and data.body is not None:
        return data.body
    if hasattr(data, 'get_json') and callable(data.get_json):
        j = data.get_json()
        if j is not None:
            return j
    if hasattr(data, 'json') and data.json is not None:
        return data.json
    if isinstance(data, dict):
        return data
    if hasattr(data, '__dict__'):
        d = data.__dict__
        if 'validatedBody' in d and d['validatedBody']:
            return d['validatedBody']
        if 'body' in d and d['body']:
            return d['body']
        return d
    return {}

def listOrders(request=None):
    return {
        "status": 200,
        "message": "Orders retrieved successfully",
        "data": list(orders_db.values())
    }

list_orders = listOrders

def showOrder(order_id):
    """Get single order by ID — accepts string ID OR request object"""
    if not isinstance(order_id, str):
        order_id = getattr(order_id, 'params', {}).get("order_id", "")
    
    if order_id not in orders_db:
        return {"status": 404, "error": "Not Found", "message": "Order not found"}
    return {
        "status": 200,
        "message": "Order retrieved",
        "data": orders_db[order_id]
    }

show_order = showOrder

def createOrder(data):
    """Create a new order"""
    payload = _extract_payload(data)

    # Validation - required fields
    if not payload.get("customer_id"):
        return {"status": 400, "error": "Bad Request", "message": "customer_id is required"}
    
    if not payload.get("product_id"):
        return {"status": 400, "error": "Bad Request", "message": "product_id is required"}

    if not payload.get("quantity"):
        return {"status": 400, "error": "Bad Request", "message": "quantity is required"}

    new_id = payload.get("order_id") or f"O{len(orders_db)+1:03d}"
    customer_id = payload.get("customer_id")
        "order_id": new_id,
        "customer_id": customer_id,
        "product_id": payload.get("product_id"),
        "quantity": payload.get("quantity", 1),
        "status": payload.get("status", "Pending"),
        "owned_by_user_id": payload.get("owned_by_user_id") or customer_id or "admin"
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

create_order = createOrder

def updateOrder(order_id, data=None):
    """Update an existing order"""
    if data is None and hasattr(order_id, 'params'):
        req = order_id
        order_id = req.params.get("order_id", "")
        data = req

    if not isinstance(order_id, str):
        order_id = getattr(order_id, 'params', {}).get("order_id", "")
    
    if order_id not in orders_db:
        return {"status": 404, "error": "Not Found", "message": "Order not found"}
    
    payload = _extract_payload(data)
    
    for k, v in payload.items():
        if k != "order_id":
            orders_db[order_id][k] = v
    
    return {
        "status": 200,
        "message": "Order updated",
        "data": orders_db[order_id]
    }

update_order = updateOrder

def deleteOrder(order_id):
    """Delete an order by ID"""
    if not isinstance(order_id, str):
        order_id = getattr(order_id, 'params', {}).get("order_id", "")
    
    if order_id not in orders_db:
        return {"status": 404, "error": "Not Found", "message": "Order not found"}
    
    deleted = orders_db.pop(order_id)
    return {
        "status": 200,
        "message": "Order deleted",
        "data": deleted
    }

delete_order = deleteOrder
