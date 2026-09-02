# ===================================
# Collection Stub Handlers
# ===================================

def listCollections(request):
    """GET /collections — List all transactions"""
    return {
        "status": 200,
        "data": { "message": "listCollections stub" },
        "error": None
    }


def showCollection(request):
    """GET /collections/:collection_id — View one transaction"""
    collection_id = request.params.get("collection_id")
    return {
        "status": 200,
        "data": {
            "message": "showCollection stub",
            "collection_id": collection_id
        },
        "error": None
    }


def createCollection(request):
    """POST /collections — Create new transaction"""
    return {
        "status": 201,
        "data": { "message": "createCollection stub" },
        "error": None
    }


def updateCollection(request):
    """PUT /collections/:collection_id — Update transaction"""
    collection_id = request.params.get("collection_id")
    return {
        "status": 200,
        "data": {
            "message": "updateCollection stub",
            "collection_id": collection_id
        },
        "error": None
    }


def deleteCollection(request):
    """DELETE /collections/:collection_id — Delete transaction"""
    collection_id = request.params.get("collection_id")
    return {
        "status": 200,
        "data": {
            "message": "deleteCollection stub",
            "collection_id": collection_id
        },
        "error": None
    }
