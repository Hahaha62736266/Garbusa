# OWNER: Obiasad
def listProducts(request):
    return {"status":200,"data":{"message":"listProducts stub"},"error":None}

def showProduct(request):
    pid = request.params.get("product_id")
    return {"status":200,"data":{"message":"showProduct stub","product_id":pid},"error":None}

def createProduct(request):
    return {"status":201,"data":{"message":"createProduct stub"},"error":None}

def updateProduct(request):
    pid = request.params.get("product_id")
    return {"status":200,"data":{"message":"updateProduct stub","product_id":pid},"error":None}

def deleteProduct(request):
    pid = request.params.get("product_id")
    return {"status":200,"data":{"message":"deleteProduct stub","product_id":pid},"error":None}
