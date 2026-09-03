import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, request, jsonify, g

# ─── Import Your Full Pipeline ───
from middleware.validation import (
    validateCustomerCreate, validateCustomerUpdate,
    validateProductCreate, validateProductUpdate,
    validateOrderCreate, validateOrderUpdate,
    validateCollectionCreate, validateCollectionUpdate,
    authorizeDeleteOrder
)
from controllers.customer_controller import (
    listCustomers, showCustomer, createCustomer, updateCustomer, deleteCustomer
)
from controllers.product_controller import (
    listProducts, showProduct, createProduct, updateProduct, deleteProduct
)
from controllers.order_controller import (
    listOrders, showOrder, createOrder, updateOrder, deleteOrder
)
from controllers.collection_controller import (
    listCollections, showCollection, createCollection, updateCollection, deleteCollection
)

app = Flask(__name__)

# ═══════════════════════════════════════════════════════
# 🔗 REQUEST WRAPPER — Convert Flask request → Your format
# ═══════════════════════════════════════════════════════
class RequestWrapper:
    """Makes Flask request look like what your controllers expect"""
    def __init__(self, body, params=None, auth_user_id=None):
        self.body = body or {}
        self.params = params or {}
        self.validatedBody = None
        self.auth = {"user_id": auth_user_id} if auth_user_id else None


def get_auth_user_id():
    """Get auth from header: X-User-ID (for demo/testing)"""
    return request.headers.get("X-User-ID")


# ═══════════════════════════════════════════════════════
# 🧾 CUSTOMER ENDPOINTS
# ═══════════════════════════════════════════════════════
@app.route("/api/customers", methods=["GET"])
def api_list_customers():
    req = RequestWrapper({})
    result = listCustomers(req)
    return jsonify(result), result["status"]

@app.route("/api/customers/<customer_id>", methods=["GET"])
def api_show_customer(customer_id):
    req = RequestWrapper({}, params={"customer_id": customer_id})
    result = showCustomer(req)
    return jsonify(result), result["status"]

@app.route("/api/customers", methods=["POST"])
def api_create_customer():
    body = request.get_json(force=True, silent=True) or {}
    req = RequestWrapper(body, auth_user_id=get_auth_user_id())
    err = validateCustomerCreate(req)
    if err: return jsonify(err), err["status"]
    result = createCustomer(req)
    return jsonify(result), result["status"]

@app.route("/api/customers/<customer_id>", methods=["PUT"])
def api_update_customer(customer_id):
    body = request.get_json(force=True, silent=True) or {}
    req = RequestWrapper(body, params={"customer_id": customer_id})
    err = validateCustomerUpdate(req)
    if err: return jsonify(err), err["status"]
    result = updateCustomer(req)
    return jsonify(result), result["status"]

@app.route("/api/customers/<customer_id>", methods=["DELETE"])
def api_delete_customer(customer_id):
    req = RequestWrapper({}, params={"customer_id": customer_id})
    result = deleteCustomer(req)
    return jsonify(result), result["status"]


# ═══════════════════════════════════════════════════════
# 🧾 PRODUCT ENDPOINTS
# ═══════════════════════════════════════════════════════
@app.route("/api/products", methods=["GET"])
def api_list_products():
    req = RequestWrapper({})
    result = listProducts(req)
    return jsonify(result), result["status"]

@app.route("/api/products/<product_id>", methods=["GET"])
def api_show_product(product_id):
    req = RequestWrapper({}, params={"product_id": product_id})
    result = showProduct(req)
    return jsonify(result), result["status"]

@app.route("/api/products", methods=["POST"])
def api_create_product():
    body = request.get_json(force=True, silent=True) or {}
    req = RequestWrapper(body)
    err = validateProductCreate(req)
    if err: return jsonify(err), err["status"]
    result = createProduct(req)
    return jsonify(result), result["status"]

@app.route("/api/products/<product_id>", methods=["PUT"])
def api_update_product(product_id):
    body = request.get_json(force=True, silent=True) or {}
    req = RequestWrapper(body, params={"product_id": product_id})
    err = validateProductUpdate(req)
    if err: return jsonify(err), err["status"]
    result = updateProduct(req)
    return jsonify(result), result["status"]

