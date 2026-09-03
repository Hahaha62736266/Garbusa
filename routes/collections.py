def createCollection(request):
    data = request.body or {}   # ← YOUR EXISTING LINE
                                #
    # ==================================================
    # ✅ PASTE EVERYTHING BELOW THIS LINE ↓
    # ==================================================

    # 🔒 GUARD CLAUSES — Validation checks FIRST
    import re

    # Check collection_id
    if not data.get("collection_id"):
        return {"status": 422, "error": "collection_id is required", "field": "collection_id"}
    if not re.match(r"^CL\d{3}$", data["collection_id"]):
        return {"status": 422, "error": "collection_id must be CL followed by 3 digits (e.g. CL001)", "field": "collection_id"}

    # Check customer_id
    if not data.get("customer_id"):
        return {"status": 422, "error": "customer_id is required", "field": "customer_id"}
    if not re.match(r"^C\d{3}$", data["customer_id"]):
        return {"status": 422, "error": "customer_id must be C followed by 3 digits (e.g. C001)", "field": "customer_id"}

    # Check order_id (optional)
    if data.get("order_id") and not re.match(r"^O\d{3}$", data["order_id"]):
        return {"status": 422, "error": "order_id must be O followed by 3 digits (e.g. O001)", "field": "order_id"}

    # Check empty_jugs_returned
    if "empty_jugs_returned" not in data:
        return {"status": 422, "error": "empty_jugs_returned is required", "field": "empty_jugs_returned"}
    if not isinstance(data["empty_jugs_returned"], int) or data["empty_jugs_returned"] < 0:
        return {"status": 422, "error": "empty_jugs_returned must be a non-negative integer", "field": "empty_jugs_returned"}

    # Check filled_jugs_released
    if "filled_jugs_released" not in data:
        return {"status": 422, "error": "filled_jugs_released is required", "field": "filled_jugs_released"}
    if not isinstance(data["filled_jugs_released"], int) or data["filled_jugs_released"] < 0:
        return {"status": 422, "error": "filled_jugs_released must be a non-negative integer", "field": "filled_jugs_released"}

    # Check container_balance
    if "container_balance" not in data:
        return {"status": 422, "error": "container_balance is required", "field": "container_balance"}
    if not isinstance(data["container_balance"], int) or data["container_balance"] < 0:
        return {"status": 422, "error": "container_balance must be a non-negative integer", "field": "container_balance"}

    # Check collected_by
    if not data.get("collected_by") or len(data["collected_by"]) < 2:
        return {"status": 422, "error": "collected_by is required (min 2 characters)", "field": "collected_by"}

    # ✅ ALL VALIDATION PASSED — your existing code below runs now


def updateCollection(request):
    data = request.body or {}
    collection_id = request.params.get("collection_id", "")  # ← from URL
                                                             #
    # ==================================================
    # ✅ PASTE EVERYTHING BELOW THIS LINE ↓
    # ==================================================

    # 🔒 GUARD CLAUSES — Validation checks FIRST
    import re

    # Validate URL collection_id FIRST
    if not re.match(r"^CL\d{3}$", collection_id):
        return {"status": 422, "error": "collection_id must be CL followed by 3 digits (e.g. CL001)", "field": "collection_id"}

    # Validate customer_id IF provided
    if "customer_id" in data:
        if not re.match(r"^C\d{3}$", data["customer_id"]):
            return {"status": 422, "error": "customer_id must be C followed by 3 digits (e.g. C001)", "field": "customer_id"}

    # Validate order_id IF provided
    if "order_id" in data and not re.match(r"^O\d{3}$", data["order_id"]):
        return {"status": 422, "error": "order_id must be O followed by 3 digits (e.g. O001)", "field": "order_id"}

    # Validate empty_jugs_returned IF provided
    if "empty_jugs_returned" in data:
        if not isinstance(data["empty_jugs_returned"], int) or data["empty_jugs_returned"] < 0:
            return {"status": 422, "error": "empty_jugs_returned must be a non-negative integer", "field": "empty_jugs_returned"}

    # Validate filled_jugs_released IF provided
    if "filled_jugs_released" in data:
        if not isinstance(data["filled_jugs_released"], int) or data["filled_jugs_released"] < 0:
            return {"status": 422, "error": "filled_jugs_released must be a non-negative integer", "field": "filled_jugs_released"}

    # Validate container_balance IF provided
    if "container_balance" in data:
        if not isinstance(data["container_balance"], int) or data["container_balance"] < 0:
            return {"status": 422, "error": "container_balance must be a non-negative integer", "field": "container_balance"}

    # Validate collected_by IF provided
    if "collected_by" in data and len(data["collected_by"]) < 2:
        return {"status": 422, "error": "collected_by must be at least 2 characters", "field": "collected_by"}

    # ✅ ALL VALIDATION PASSED — your existing code below runs now

# ==========================================================
# ROUTES: Collections
# Pipeline: Validation → Controller
# ==========================================================

from middleware.validation import (
    validateCollectionCreate,
    validateCollectionUpdate
)
from controllers.collection_controller import (
    listCollections,
    showCollection,
    createCollection,
    updateCollection,
    deleteCollection
)

def GET_collections(request):
    """GET /collections — List all"""
    return listCollections(request)

def GET_collection_by_id(request):
    """GET /collections/:collection_id — Show one"""
    return showCollection(request)

def POST_collections(request):
    """POST /collections — Create"""
    error = validateCollectionCreate(request)
    if error:
        return error
    return createCollection(request)

def PUT_collection_by_id(request):
    """PUT /collections/:collection_id — Update"""
    error = validateCollectionUpdate(request)
    if error:
        return error
    return updateCollection(request)

def DELETE_collection_by_id(request):
    """DELETE /collections/:collection_id — Delete (stub; add auth later)"""
    return deleteCollection(request)
