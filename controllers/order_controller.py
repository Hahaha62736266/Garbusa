# OWNER: Taylaran
def listOrders(request):
    return {"status":200,"data":{"message":"listOrders stub"},"error":None}

def showOrder(request):
    oid = request.params.get("order_id")
    return {"status":200,"data":{"message":"showOrder stub","order_id":oid},"error":None}

def createOrder(request):
    return {"status":201,"data":{"message":"createOrder stub"},"error":None}

def updateOrder(request):
    oid = request.params.get("order_id")
    return {"status":200,"data":{"message":"updateOrder stub","order_id":oid},"error":None}

def deleteOrder(request):
    oid = request.params.get("order_id")
    return {"status":200,"data":{"message":"deleteOrder stub","order_id":oid},"error":None}
