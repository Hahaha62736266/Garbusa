# ==========================================================
# ROUTES: Collections
# Pipeline: Validation → Controller
# ==========================================================

from middleware.validation import (
    validateCollectionCreate,
    validateCollectionUpdate
)
from controllers.collection_controller import (
    listCollections,
    showCollection,
    createCollection,
    updateCollection,
    deleteCollection
)

def GET_collections(request):
    """GET /collections — List all"""
    return listCollections(request)

def GET_collection_by_id(request):
    """GET /collections/:collection_id — Show one"""
    return showCollection(request)

def POST_collections(request):
    """POST /collections — Create"""
    error = validateCollectionCreate(request)
    if error:
        return error
    return createCollection(request)

def PUT_collection_by_id(request):
    """PUT /collections/:collection_id — Update"""
    error = validateCollectionUpdate(request)
    if error:
        return error
    return updateCollection(request)

def DELETE_collection_by_id(request):
    """DELETE /collections/:collection_id — Delete (stub; add auth later)"""
    return deleteCollection(request)
