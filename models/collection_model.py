# ==========================================================
# DATA LAYER: Collection Model
# ==========================================================

_collections = {}
_next_id = 1

def all():
    return list(_collections.values())

def find(collection_id):
    return _collections.get(collection_id)

def save(data):
    global _next_id
    record = {
        "id": _next_id,
        "collection_id": data.get("collection_id"),
        "customer_id": data.get("customer_id"),
        "order_id": data.get("order_id"),
        "empty_jugs_returned": data.get("empty_jugs_returned", 0),
        "filled_jugs_released": data.get("filled_jugs_released", 0),
        "container_balance": data.get("container_balance", 0),
        "collected_by": data.get("collected_by")
    }
    _collections[data["collection_id"]] = record
    _next_id += 1
    return record

def update(collection_id, data):
    record = _collections.get(collection_id)
    if not record:
        return None
    if "customer_id" in data: record["customer_id"] = data["customer_id"]
    if "order_id" in data: record["order_id"] = data["order_id"]
    if "empty_jugs_returned" in data: record["empty_jugs_returned"] = data["empty_jugs_returned"]
    if "filled_jugs_released" in data: record["filled_jugs_released"] = data["filled_jugs_released"]
    if "container_balance" in data: record["container_balance"] = data["container_balance"]
    if "collected_by" in data: record["collected_by"] = data["collected_by"]
    return record

def remove(collection_id):
    if collection_id in _collections:
        del _collections[collection_id]
        return True
    return False
