# ═══════════════════════════════════════════════════════
# 🏠 HOME & WEB PAGES
# ═══════════════════════════════════════════════════════
from flask import render_template, redirect, url_for

@app.route("/", methods=["GET"])
def index():
    # Check if templates exist — show dashboard page
    try:
        return render_template("index.html")
    except Exception:
        # Fallback: API info if template missing
        return jsonify({
            "message": "Garbusa API + Web Dashboard",
            "note": "Visit /customers for customer list page",
            "api_endpoints": {
                "customers": "/api/customers",
                "products": "/api/products",
                "orders": "/api/orders",
                "collections": "/api/collections"
            }
        }), 200

# 👤 Customers Web Pages
@app.route("/customers")
def customers_list_page():
    try:
        result = list_customers()
        return render_template("customers/list.html", customers=result["data"])
    except Exception as e:
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
            return redirect(url_for("customers_list_page"))
        return f"Error: {result['message']}"
    return render_template("customers/create.html")

@app.route("/customers/<customer_id>")
def customers_detail_page(customer_id):
    result = showCustomer(customer_id)
    if result["status"] == 404:
        return "Customer not found", 404
    return render_template("customers/detail.html", customer=result["data"])

@app.route("/customers/<customer_id>/edit", methods=["GET", "POST"])
def customers_edit_page(customer_id):
    if request.method == "POST":
        class Req:
            def __init__(self, body):
                self.body = body
        req = Req(request.form)
        result = updateCustomer(customer_id, req)
        if result["status"] == 200:
            return redirect(url_for("customers_detail_page", customer_id=customer_id))
        return f"Error: {result['message']}"
    result = showCustomer(customer_id)
    if result["status"] == 404:
        return "Customer not found", 404
    return render_template("customers/edit.html", customer=result["data"])

from flask import Flask, render_template

app = Flask(__name__)

# THIS IS THE HOME PAGE ROUTE — "Cannot GET /" means this was missing!
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/customers")
def customers():
    return render_template("customers/list.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
