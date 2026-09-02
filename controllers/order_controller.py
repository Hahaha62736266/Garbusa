# OWNER: Taylaran
def listOrders(request):
    return {"status":200,"data":{"message":"listOrders stub"},"error":None}

def showOrder(request):
    oid = request.params.get("order_id")
    return {"status":200,"data":{"message":"showOrder stub","order_id":oid},"error":None}

def createOrder(request):
    return {"status":201,"data":{"message":"createOrder stub"},"error":None}

def updateOrder(request):
    oid = request.params.get("order_id")
    return {"status":200,"data":{"message":"updateOrder stub","order_id":oid},"error":None}

def deleteOrder(request):
    oid = request.params.get("order_id")
    return {"status":200,"data":{"message":"deleteOrder stub","order_id":oid},"error":None}


# OWNER: Taylaran
def createOrder(request):
    data = request.body or {}
    ALLOWED_STATUSES = {"Pending", "Delivered"}

    # GUARD CLAUSES
    if not data.get("order_id"):
        return {"status": 422, "data": None, "error": "order_id is required"}
    if not re.match(r"^O\d{3}$", data["order_id"]):
        return {"status": 422, "data": None, "error": "order_id must be O followed by 3 digits (e.g. O001)"}

    if not data.get("customer_id"):
        return {"status": 422, "data": None, "error": "customer_id is required"}
    if not re.match(r"^C\d{3}$", data["customer_id"]):
        return {"status": 422, "data": None, "error": "customer_id must use format C###"}

    if not data.get("product_id"):
        return {"status": 422, "data": None, "error": "product_id is required"}
    if not re.match(r"^P\d{3}$", data["product_id"]):
        return {"status": 422, "data": None, "error": "product_id must use format P###"}

    if "quantity" not in data:
        return {"status": 422, "data": None, "error": "quantity is required"}
    if not isinstance(data["quantity"], int) or not (1 <= data["quantity"] <= 999):
        return {"status": 422, "data": None, "error": "quantity must be an integer between 1 and 999"}

    if not data.get("status"):
        return {"status": 422, "data": None, "error": "status is required"}
    if data["status"] not in ALLOWED_STATUSES:
        return {"status": 422, "data": None, "error": f"status must be one of: {', '.join(ALLOWED_STATUSES)}"}

    # ✅ ALL VALID — Proceed to create
    return {"status": 201, "data": {"message": "createOrder stub"}, "error": None}


# OWNER: Taylaran
def updateOrder(request):
    order_id = request.params.get("order_id")
    data = request.body or {}
    ALLOWED_STATUSES = {"Pending", "Delivered"}

    # GUARD CLAUSES
    if not re.match(r"^O\d{3}$", order_id or ""):
        return {"status": 422, "data": None, "error": "order_id must be O followed by 3 digits"}

    if "customer_id" in data and not re.match(r"^C\d{3}$", data["customer_id"]):
        return {"status": 422, "data": None, "error": "customer_id must use format C###"}

    if "product_id" in data and not re.match(r"^P\d{3}$", data["product_id"]):
        return {"status": 422, "data": None, "error": "product_id must use format P###"}

    if "quantity" in data:
        if not isinstance(data["quantity"], int) or not (1 <= data["quantity"] <= 999):
            return {"status": 422, "data": None, "error": "quantity must be an integer between 1 and 999"}

    if "status" in data and data["status"] not in ALLOWED_STATUSES:
        return {"status": 422, "data": None, "error": f"status must be one of: {', '.join(ALLOWED_STATUSES)}"}

    # ✅ ALL VALID — Proceed to update
    return {"status": 200, "data": {"message": "updateOrder stub", "order_id": order_id}, "error": None}
