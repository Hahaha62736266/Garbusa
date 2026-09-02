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
