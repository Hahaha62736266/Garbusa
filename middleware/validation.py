import re

# ==========================================================
# VALIDATION MIDDLEWARE
# Purpose: Run ALL guard clauses BEFORE controllers
# Returns 422 immediately if invalid → never reaches controller
# Attaches clean data to: request.validatedBody
# ==========================================================

# ----------------------------------------------------------
# CUSTOMERS Validation
# ----------------------------------------------------------
def validateCustomerCreate(request):
    """Validate POST /customers — returns error dict OR None if OK"""
    data = request.body or {}

    if not data.get("customer_id"):
        return {"status": 422, "error": "customer_id is required", "field": "customer_id"}
    if not re.match(r"^C\d{3}$", data["customer_id"]):
        return {"status": 422, "error": "customer_id must be C followed by 3 digits", "field": "customer_id"}

    if not data.get("full_name"):
        return {"status": 422, "error": "full_name is required", "field": "full_name"}
    if not isinstance(data["full_name"], str) or not (2 <= len(data["full_name"]) <= 100):
        return {"status": 422, "error": "full_name must be 2–100 characters", "field": "full_name"}

    if not data.get("contact_number"):
        return {"status": 422, "error": "contact_number is required", "field": "contact_number"}
    if not re.match(r"^09\d{2}-\d{3}-\d{4}$", data["contact_number"]):
        return {"status": 422, "error": "contact_number must use format 09XX-XXX-XXXX", "field": "contact_number"}

    if not data.get("address") or len(data["address"]) < 5:
        return {"status": 422, "error": "address is required (min 5 characters)", "field": "address"}

    if "container_owned" not in data:
        return {"status": 422, "error": "container_owned is required", "field": "container_owned"}
    if not isinstance(data["container_owned"], int) or data["container_owned"] < 0:
        return {"status": 422, "error": "container_owned must be a non-negative integer", "field": "container_owned"}

    # ✅ ALL VALID — attach clean data to request
    request.validatedBody = data
    return None


def validateCustomerUpdate(request):
    """Validate PUT /customers/:customer_id — returns error dict OR None if OK"""
    data = request.body or {}
    customer_id = request.params.get("customer_id", "")

    if not re.match(r"^C\d{3}$", customer_id):
        return {"status": 422, "error": "customer_id must be C followed by 3 digits", "field": "customer_id"}

    if "full_name" in data:
        if not isinstance(data["full_name"], str) or not (2 <= len(data["full_name"]) <= 100):
            return {"status": 422, "error": "full_name must be 2–100 characters", "field": "full_name"}

    if "contact_number" in data:
        if not re.match(r"^09\d{2}-\d{3}-\d{4}$", data["contact_number"]):
            return {"status": 422, "error": "contact_number must use format 09XX-XXX-XXXX", "field": "contact_number"}

    if "address" in data and len(data["address"]) < 5:
        return {"status": 422, "error": "address must be at least 5 characters", "field": "address"}

    if "container_owned" in data:
        if not isinstance(data["container_owned"], int) or data["container_owned"] < 0:
            return {"status": 422, "error": "container_owned must be a non-negative integer", "field": "container_owned"}

    # ✅ ALL VALID
    request.validatedBody = data
    return None

# ----------------------------------------------------------
# PRODUCTS Validation
# ----------------------------------------------------------
def validateProductCreate(request):
    """Validate POST /products"""
    data = request.body or {}

    if not data.get("product_id"):
        return {"status": 422, "error": "product_id is required", "field": "product_id"}
    if not re.match(r"^P\d{3}$", data["product_id"]):
        return {"status": 422, "error": "product_id must be P followed by 3 digits", "field": "product_id"}

    if not data.get("product_name"):
        return {"status": 422, "error": "product_name is required", "field": "product_name"}
    if not isinstance(data["product_name"], str) or not (2 <= len(data["product_name"]) <= 100):
        return {"status": 422, "error": "product_name must be 2–100 characters", "field": "product_name"}

    if "price_per_unit" not in data:
        return {"status": 422, "error": "price_per_unit is required", "field": "price_per_unit"}
    try:
        price = float(data["price_per_unit"])
        if price < 0.00:
            return {"status": 422, "error": "price_per_unit must be ≥ 0.00", "field": "price_per_unit"}
    except (TypeError, ValueError):
        return {"status": 422, "error": "price_per_unit must be a valid number", "field": "price_per_unit"}

    if "stock_available" not in data:
        return {"status": 422, "error": "stock_available is required", "field": "stock_available"}
    if not isinstance(data["stock_available"], int) or data["stock_available"] < 0:
        return {"status": 422, "error": "stock_available must be a non-negative integer", "field": "stock_available"}

    # ✅ ALL VALID
    request.validatedBody = data
    return None