@app.route("/api/products/<product_id>", methods=["DELETE"])
def api_delete_product(product_id):
    req = RequestWrapper({}, params={"product_id": product_id})
    result = deleteProduct(req)
    return jsonify(result), result["status"]


# ═══════════════════════════════════════════════════════
# 🧾 ORDER ENDPOINTS
# ═══════════════════════════════════════════════════════
@app.route("/api/orders", methods=["GET"])
def api_list_orders():
    req = RequestWrapper({})
    result = listOrders(req)
    return jsonify(result), result["status"]

@app.route("/api/orders/<order_id>", methods=["GET"])
def api_show_order(order_id):
    req = RequestWrapper({}, params={"order_id": order_id})
    result = showOrder(req)
    return jsonify(result), result["status"]

@app.route("/api/orders", methods=["POST"])
def api_create_order():
    body = request.get_json(force=True, silent=True) or {}
    req = RequestWrapper(body, auth_user_id=get_auth_user_id())
    err = validateOrderCreate(req)
    if err: return jsonify(err), err["status"]
    result = createOrder(req)
    return jsonify(result), result["status"]

@app.route("/api/orders/<order_id>", methods=["PUT"])
def api_update_order(order_id):
    body = request.get_json(force=True, silent=True) or {}
    req = RequestWrapper(body, params={"order_id": order_id})
    err = validateOrderUpdate(req)
    if err: return jsonify(err), err["status"]
    result = updateOrder(req)
    return jsonify(result), result["status"]

@app.route("/api/orders/<order_id>", methods=["DELETE"])
def api_delete_order(order_id):
    req = RequestWrapper({}, params={"order_id": order_id}, auth_user_id=get_auth_user_id())
    auth_err = authorizeDeleteOrder(req)
    if auth_err: return jsonify(auth_err), auth_err["status"]
    result = deleteOrder(req)
    return jsonify(result), result["status"]


# ═══════════════════════════════════════════════════════
# 🧾 COLLECTION ENDPOINTS
# ═══════════════════════════════════════════════════════
@app.route("/api/collections", methods=["GET"])
def api_list_collections():
    req = RequestWrapper({})
    result = listCollections(req)
    return jsonify(result), result["status"]

@app.route("/api/collections/<collection_id>", methods=["GET"])
def api_show_collection(collection_id):
    req = RequestWrapper({}, params={"collection_id": collection_id})
    result = showCollection(req)
    return jsonify(result), result["status"]

@app.route("/api/collections", methods=["POST"])
def api_create_collection():
    body = request.get_json(force=True, silent=True) or {}
    req = RequestWrapper(body, auth_user_id=get_auth_user_id())
    err = validateCollectionCreate(req)
    if err: return jsonify(err), err["status"]
    result = createCollection(req)
    return jsonify(result), result["status"]

@app.route("/api/collections/<collection_id>", methods=["PUT"])
def api_update_collection(collection_id):
    body = request.get_json(force=True, silent=True) or {}
    req = RequestWrapper(body, params={"collection_id": collection_id})
    err = validateCollectionUpdate(req)
    if err: return jsonify(err), err["status"]
    result = updateCollection(req)
    return jsonify(result), result["status"]

@app.route("/api/collections/<collection_id>", methods=["DELETE"])
def api_delete_collection(collection_id):
    req = RequestWrapper({}, params={"collection_id": collection_id})
    result = deleteCollection(req)
    return jsonify(result), result["status"]


# ═══════════════════════════════════════════════════════
# 🏠 HOME
# ═══════════════════════════════════════════════════════
@app.route("/", methods=["GET"])
def index():
    return jsonify({
        "message": "Garbusa REST API — Full Pipeline Working ✅",
        "version": "1.0.0",
        "endpoints": {
            "customers": "/api/customers",
            "products": "/api/products",
            "orders": "/api/orders",
            "collections": "/api/collections"
        },
        "note": "Send X-User-ID header for auth/delete operations"
    }), 200


if __name__ == "__main__":
    print("🚀 Starting Garbusa API Server...")
    print("📍 http://127.0.0.1:5000")
    app.run(host="0.0.0.0", port=5000, debug=True)
