"""Product Controller — MockRequest compatible"""

products_db = {}

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

def listProducts(request=None):
    return {
        "status": 200,
        "message": "Products retrieved successfully",
        "data": list(products_db.values())
    }

list_products = listProducts

def showProduct(product_id):
    if not isinstance(product_id, str):
        product_id = getattr(product_id, 'params', {}).get("product_id", "")
    if product_id not in products_db:
        return {"status": 404, "error": "Not Found", "message": "Product not found"}
    return {"status": 200, "message": "Product retrieved", "data": products_db[product_id]}

show_product = showProduct

def createProduct(data):
    payload = _extract_payload(data)

    new_id = payload.get("product_id") or f"P{len(products_db)+1:03d}"
    product = {
        "product_id": new_id,
        "product_name": payload.get("product_name"),
        "price_per_unit": float(payload.get("price_per_unit", 0.0)),
        "description": payload.get("description", ""),
        "stock_available": int(payload.get("stock_available", 0))
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

create_product = createProduct

def updateProduct(product_id, data=None):
    if data is None and hasattr(product_id, 'params'):
        req = product_id
        product_id = req.params.get("product_id", "")
        data = req

    if not isinstance(product_id, str):
        product_id = getattr(product_id, 'params', {}).get("product_id", "")

    payload = _extract_payload(data)
    if product_id not in products_db:
        return {"status": 404, "error": "Not Found", "message": "Product not found"}
    for k, v in payload.items():
        if k != "product_id":
            products_db[product_id][k] = v
    return {"status": 200, "message": "Product updated", "data": products_db[product_id]}

update_product = updateProduct

def deleteProduct(product_id):
    if not isinstance(product_id, str):
        product_id = getattr(product_id, 'params', {}).get("product_id", "")
    if product_id not in products_db:
        return {"status": 404, "error": "Not Found", "message": "Product not found"}
    deleted = products_db.pop(product_id)
    return {"status": 200, "message": "Product deleted", "data": deleted}

delete_product = deleteProduct