def validateProductUpdate(request):
    """Validate PUT /products/:product_id"""
    data = request.body or {}
    product_id = request.params.get("product_id", "")

    if not re.match(r"^P\d{3}$", product_id):
        return {"status": 422, "error": "product_id must be P followed by 3 digits", "field": "product_id"}

    if "product_name" in data:
        if not isinstance(data["product_name"], str) or not (2 <= len(data["product_name"]) <= 100):
            return {"status": 422, "error": "product_name must be 2–100 characters", "field": "product_name"}

    if "price_per_unit" in data:
        try:
            price = float(data["price_per_unit"])
            if price < 0.00:
                return {"status": 422, "error": "price_per_unit must be ≥ 0.00", "field": "price_per_unit"}
        except (TypeError, ValueError):
            return {"status": 422, "error": "price_per_unit must be a valid number", "field": "price_per_unit"}

    if "stock_available" in data:
        if not isinstance(data["stock_available"], int) or data["stock_available"] < 0:
            return {"status": 422, "error": "stock_available must be a non-negative integer", "field": "stock_available"}

    # ✅ ALL VALID
    request.validatedBody = data
    return None

# ----------------------------------------------------------
# ORDERS Validation
# ----------------------------------------------------------
ALLOWED_ORDER_STATUSES = {"Pending", "Delivered"}

def validateOrderCreate(request):
    """Validate POST /orders"""
    data = request.body or {}

    if not data.get("order_id"):
        return {"status": 422, "error": "order_id is required", "field": "order_id"}
    if not re.match(r"^O\d{3}$", data["order_id"]):
        return {"status": 422, "error": "order_id must be O followed by 3 digits", "field": "order_id"}

    if not data.get("customer_id"):
        return {"status": 422, "error": "customer_id is required", "field": "customer_id"}
    if not re.match(r"^C\d{3}$", data["customer_id"]):
        return {"status": 422, "error": "customer_id must use format C###", "field": "customer_id"}

    if not data.get("product_id"):
        return {"status": 422, "error": "product_id is required", "field": "product_id"}
    if not re.match(r"^P\d{3}$", data["product_id"]):
        return {"status": 422, "error": "product_id must use format P###", "field": "product_id"}

    if "quantity" not in data:
        return {"status": 422, "error": "quantity is required", "field": "quantity"}
    if not isinstance(data["quantity"], int) or not (1 <= data["quantity"] <= 999):
        return {"status": 422, "error": "quantity must be an integer between 1 and 999", "field": "quantity"}

    if not data.get("status"):
        return {"status": 422, "error": "status is required", "field": "status"}
    if data["status"] not in ALLOWED_ORDER_STATUSES:
        return {"status": 422, "error": f"status must be one of: {', '.join(ALLOWED_ORDER_STATUSES)}", "field": "status"}

    # ✅ ALL VALID
    request.validatedBody = data
    return None


def validateOrderUpdate(request):
    """Validate PUT /orders/:order_id"""
    data = request.body or {}
    order_id = request.params.get("order_id", "")

    if not re.match(r"^O\d{3}$", order_id):
        return {"status": 422, "error": "order_id must be O followed by 3 digits", "field": "order_id"}

    if "customer_id" in data and not re.match(r"^C\d{3}$", data["customer_id"]):
        return {"status": 422, "error": "customer_id must use format C###", "field": "customer_id"}

    if "product_id" in data and not re.match(r"^P\d{3}$", data["product_id"]):
        return {"status": 422, "error": "product_id must use format P###", "field": "product_id"}

    if "quantity" in data:
        if not isinstance(data["quantity"], int) or not (1 <= data["quantity"] <= 999):
            return {"status": 422, "error": "quantity must be an integer between 1 and 999", "field": "quantity"}

    if "status" in data and data["status"] not in ALLOWED_ORDER_STATUSES:
        return {"status": 422, "error": f"status must be one of: {', '.join(ALLOWED_ORDER_STATUSES)}", "field": "status"}

    # ✅ ALL VALID
    request.validatedBody = data
    return None

