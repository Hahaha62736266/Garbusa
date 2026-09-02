from models.product_model import Product
def listProducts(r): return {"status":200,"data":Product.all(),"error":None}
def showProduct(r): return {"status":200,"data":Product.find(r.params.get("product_id")),"error":None}
def createProduct(r): return {"status":201,"data":Product.save(r.validatedBody),"error":None}
def updateProduct(r): return {"status":200,"data":Product.update(r.params.get("product_id"),r.validatedBody),"error":None}
def deleteProduct(r): Product.remove(r.params.get("product_id")); return {"status":200,"data":{},"error":None}
