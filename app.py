"""
Aquaflow Tracker — Flask Application Entry Point
Water Refilling Station Management System
"""

import os
import uuid
import datetime
from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
from supabase import create_client, Client

# ==================================================
# ENVIRONMENT & CONFIG
# ==================================================
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "dev-secret-key")

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY") or os.getenv("SUPABASE_PUBLISHABLE_KEY") or os.getenv("SUPABASE_SECRET_KEY")

# Initialize Supabase client (will be None if keys are not set)
supabase: Client = None
is_placeholder = any(p in (SUPABASE_URL or "").lower() for p in ["your-project", "your-anon", "your-service-role"])
if SUPABASE_URL and SUPABASE_KEY and not is_placeholder:
    try:
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
        print("[+] Supabase connected successfully.")
    except Exception as e:
        print(f"[!] Supabase connection failed: {e}")
else:
    print("[!] Supabase not configured. Set real SUPABASE_URL and SUPABASE_KEY in .env")



# In-memory storage fallback when Supabase is not connected
MOCK_DB = {
    "customers": [],
    "products": [],
    "orders": [],
    "collections": []
}


def fetch_all(table):
    """Get all records from a Supabase table (or mock store if disconnected)"""
    if supabase:
        try:
            res = supabase.table(table).select("*").execute()
            return res.data or []
        except Exception as e:
            print(f"Error loading {table}: {e}")
            return MOCK_DB.get(table, [])
    return MOCK_DB.get(table, [])


def insert_record(table, data):
    """Add a new record to a Supabase table (or mock store if disconnected)"""
    if supabase:
        try:
            supabase.table(table).insert(data).execute()
            return True
        except Exception as e:
            print(f"Error saving to {table}: {e}")
            return False
    MOCK_DB.setdefault(table, []).append(data)
    return True


def update_order_status(order_id, new_status):
    """Update delivery status of an order"""
    if supabase:
        try:
            supabase.table("orders").update({"status": new_status}).eq("order_id", order_id).execute()
            return True
        except Exception as e:
            print(f"Error updating order: {e}")
            return False
    for order in MOCK_DB.get("orders", []):
        if order.get("order_id") == order_id:
            order["status"] = new_status
            return True
    return False


def get_next_id(table, prefix):
    """Generate next sequential ID like C001, O002"""
    records = fetch_all(table)
    count = len(records) + 1
    return f"{prefix}{count:03d}"



# ==================================================
# ROUTES — CUSTOMERS
# ==================================================
@app.route("/api/customers", methods=["GET"])
def get_customers():
    customers = fetch_all("customers")
    return jsonify({"status": 200, "data": customers})


@app.route("/api/customers", methods=["POST"])
def add_customer():
    data = request.get_json()
    if not data or not data.get("full_name"):
        return jsonify({"status": 422, "error": "full_name is required"}), 422

    new_id = get_next_id("customers", "C")
    record = {
        "customer_id": new_id,
        "full_name": data.get("full_name"),
        "contact_number": data.get("contact_number"),
        "address": data.get("address"),
        "container_owned": data.get("container_owned", 0),
        "registration_date": str(datetime.date.today())
    }
    if insert_record("customers", record):
        return jsonify({"status": 201, "message": f"Customer {new_id} created", "data": record}), 201
    return jsonify({"status": 500, "error": "Failed to save customer"}), 500


# ==================================================
# ROUTES — PRODUCTS
# ==================================================
@app.route("/api/products", methods=["GET"])
def get_products():
    products = fetch_all("products")
    return jsonify({"status": 200, "data": products})


@app.route("/api/products", methods=["POST"])
def add_product():
    data = request.get_json()
    if not data or not data.get("product_name"):
        return jsonify({"status": 422, "error": "product_name is required"}), 422
    if data.get("price_per_unit", 0) < 0:
        return jsonify({"status": 422, "error": "price_per_unit cannot be negative"}), 422

    new_id = get_next_id("products", "P")
    record = {
        "product_id": new_id,
        "product_name": data.get("product_name"),
        "price_per_unit": float(data.get("price_per_unit", 0)),
        "description": data.get("description", ""),
        "stock_available": data.get("stock_available", 0)
    }
    if insert_record("products", record):
        return jsonify({"status": 201, "message": f"Product {new_id} created", "data": record}), 201
    return jsonify({"status": 500, "error": "Failed to save product"}), 500


# ==================================================
# ROUTES — ORDERS
# ==================================================
@app.route("/api/orders", methods=["GET"])
def get_orders():
    orders = fetch_all("orders")
    return jsonify({"status": 200, "data": orders})


