# OWNER: Baydal
def listCustomers(request):
    return {"status":200,"data":{"message":"listCustomers stub"},"error":None}

def showCustomer(request):
    cid = request.params.get("customer_id")
    return {"status":200,"data":{"message":"showCustomer stub","customer_id":cid},"error":None}

def createCustomer(request):
    return {"status":201,"data":{"message":"createCustomer stub"},"error":None}

def updateCustomer(request):
    cid = request.params.get("customer_id")
    return {"status":200,"data":{"message":"updateCustomer stub","customer_id":cid},"error":None}

def deleteCustomer(request):
    cid = request.params.get("customer_id")
    return {"status":200,"data":{"message":"deleteCustomer stub","customer_id":cid},"error":None}
