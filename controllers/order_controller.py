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

def updateOrder(order_id, data):
    """Update an existing order by ID"""
    try:
        # Connect to your database here
        from models.database import get_connection
        conn = get_connection()
        cursor = conn.cursor()

        # Build update fields dynamically
        fields = []
        values = []
        
        if "customer_id" in data:
            fields.append("customer_id = %s")
            values.append(data["customer_id"])
        if "product_id" in data:
            fields.append("product_id = %s")
            values.append(data["product_id"])
        if "quantity" in data:
            fields.append("quantity = %s")
            values.append(data["quantity"])
        if "status" in data:
            fields.append("status = %s")
            values.append(data["status"])
        if "total_amount" in data:
            fields.append("total_amount = %s")
            values.append(data["total_amount"])

        if not fields:
            return {"success": False, "message": "No fields to update"}, 400

        values.append(order_id)
        query = f"UPDATE orders SET {', '.join(fields)} WHERE id = %s"
        
        cursor.execute(query, values)
        conn.commit()

        if cursor.rowcount == 0:
            return {"success": False, "message": "Order not found"}, 404

        return {"success": True, "message": "Order updated successfully"}, 200

    except Exception as e:
        return {"success": False, "message": str(e)}, 500

def updateOrder(order_id, data):
    """Update an existing order record"""
    try:
        from models.database import get_connection
        conn = get_connection()
        cursor = conn.cursor()

        updates = []
        values = []

        if "customer_id" in data:
            updates.append("customer_id = %s")
            values.append(data["customer_id"])
        if "product_id" in data:
            updates.append("product_id = %s")
            values.append(data["product_id"])
        if "quantity" in data:
            updates.append("quantity = %s")
            values.append(data["quantity"])
        if "status" in data:
            updates.append("status = %s")
            values.append(data["status"])
        if "total_amount" in data:
            updates.append("total_amount = %s")
            values.append(data["total_amount"])

        if not updates:
            return {"success": False, "message": "No fields provided to update"}, 400

        values.append(order_id)
        query = f"UPDATE orders SET {', '.join(updates)} WHERE order_id = %s"
        cursor.execute(query, values)
        conn.commit()

        if cursor.rowcount == 0:
            return {"success": False, "message": "Order not found"}, 404

        return {"success": True, "message": "Order updated successfully"}, 200

    except Exception as e:
        return {"success": False, "message": f"Database error: {str(e)}"}, 500

__all__ = ["createOrder", "getAllOrders", "getOrder", "updateOrder", "deleteOrder"]
