from flask import Flask, render_template, request, redirect, url_for, jsonify

# Import controllers
from controllers.customer_controller import (
    list_customers, showCustomer, createCustomer, updateCustomer, deleteCustomer
)

app = Flask(__name__)

# =============================================
# 🏠 WEB PAGES — These were MISSING!
# =============================================
@app.route("/dashboard")
def dashboard():
    from flask import render_template
    return render_template("dashboard.html")

@app.route("/customers")
def customers_page():
    try:
        result = list_customers()
        return render_template("customers/list.html", customers=result["data"])
    except Exception as e:
        # Pass error → triggers Error State
        return render_template("customers/list.html", error=str(e)), 500

@app.route("/customers/create", methods=["GET", "POST"])
def customers_create_page():
    if request.method == "POST":
        class Req:
            def __init__(self, body):
                self.body = body
                self.validatedBody = body
        req = Req(request.form)
        result = createCustomer(req)
        if result["status"] == 201:
            return redirect(url_for("customers_page"))
        return f"Error: {result.get('message')} — {result.get('error','')}"
    return render_template("customers/create.html")

# =============================================
# 🧾 API ENDPOINTS — Keep your original ones
# =============================================
@app.route("/api/customers", methods=["GET"])
def api_list_customers():
    return jsonify(list_customers()), 200

@app.route("/api/customers", methods=["POST"])
def api_create_customer():
    body = request.get_json(silent=True) or {}
    class Req:
        def __init__(self, b):
            self.body = b
            self.validatedBody = b
    result = createCustomer(Req(body))
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
# 🏠 HOME & WEB PAGES
# ═══════════════════════════════════════════════════════
from flask import render_template, redirect, url_for, request

@app.route("/", methods=["GET"])
def index():
    try:
        return render_template("index.html")
    except Exception as e:
        return f"""
        <html><body style="padding:2rem;font-family:sans-serif;">
            <h1>💧 Aquaflow Tracker</h1>
            <p style="color:red;">⚠️ Template missing: {e}</p>
            <h3>Quick Links:</h3>
            <ul>
                <li><a href="/customers">/customers</a> — Customer List</li>
                <li><a href="/api/customers">/api/customers</a> — JSON Data</li>
            </ul>
        </body></html>
        """, 200

# 👤 Customers Web Pages
@app.route("/customers")
def customers_list_page():
    try:
        from controllers.customer_controller import list_customers
        result = list_customers()
        return render_template("customers/list.html", customers=result["data"])
    except Exception as e:
        return f"Error: {str(e)}", 500

@app.route("/customers/create", methods=["GET", "POST"])
def customers_create_page():
    from controllers.customer_controller import createCustomer
    if request.method == "POST":
        class Req:
            def __init__(self, body):
                self.body = body
                self.validatedBody = body
        req = Req(request.form)
        result = createCustomer(req)
        if result["status"] == 201:
            return redirect(url_for("customers_list_page"))
        return f"Error: {result['message']}", 400



# ==================================================
# ✅ STANDARD ERROR HANDLER — PREVENT STACK TRACES LEAKING
# ==================================================
@app.errorhandler(Exception)

def handle_all_errors(e):
    # NEVER return raw stack traces or database errors to client
    return {
        "status": 500,
        "error": "Internal server error. Please check your input or try again.",
        "field": "server"
    }, 500
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
