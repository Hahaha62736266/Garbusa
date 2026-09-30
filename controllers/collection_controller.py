"""Collection Controller — MockRequest compatible"""
from datetime import date

collections_db = {}

def listCollections():
    return {
        "status": 200,
        "message": "Collections retrieved successfully",
        "data": list(collections_db.values())
    }

def showCollection(collection_id):
    if collection_id not in collections_db:
        return {"status": 404, "error": "Not Found", "message": "Collection not found"}
    return {"status": 200, "message": "Collection retrieved", "data": collections_db[collection_id]}

def createCollection(data):
    if hasattr(data, 'json') and data.json is not None:
        payload = data.json
    else:
        payload = {
            "customer_id": getattr(data, "customer_id", None),
            "order_id": getattr(data, "order_id", None),
            "empty_jugs_returned": getattr(data, "empty_jugs_returned", 0),
            "filled_jugs_released": getattr(data, "filled_jugs_released", 0),
            "container_balance": getattr(data, "container_balance", 0),
            "collected_by": getattr(data, "collected_by", "Staff")
        }

    new_id = f"CL{len(collections_db)+1:03d}"
    # ✅ SAVE to variable 'collection'
    collection = {
        "collection_id": new_id,
        "customer_id": payload.get("customer_id"),
        "order_id": payload.get("order_id"),
        "empty_jugs_returned": payload.get("empty_jugs_returned", 0),
        "filled_jugs_released": payload.get("filled_jugs_released", 0),
        "container_balance": payload.get("container_balance", 0),
        "collected_by": payload.get("collected_by", "Staff")
    }
    collections_db[new_id] = collection

    return {
        "status": 201,
        "message": "Collection created",
        "data": {
            "id": len(collections_db),
            "collection_id": new_id,
            "customer_id": collection["customer_id"],
            "order_id": collection["order_id"],
            "empty_jugs_returned": collection["empty_jugs_returned"],
            "filled_jugs_released": collection["filled_jugs_released"],
            "container_balance": collection["container_balance"]
        }
    }

def updateCollection(collection_id, data):
    if hasattr(data, 'json'):
        payload = data.json
    else:
        payload = data
    if collection_id not in collections_db:
        return {"status": 404, "error": "Not Found", "message": "Collection not found"}
    for k, v in payload.items():
        if k != "collection_id":
            collections_db[collection_id][k] = v
    return {"status": 200, "message": "Collection updated", "data": collections_db[collection_id]}

def deleteCollection(collection_id):
    if collection_id not in collections_db:
        return {"status": 404, "error": "Not Found", "message": "Collection not found"}
    deleted = collections_db.pop(collection_id)
    return {"status": 200, "message": "Collection deleted", "data": deleted}