@app.route("/api/orders", methods=["POST"])
def add_order():
    data = request.get_json()
    if not data or not data.get("customer_id") or not data.get("product_id"):
        return jsonify({"status": 422, "error": "customer_id and product_id are required"}), 422
    if data.get("quantity", 0) < 1:
        return jsonify({"status": 422, "error": "quantity must be at least 1"}), 422

    new_id = get_next_id("orders", "O")
    record = {
        "order_id": new_id,
        "customer_id": data.get("customer_id"),
        "product_id": data.get("product_id"),
        "quantity": data.get("quantity"),
        "total_amount": float(data.get("total_amount", 0)),
        "order_date": str(datetime.date.today()),
        "status": "Pending"
    }
    if insert_record("orders", record):
        return jsonify({"status": 201, "message": f"Order {new_id} created", "data": record}), 201
    return jsonify({"status": 500, "error": "Failed to save order"}), 500


@app.route("/api/orders/<order_id>", methods=["PATCH"])
def patch_order_status(order_id):
    data = request.get_json()
    new_status = data.get("status")
    if new_status not in ["Pending", "Delivered", "Cancelled"]:
        return jsonify({"status": 422, "error": "status must be Pending, Delivered, or Cancelled"}), 422
    if update_order_status(order_id, new_status):
        return jsonify({"status": 200, "message": f"Order {order_id} updated to {new_status}"})
    return jsonify({"status": 500, "error": "Failed to update order"}), 500


# ==================================================
# ROUTES — COLLECTIONS
# ==================================================
@app.route("/api/collections", methods=["GET"])
def get_collections():
    collections = fetch_all("collections")
    return jsonify({"status": 200, "data": collections})


@app.route("/api/collections", methods=["POST"])
def add_collection():
    data = request.get_json()
    if not data or not data.get("customer_id"):
        return jsonify({"status": 422, "error": "customer_id is required"}), 422

    empty_returned = data.get("empty_jugs_returned", 0)
    filled_released = data.get("filled_jugs_released", 0)
    balance = filled_released - empty_returned

    if balance < 0:
        return jsonify({"status": 422, "error": "container_balance cannot be negative"}), 422

    new_id = get_next_id("collections", "CL")
    record = {
        "collection_id": new_id,
        "customer_id": data.get("customer_id"),
        "order_id": data.get("order_id"),
        "empty_jugs_returned": empty_returned,
        "filled_jugs_released": filled_released,
        "container_balance": balance,
        "collection_date": str(datetime.date.today()),
        "collected_by": data.get("collected_by", "")
    }
    if insert_record("collections", record):
        return jsonify({"status": 201, "message": f"Collection {new_id} recorded", "data": record}), 201
    return jsonify({"status": 500, "error": "Failed to save collection"}), 500


# ==================================================
# DASHBOARD ROUTE — serves the HTML frontend
# ==================================================
@app.route("/")
def dashboard():
    return app.send_static_file("../index.html") if not os.path.exists("templates/index.html") \
        else render_template("index.html")


@app.route("/login")
def login_page():
    return render_template("login.html")



# ==================================================
# AUTHENTICATION & USERS
# ==================================================
SYSTEM_USERS = {
    "admin@aquaflow.com": {"name": "System Admin", "role": "admin", "password": "admin123"},
    "delivery@aquaflow.com": {"name": "Delivery Team", "role": "delivery", "password": "staff123"},
    "customer@aquaflow.com": {"name": "Juan Dela Cruz", "role": "customer", "customer_id": "C001", "password": "user123"}
}


@app.route("/api/login", methods=["POST"])
def api_login():
    data = request.get_json() or {}
    email = data.get("email", "").strip().lower()
    password = data.get("password", "").strip()

    user = SYSTEM_USERS.get(email)
    if user and user["password"] == password:
        return jsonify({
            "status": 200,
            "message": "Login successful",
            "user": {
                "email": email,
                "name": user["name"],
                "role": user["role"],
                "customer_id": user.get("customer_id")
            }
        })
    return jsonify({"status": 401, "error": "Invalid email or password"}), 401


# ==================================================
# HEALTH CHECK
# ==================================================
@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({
        "status": 200,
        "message": "AquaFlow Tracker API is running",
        "supabase_connected": supabase is not None,
        "version": "1.0.0"
    })



# ==================================================
# ENTRY POINT
# ==================================================
if __name__ == "__main__":
    app.run(debug=True, use_reloader=True, port=5000)
