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

# OWNER: Apostol
def updateCollection(request):
    collection_id = request.params.get("collection_id")
    data = request.body or {}

    # GUARD CLAUSES
    if not re.match(r"^CL\d{3}$", collection_id or ""):
        return {"status": 422, "data": None, "error": "collection_id must be CL followed by 3 digits"}

    if "customer_id" in data and not re.match(r"^C\d{3}$", data["customer_id"]):
        return {"status": 422, "data": None, "error": "customer_id must use format C###"}

    if "order_id" in data and not re.match(r"^O\d{3}$", data["order_id"]):
        return {"status": 422, "data": None, "error": "order_id must use format O###"}

    if "empty_jugs_returned" in data:
        if not isinstance(data["empty_jugs_returned"], int) or data["empty_jugs_returned"] < 0:
            return {"status": 422, "data": None, "error": "empty_jugs_returned must be a non-negative integer"}

    if "filled_jugs_released" in data:
        if not isinstance(data["filled_jugs_released"], int) or data["filled_jugs_released"] < 0:
            return {"status": 422, "data": None, "error": "filled_jugs_released must be a non-negative integer"}

    if "container_balance" in data:
        if not isinstance(data["container_balance"], int) or data["container_balance"] < 0:
            return {"status": 422, "data": None, "error": "container_balance must be a non-negative integer"}

    if "collected_by" in data and len(data["collected_by"]) < 2:
        return {"status": 422, "data": None, "error": "collected_by must be at least 2 characters"}

    # ✅ ALL VALID — Proceed to update
    return {"status": 200, "data": {"message": "updateCollection stub", "collection_id": collection_id}, "error": None}

# OWNER: Apostol
# THIN CONTROLLER — Only orchestrate, never validate or query directly

from models.collection_model import Collection

def listCollections(request):
    collections = Collection.all()
    return {"status": 200, "data": collections, "error": None}

def showCollection(request):
    clid = request.params.get("collection_id")
    collection = Collection.find(clid)
    return {"status": 200, "data": collection, "error": None}

def createCollection(request):
    data = request.validatedBody           # ✅ Passed validation middleware
    collection = Collection.save(data)
    return {"status": 201, "data": collection, "error": None}

def updateCollection(request):
    clid = request.params.get("collection_id")
    data = request.validatedBody
    collection = Collection.update(clid, data)
    return {"status": 200, "data": collection, "error": None}

def deleteCollection(request):
    clid = request.params.get("collection_id")
    Collection.remove(clid)
    return {"status": 200, "data": {"deleted_id": clid}, "error": None}
    
