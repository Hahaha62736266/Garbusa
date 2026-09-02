# OWNER: Obiasad
def listProducts(request):
    return {"status":200,"data":{"message":"listProducts stub"},"error":None}

def showProduct(request):
    pid = request.params.get("product_id")
    return {"status":200,"data":{"message":"showProduct stub","product_id":pid},"error":None}

def createProduct(request):
    return {"status":201,"data":{"message":"createProduct stub"},"error":None}

def updateProduct(request):
    pid = request.params.get("product_id")
    return {"status":200,"data":{"message":"updateProduct stub","product_id":pid},"error":None}

def deleteProduct(request):
    pid = request.params.get("product_id")
    return {"status":200,"data":{"message":"deleteProduct stub","product_id":pid},"error":None}

# OWNER: Obiasad
def createProduct(request):
    data = request.body or {}

    # GUARD CLAUSES
    if not data.get("product_id"):
        return {"status": 422, "data": None, "error": "product_id is required"}
    if not re.match(r"^P\d{3}$", data["product_id"]):
        return {"status": 422, "data": None, "error": "product_id must be P followed by 3 digits (e.g. P001)"}

    if not data.get("product_name"):
        return {"status": 422, "data": None, "error": "product_name is required"}
    if not isinstance(data["product_name"], str) or not (2 <= len(data["product_name"]) <= 100):
        return {"status": 422, "data": None, "error": "product_name must be 2–100 characters"}

    if "price_per_unit" not in data:
        return {"status": 422, "data": None, "error": "price_per_unit is required"}
    try:
        price = float(data["price_per_unit"])
        if price < 0.00:
            return {"status": 422, "data": None, "error": "price_per_unit must be ≥ 0.00"}
    except (TypeError, ValueError):
        return {"status": 422, "data": None, "error": "price_per_unit must be a valid number"}

    if "stock_available" not in data:
        return {"status": 422, "data": None, "error": "stock_available is required"}
    if not isinstance(data["stock_available"], int) or data["stock_available"] < 0:
        return {"status": 422, "data": None, "error": "stock_available must be a non-negative integer"}

    # ✅ ALL VALID — Proceed to create
    return {"status": 201, "data": {"message": "createProduct stub"}, "error": None}