# ----------------------------------------------------------
# COLLECTIONS Validation
# ----------------------------------------------------------
def validateCollectionCreate(request):
    """Validate POST /collections"""
    data = request.body or {}

    if not data.get("collection_id"):
        return {"status": 422, "error": "collection_id is required", "field": "collection_id"}
    if not re.match(r"^CL\d{3}$", data["collection_id"]):
        return {"status": 422, "error": "collection_id must be CL followed by 3 digits", "field": "collection_id"}

    if not data.get("customer_id"):
        return {"status": 422, "error": "customer_id is required", "field": "customer_id"}
    if not re.match(r"^C\d{3}$", data["customer_id"]):
        return {"status": 422, "error": "customer_id must use format C###", "field": "customer_id"}

    if data.get("order_id") and not re.match(r"^O\d{3}$", data["order_id"]):
        return {"status": 422, "error": "order_id must use format O###", "field": "order_id"}

    if "empty_jugs_returned" not in data:
        return {"status": 422, "error": "empty_jugs_returned is required", "field": "empty_jugs_returned"}
    if not isinstance(data["empty_jugs_returned"], int) or data["empty_jugs_returned"] < 0:
        return {"status": 422, "error": "empty_jugs_returned must be a non-negative integer", "field": "empty_jugs_returned"}

    if "filled_jugs_released" not in data:
        return {"status": 422, "error": "filled_jugs_released is required", "field": "filled_jugs_released"}
    if not isinstance(data["filled_jugs_released"], int) or data["filled_jugs_released"] < 0:
        return {"status": 422, "error": "filled_jugs_released must be a non-negative integer", "field": "filled_jugs_released"}

    if "container_balance" not in data:
        return {"status": 422, "error": "container_balance is required", "field": "container_balance"}
    if not isinstance(data["container_balance"], int) or data["container_balance"] < 0:
        return {"status": 422, "error": "container_balance must be a non-negative integer", "field": "container_balance"}

    if not data.get("collected_by") or len(data["collected_by"]) < 2:
        return {"status": 422, "error": "collected_by is required (min 2 characters)", "field": "collected_by"}

    # ✅ ALL VALID
    request.validatedBody = data
    return None


def validateCollectionUpdate(request):
    """Validate PUT /collections/:collection_id"""
    data = request.body or {}
    collection_id = request.params.get("collection_id", "")

    if not re.match(r"^CL\d{3}$", collection_id):
        return {"status": 422, "error": "collection_id must be CL followed by 3 digits", "field": "collection_id"}

    if "customer_id" in data and not re.match(r"^C\d{3}$", data["customer_id"]):
        return {"status": 422, "error": "customer_id must use format C###", "field": "customer_id"}

    if "order_id" in data and not re.match(r"^O\d{3}$", data["order_id"]):
        return {"status": 422, "error": "order_id must use format O###", "field": "order_id"}

    if "empty_jugs_returned" in data:
        if not isinstance(data["empty_jugs_returned"], int) or data["empty_jugs_returned"] < 0:
            return {"status": 422, "error": "empty_jugs_returned must be a non-negative integer", "field": "empty_jugs_returned"}

    if "filled_jugs_released" in data:
        if not isinstance(data["filled_jugs_released"], int) or data["filled_jugs_released"] < 0:
            return {"status": 422, "error": "filled_jugs_released must be a non-negative integer", "field": "filled_jugs_released"}

    if "container_balance" in data:
        if not isinstance(data["container_balance"], int) or data["container_balance"] < 0:
            return {"status": 422, "error": "container_balance must be a non-negative integer", "field": "container_balance"}

    if "collected_by" in data and len(data["collected_by"]) < 2:
        return {"status": 422, "error": "collected_by must be at least 2 characters", "field": "collected_by"}

    # ✅ ALL VALID
    request.validatedBody = data
    return None


# ==========================================================
# AUTHORIZATION GUARD — Permission Checks
# Returns 403 if user is NOT ALLOWED (distinct from 422)
# ==========================================================

def checkOwnership(request, recordOwnerId):
    """
    Simple permission check:
    Current logged-in user must match the record owner ID.
    Return None if allowed, or 403 error dict if forbidden.
    """
    currentUserId = request.auth.get("user_id") if request.auth else None

    if not currentUserId:
        return {
            "status": 403,
            "error": "Not authenticated — permission denied",
            "field": None
        }

    if str(currentUserId) != str(recordOwnerId):
        return {
            "status": 403,
            "error": "Forbidden: you do not own this record",
            "field": None
        }

    return None


# ----------------------------------------------------------
# AUTHORIZATION MIDDLEWARE — Apply to Sensitive Actions
# ----------------------------------------------------------

def authorizeDeleteCustomer(request):
    """DELETE /customers/:customer_id — Only the owner can delete"""
    from models.customer_model import Customer
    customerId = request.params.get("customer_id")
    existing = Customer.find(customerId)

    if not existing:
        return {"status": 404, "error": "Record not found", "field": None}

    ownerId = existing.get("owned_by_user_id", "admin")
    return checkOwnership(request, ownerId)


def authorizeDeleteOrder(request):
    """DELETE /orders/:order_id — Only the customer who placed it can delete"""
    from models import order_model
    orderId = request.params.get("order_id")
    existing = Order.find(orderId)

    if not existing:
        return {"status": 404, "error": "Record not found", "field": None}

    ownerId = existing.get("customer_id")
    return checkOwnership(request, ownerId)
    
