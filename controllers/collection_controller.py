from models.collection_model import Collection
def listCollections(r): return {"status":200,"data":Collection.all(),"error":None}
def showCollection(r): return {"status":200,"data":Collection.find(r.params.get("collection_id")),"error":None}
def createCollection(r): return {"status":201,"data":Collection.save(r.validatedBody),"error":None}
def updateCollection(r): return {"status":200,"data":Collection.update(r.params.get("collection_id"),r.validatedBody),"error":None}
def deleteCollection(r): Collection.remove(r.params.get("collection_id")); return {"status":200,"data":{},"error":None}
