# ===================================
# Product Stub Handlers
# ===================================

def listProducts(request):
    """GET /products — List all products"""
    return {
        "status": 200,
        "data": { "message": "listProducts stub" },
        "error": None
    }


def showProduct(request):
    """GET /products/:product_id — View one product"""
    product_id = request.params.get("product_id")
    return {
        "status": 200,
        "data": {
            "message": "showProduct stub",
            "product_id": product_id
        },
        "error": None
    }


def createProduct(request):
    """POST /products — Create new product"""
    return {
        "status": 201,
        "data": { "message": "createProduct stub" },
        "error": None
    }


def updateProduct(request):
    """PUT /products/:product_id — Update product"""
    product_id = request.params.get("product_id")
    return {
        "status": 200,
        "data": {
            "message": "updateProduct stub",
            "product_id": product_id
        },
        "error": None
    }


def deleteProduct(request):
    """DELETE /products/:product_id — Delete product"""
    product_id = request.params.get("product_id")
    return {
        "status": 200,
        "data": {
            "message": "deleteProduct stub",
            "product_id": product_id
        },
        "error": None
    }

