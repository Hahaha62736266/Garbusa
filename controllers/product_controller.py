"""Product Controller — MockRequest compatible"""

products_db = {}

def listProducts():
    return {
        "status": 200,
        "message": "Products retrieved successfully",
        "data": list(products_db.values())
    }

def showProduct(product_id):
    if product_id not in products_db:
        return {"status": 404, "error": "Not Found", "message": "Product not found"}
    return {"status": 200, "message": "Product retrieved", "data": products_db[product_id]}

def createProduct(data):
    # ✅ FORCE extract JSON — NO fallback to MockRequest object
    if hasattr(data, 'json') and data.json is not None:
        payload = data.json
    else:
        # LAST RESORT — convert MANUALLY to dictionary
        payload = {
            "product_name": getattr(data, "product_name", None),
            "price_per_unit": getattr(data, "price_per_unit", 0.0),
            "description": getattr(data, "description", ""),
            "stock_available": getattr(data, "stock_available", 0)
        }

    new_id = f"P{len(products_db)+1:03d}"
    product = {
        "product_id": new_id,
        "product_name": payload.get("product_name"),
        "price_per_unit": payload.get("price_per_unit", 0.0),
        "description": payload.get("description", ""),
        "stock_available": payload.get("stock_available", 0)
    }
    products_db[new_id] = product
    return {
        "status": 201,
        "message": "Product created",
        "data": {
            "id": len(products_db),
            "product_id": new_id,
            "product_name": product["product_name"],
            "price_per_unit": product["price_per_unit"],
            "stock_available": product["stock_available"]
        }
    }

def updateProduct(product_id, data):
    if hasattr(data, 'json'):
        payload = data.json
    else:
        payload = data
    if product_id not in products_db:
        return {"status": 404, "error": "Not Found", "message": "Product not found"}
    for k, v in payload.items():
        if k != "product_id":
            products_db[product_id][k] = v
    return {"status": 200, "message": "Product updated", "data": products_db[product_id]}

def deleteProduct(product_id):
    if product_id not in products_db:
        return {"status": 404, "error": "Not Found", "message": "Product not found"}
    deleted = products_db.pop(product_id)
    return {"status": 200, "message": "Product deleted", "data": deleted}