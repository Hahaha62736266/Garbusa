# ==========================================================
# THIN CONTROLLER: Collections
# ==========================================================
from models.collection_model import Collection

def listCollections(request):
    collections = Collection.all()
    return {"status": 200, "data": collections, "error": None}

def showCollection(request):
    collection_id = request.params.get("collection_id")
    collection = Collection.find(collection_id)
    return {"status": 200, "data": collection, "error": None}

def createCollection(request):
    data = request.validatedBody
    collection = Collection.save(data)
    return {"status": 201, "data": collection, "error": None}

def updateCollection(request):
    collection_id = request.params.get("collection_id")
    data = request.validatedBody
    collection = Collection.update(collection_id, data)
    return {"status": 200, "data": collection, "error": None}

def deleteCollection(request):
    collection_id = request.params.get("collection_id")
    Collection.remove(collection_id)
    return {"status": 200, "data": {"deleted_id": collection_id}, "error": None}
