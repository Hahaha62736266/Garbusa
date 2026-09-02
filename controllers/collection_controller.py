# OWNER: Apostol
def listCollections(request):
    return {"status":200,"data":{"message":"listCollections stub"},"error":None}

def showCollection(request):
    clid = request.params.get("collection_id")
    return {"status":200,"data":{"message":"showCollection stub","collection_id":clid},"error":None}

def createCollection(request):
    return {"status":201,"data":{"message":"createCollection stub"},"error":None}

def updateCollection(request):
    clid = request.params.get("collection_id")
    return {"status":200,"data":{"message":"updateCollection stub","collection_id":clid},"error":None}

def deleteCollection(request):
    clid = request.params.get("collection_id")
    return {"status":200,"data":{"message":"deleteCollection stub","collection_id":clid},"error":None}
