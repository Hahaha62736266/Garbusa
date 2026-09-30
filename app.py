from flask import Flask, render_template, redirect, url_for, request, jsonify

app = Flask(__name__)

# =============================================
# 🏠 WEB PAGES
# =============================================
@app.route("/")
def home_page():
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

@app.route("/customers")
def customers_page():
    try:
        from controllers.customer_controller import list_customers
        result = list_customers()
        return render_template("customers/list.html", customers=result["data"])
    except Exception as e:
        return render_template("customers/list.html", error=str(e)), 500

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
            return redirect(url_for("customers_page"))
        return f"Error: {result.get('message')} — {result.get('error','')}", 400
    return render_template("customers/create.html")

# =============================================
# 📝 FORM SUBMISSION — NEW FUNCTION
# =============================================
@app.route("/submit-form", methods=["POST"])
def submit_form():
    """Handle general form submissions"""
    try:
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        message = request.form.get("message", "").strip()

        if not name or not email:
            return jsonify({
                "success": False,
                "message": "Name and email are required fields"
            }), 400

        # Save to database or process here
        print(f"📩 Form: {name} | {email} | {message}")

        return jsonify({
            "success": True,
            "message": "Form submitted successfully!"
        }), 200

    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Error: {str(e)}"
        }), 500

# =============================================
# 🧾 API — Customers
# =============================================
@app.route("/api/customers", methods=["GET"])
def api_list_customers():
    from controllers.customer_controller import list_customers
    return jsonify(list_customers()), 200

@app.route("/api/customers", methods=["POST"])
def api_create_customer():
    from controllers.customer_controller import createCustomer
    body = request.get_json(silent=True) or {}
    class Req:
        def __init__(self, b):
            self.body = b
            self.validatedBody = b
    return jsonify(createCustomer(Req(body))), 200

# =============================================
# 📦 API — Orders
# =============================================
class RequestWrapper:
    def __init__(self, body, params=None, auth_user_id=None):
        self.body = body
        self.params = params or {}
        self.auth_user_id = auth_user_id

def get_auth_user_id():
    return None

@app.route("/api/orders", methods=["GET"])
def api_list_orders():
    return jsonify({"status": 200, "data": []}), 200

@app.route("/api/orders/<order_id>", methods=["GET"])
def api_show_order(order_id):
    return jsonify({"status": 200, "data": {"id": order_id}}), 200

@app.route("/api/orders", methods=["POST"])
def api_create_order():
    return jsonify({"status": 201, "message": "Order created"}), 201

@app.route("/api/orders/<order_id>", methods=["PUT"])
def api_update_order(order_id):
    return jsonify({"status": 200, "message": f"Order {order_id} updated"}), 200

@app.route("/api/orders/<order_id>", methods=["DELETE"])
def api_delete_order(order_id):
    return jsonify({"status": 200, "message": f"Order {order_id} deleted"}), 200

# =============================================
# 📂 API — Collections
# =============================================
@app.route("/api/collections", methods=["GET"])
def api_list_collections():
    return jsonify({"status": 200, "data": []}), 200

@app.route("/api/collections/<collection_id>", methods=["GET"])
def api_show_collection(collection_id):
    return jsonify({"status": 200, "data": {"id": collection_id}}), 200

@app.route("/api/collections", methods=["POST"])
def api_create_collection():
    return jsonify({"status": 201, "message": "Collection created"}), 201

@app.route("/api/collections/<collection_id>", methods=["PUT"])
def api_update_collection(collection_id):
    return jsonify({"status": 200, "message": f"Collection {collection_id} updated"}), 200

@app.route("/api/collections/<collection_id>", methods=["DELETE"])
def api_delete_collection(collection_id):
    return jsonify({"status": 200, "message": f"Collection {collection_id} deleted"}), 200

# =============================================
# ✅ ERROR HANDLER
# =============================================
@app.errorhandler(Exception)
def handle_all_errors(e):
    return {
        "status": 500,
        "error": "Internal server error. Please check your input or try again.",
        "field": "server"
    }, 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
