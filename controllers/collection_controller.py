# OWNER: Apostol
def listCollections(request):
    return {"status":200,"data":{"message":"listCollections stub"},"error":None}

def showCollection(request):
    clid = request.params.get("collection_id")
    return {"status":200,"data":{"message":"showCollection stub","collection_id":clid},"error":None}

def createCollection(request):
    return {"status":201,"data":{"message":"createCollection stub"},"error":None}

def updateCollection(request):
    clid = request.params.get("collection_id")
    return {"status":200,"data":{"message":"updateCollection stub","collection_id":clid},"error":None}

def deleteCollection(request):
    clid = request.params.get("collection_id")
    return {"status":200,"data":{"message":"deleteCollection stub","collection_id":clid},"error":None}

# OWNER: Apostol
def createCollection(request):
    data = request.body or {}

    # GUARD CLAUSES
    if not data.get("collection_id"):
        return {"status": 422, "data": None, "error": "collection_id is required"}
    if not re.match(r"^CL\d{3}$", data["collection_id"]):
        return {"status": 422, "data": None, "error": "collection_id must be CL followed by 3 digits (e.g. CL001)"}

    if not data.get("customer_id"):
        return {"status": 422, "data": None, "error": "customer_id is required"}
    if not re.match(r"^C\d{3}$", data["customer_id"]):
        return {"status": 422, "data": None, "error": "customer_id must use format C###"}

    if data.get("order_id") and not re.match(r"^O\d{3}$", data["order_id"]):
        return {"status": 422, "data": None, "error": "order_id must use format O###"}

    if "empty_jugs_returned" not in data:
        return {"status": 422, "data": None, "error": "empty_jugs_returned is required"}
    if not isinstance(data["empty_jugs_returned"], int) or data["empty_jugs_returned"] < 0:
        return {"status": 422, "data": None, "error": "empty_jugs_returned must be a non-negative integer"}

    if "filled_jugs_released" not in data:
        return {"status": 422, "data": None, "error": "filled_jugs_released is required"}
    if not isinstance(data["filled_jugs_released"], int) or data["filled_jugs_released"] < 0:
        return {"status": 422, "data": None, "error": "filled_jugs_released must be a non-negative integer"}

    if "container_balance" not in data:
        return {"status": 422, "data": None, "error": "container_balance is required"}
    if not isinstance(data["container_balance"], int) or data["container_balance"] < 0:
        return {"status": 422, "data": None, "error": "container_balance must be a non-negative integer"}

    if not data.get("collected_by") or len(data["collected_by"]) < 2:
        return {"status": 422, "data": None, "error": "collected_by is required (min 2 characters)"}

    # ✅ ALL VALID — Proceed to create
    return {"status": 201, "data": {"message": "createCollection stub"}, "error": None}
