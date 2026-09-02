from models.order_model import Order
def listOrders(r): return {"status":200,"data":Order.all(),"error":None}
def showOrder(r): return {"status":200,"data":Order.find(r.params.get("order_id")),"error":None}
def createOrder(r): return {"status":201,"data":Order.save(r.validatedBody),"error":None}
def updateOrder(r): return {"status":200,"data":Order.update(r.params.get("order_id"),r.validatedBody),"error":None}
def deleteOrder(r): Order.remove(r.params.get("order_id")); return {"status":200,"data":{},"error":None}
