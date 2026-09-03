def createProduct(request):
    data = request.body or {}   # ← YOUR EXISTING LINE
                                #
    # ==================================================
    # ✅ PASTE EVERYTHING BELOW THIS LINE ↓
    # ==================================================

    # 🔒 GUARD CLAUSES — Validation checks FIRST
    import re

    # Check product_id
    if not data.get("product_id"):
        return {"status": 422, "error": "product_id is required", "field": "product_id"}
    if not re.match(r"^P\d{3}$", data["product_id"]):
        return {"status": 422, "error": "product_id must be P followed by 3 digits (e.g. P001)", "field": "product_id"}

    # Check product_name
    if not data.get("product_name"):
        return {"status": 422, "error": "product_name is required", "field": "product_name"}
    if not isinstance(data["product_name"], str) or len(data["product_name"]) < 2 or len(data["product_name"]) > 100:
        return {"status": 422, "error": "product_name must be 2–100 characters", "field": "product_name"}

    # Check price_per_unit
    if "price_per_unit" not in data:
        return {"status": 422, "error": "price_per_unit is required", "field": "price_per_unit"}
    try:
        price = float(data["price_per_unit"])
        if price < 0.00:
            return {"status": 422, "error": "price_per_unit must be ≥ 0.00", "field": "price_per_unit"}
    except (TypeError, ValueError):
        return {"status": 422, "error": "price_per_unit must be a valid number", "field": "price_per_unit"}

    # Check stock_available
    if "stock_available" not in data:
        return {"status": 422, "error": "stock_available is required", "field": "stock_available"}
    if not isinstance(data["stock_available"], int) or data["stock_available"] < 0:
        return {"status": 422, "error": "stock_available must be a non-negative integer", "field": "stock_available"}

    # ✅ ALL VALIDATION PASSED — your existing code below runs now

# ==========================================================
# ROUTES: Products
# Pipeline: Validation → Controller
# ==========================================================

from middleware.validation import (
    validateProductCreate,
    validateProductUpdate
)
from controllers.product_controller import (
    listProducts,
    showProduct,
    createProduct,
    updateProduct,
    deleteProduct
)

def GET_products(request):
    """GET /products — List all"""
    return listProducts(request)

def GET_product_by_id(request):
    """GET /products/:product_id — Show one"""
    return showProduct(request)

def POST_products(request):
    """POST /products — Create"""
    error = validateProductCreate(request)
    if error:
        return error
    return createProduct(request)

def PUT_product_by_id(request):
    """PUT /products/:product_id — Update"""
    error = validateProductUpdate(request)
    if error:
        return error
    return updateProduct(request)

def DELETE_product_by_id(request):
    """DELETE /products/:product_id — Delete (stub; add auth later)"""
    return deleteProduct(request)
