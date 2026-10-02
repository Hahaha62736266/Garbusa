"""Collection Controller — MockRequest compatible"""
from datetime import date

collections_db = {}

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

def listCollections(request=None):
    return {
        "status": 200,
        "message": "Collections retrieved successfully",
        "data": list(collections_db.values())
    }

list_collections = listCollections

def showCollection(collection_id):
    if not isinstance(collection_id, str):
        collection_id = getattr(collection_id, 'params', {}).get("collection_id", "")
    if collection_id not in collections_db:
        return {"status": 404, "error": "Not Found", "message": "Collection not found"}
    return {"status": 200, "message": "Collection retrieved", "data": collections_db[collection_id]}

show_collection = showCollection

def createCollection(data):
    payload = _extract_payload(data)

    new_id = payload.get("collection_id") or f"CL{len(collections_db)+1:03d}"
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

create_collection = createCollection

def updateCollection(collection_id, data=None):
    if data is None and hasattr(collection_id, 'params'):
        req = collection_id
        collection_id = req.params.get("collection_id", "")
        data = req

    if not isinstance(collection_id, str):
        collection_id = getattr(collection_id, 'params', {}).get("collection_id", "")

    payload = _extract_payload(data)
    if collection_id not in collections_db:
        return {"status": 404, "error": "Not Found", "message": "Collection not found"}
    for k, v in payload.items():
        if k != "collection_id":
            collections_db[collection_id][k] = v
    return {"status": 200, "message": "Collection updated", "data": collections_db[collection_id]}

update_collection = updateCollection

def deleteCollection(collection_id):
    if not isinstance(collection_id, str):
        collection_id = getattr(collection_id, 'params', {}).get("collection_id", "")
    if collection_id not in collections_db:
        return {"status": 404, "error": "Not Found", "message": "Collection not found"}
    deleted = collections_db.pop(collection_id)
    return {"status": 200, "message": "Collection deleted", "data": deleted}

delete_collection = deleteCollection