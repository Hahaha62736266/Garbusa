# ==========================================================
# THIN CONTROLLER: Products
# ==========================================================
from models.product_model import Product

def listProducts(request):
    products = Product.all()
    return {"status": 200, "data": products, "error": None}

def showProduct(request):
    product_id = request.params.get("product_id")
    product = Product.find(product_id)
    return {"status": 200, "data": product, "error": None}

def createProduct(request):
    data = request.validatedBody
    product = Product.save(data)
    return {"status": 201, "data": product, "error": None}

def updateProduct(request):
    product_id = request.params.get("product_id")
    data = request.validatedBody
    product = Product.update(product_id, data)
    return {"status": 200, "data": product, "error": None}

def deleteProduct(request):
    product_id = request.params.get("product_id")
    Product.remove(product_id)
    return {"status": 200, "data": {"deleted_id": product_id}, "error": None}
