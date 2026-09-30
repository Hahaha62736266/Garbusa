"""
Aquaflow Tracker — Main Flask App
Serves all static templates + connects to controllers
"""
from flask import Flask, render_template, request, redirect, url_for

# Import controllers
from controllers.customer_controller import (
    list_customers,
    showCustomer,
    createCustomer,
    updateCustomer,
    deleteCustomer
)

app = Flask(__name__)

# =============================================
# 🏠 DASHBOARD / HOME
# =============================================
@app.route("/")
def index():
    return render_template("index.html")

# =============================================
# 👤 CUSTOMERS — List, Create, Detail, Edit
# =============================================
@app.route("/customers")
def customers_list():
    result = list_customers()
    return render_template("customers/list.html", customers=result["data"])

@app.route("/customers/create", methods=["GET", "POST"])
def customers_create():
    if request.method == "POST":
        # Wrap request body to match controller expectation
        class Req:
            def __init__(self, body):
                self.body = body
                self.validatedBody = body
        req = Req(request.form)
        result = createCustomer(req)
        if result["status"] == 201:
            return redirect(url_for("customers_list"))
        return f"Error: {result['message']} — {result.get('error','')}"
    return render_template("customers/create.html")

@app.route("/customers/<customer_id>")
def customers_detail(customer_id):
    result = showCustomer(customer_id)
    if result["status"] == 404:
        return "Customer not found", 404
    return render_template("customers/detail.html", customer=result["data"])

@app.route("/customers")
def customers_list():
    try:
        result = list_customers()
        # Pass empty list [] if no data — triggers empty state
        return render_template("customers/list.html", customers=result["data"])
    except Exception as e:
        # Pass error message — triggers error state
        return render_template("customers/list.html", error=str(e)), 500

@app.route("/customers/<customer_id>/edit", methods=["GET", "POST"])
def customers_edit(customer_id):
    if request.method == "POST":
        class Req:
            def __init__(self, body):
                self.body = body
        req = Req(request.form)
        result = updateCustomer(customer_id, req)
        if result["status"] == 200:
            return redirect(url_for("customers_detail", customer_id=customer_id))
        return f"Error: {result['message']}"
    # GET — Show edit form with sample data
    result = showCustomer(customer_id)
    if result["status"] == 404:
        return "Customer not found", 404
    return render_template("customers/edit.html", customer=result["data"])

# =============================================
# 🚀 RUN SERVER
# =============================================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
