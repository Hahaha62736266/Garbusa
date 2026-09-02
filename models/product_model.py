# ==========================================================
# DATA LAYER: Product Model
# ==========================================================

_products = {}
_next_id = 1

def all():
    return list(_products.values())

def find(product_id):
    return _products.get(product_id)

def save(data):
    global _next_id
    record = {
        "id": _next_id,
        "product_id": data.get("product_id"),
        "product_name": data.get("product_name"),
        "price_per_unit": float(data.get("price_per_unit", 0)),
        "stock_available": data.get("stock_available", 0)
    }
    _products[data["product_id"]] = record
    _next_id += 1
    return record

def update(product_id, data):
    record = _products.get(product_id)
    if not record:
        return None
    if "product_name" in data: record["product_name"] = data["product_name"]
    if "price_per_unit" in data: record["price_per_unit"] = float(data["price_per_unit"])
    if "stock_available" in data: record["stock_available"] = data["stock_available"]
    return record

def remove(product_id):
    if product_id in _products:
        del _products[product_id]
        return True
    return False
