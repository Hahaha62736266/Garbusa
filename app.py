from flask import Flask, render_template, request, redirect, url_for, jsonify

# Import controllers
from controllers.customer_controller import (
    list_customers, showCustomer, createCustomer, updateCustomer, deleteCustomer
)

app = Flask(__name__)

# =============================================
# 🏠 WEB PAGES — These were MISSING!
# =============================================
@app.route("/")
def home_page():
    return render_template("index.html")

@app.route("/customers")
def customers_page():
    try:
        result = list_customers()
        return render_template("customers/list.html", customers=result["data"])
    except Exception as e:
        return render_template("customers/list.html", error=str(e))

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

# =============================================
# 🚀 SERVER — Must use 0.0.0.0 for Codespaces
# =============================================
if __name__ == "__main__":
    print("🚀 Aquaflow starting...")
    app.run(host="0.0.0.0", port=5000, debug=True)
