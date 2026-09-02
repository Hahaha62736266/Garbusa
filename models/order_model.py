# ==========================================================
# DATA LAYER: Order Model
# ==========================================================

_orders = {}
_next_id = 1

def all():
    return list(_orders.values())

def find(order_id):
    return _orders.get(order_id)

def save(data):
    global _next_id
    record = {
        "id": _next_id,
        "order_id": data.get("order_id"),
        "customer_id": data.get("customer_id"),
        "product_id": data.get("product_id"),
        "quantity": data.get("quantity"),
        "status": data.get("status", "Pending")
    }
    _orders[data["order_id"]] = record
    _next_id += 1
    return record

def update(order_id, data):
    record = _orders.get(order_id)
    if not record:
        return None
    if "customer_id" in data: record["customer_id"] = data["customer_id"]
    if "product_id" in data: record["product_id"] = data["product_id"]
    if "quantity" in data: record["quantity"] = data["quantity"]
    if "status" in data: record["status"] = data["status"]
    return record

def remove(order_id):
    if order_id in _orders:
        del _orders[order_id]
        return True
    return False
