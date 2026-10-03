"""
Aquaflow Tracker — Flask Application Entry Point
Water Refilling Station Management System
"""

import os
import re
import secrets
import datetime
from functools import wraps

from flask import Flask, request, jsonify, render_template, session, redirect, url_for
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash, check_password_hash
from supabase import create_client, Client

from middleware.validation import ALLOWED_ORDER_STATUSES

# ==================================================
# ENVIRONMENT & CONFIG
# ==================================================
load_dotenv()


def env_flag(name, default=False):
    """Read a true/false environment variable."""
    return os.getenv(name, str(default)).strip().lower() in ("1", "true", "yes", "on")


app = Flask(__name__)

_secret_key = os.getenv("SECRET_KEY")
if not _secret_key:
    _secret_key = secrets.token_hex(32)
    print("[!] SECRET_KEY not set — using a temporary key (all sessions reset on restart).")
app.secret_key = _secret_key
app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",
    SESSION_COOKIE_SECURE=env_flag("SESSION_COOKIE_SECURE"),  # set true when served over HTTPS
    PERMANENT_SESSION_LIFETIME=datetime.timedelta(hours=12),
)

DEMO_MODE = env_flag("DEMO_MODE")

ROLES = ("admin", "delivery", "customer")
SELF_REGISTER_ROLES = ("customer", "delivery")  # admins can never self-register
EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
MIN_PASSWORD_LENGTH = 8

# ==================================================
# SUPABASE CONNECTION
# ==================================================
SUPABASE_URL = os.getenv("SUPABASE_URL", "")

# The backend should use the SECRET key (bypasses RLS). The legacy SUPABASE_KEY
# is only a fallback — once schema.sql is applied, anon keys are blocked by RLS.
_KEY_CANDIDATES = ("SUPABASE_SECRET_KEY", "SUPABASE_KEY")


def _connect_supabase():
    is_placeholder = any(p in SUPABASE_URL.lower() for p in ("your-project", "your-anon", "your-service-role"))
    if not SUPABASE_URL or is_placeholder:
        print("[!] Supabase not configured. Set SUPABASE_URL and SUPABASE_SECRET_KEY in .env")
        return None, None
    for key_name in _KEY_CANDIDATES:
        key = os.getenv(key_name)
        if not key:
            continue
        try:
            client = create_client(SUPABASE_URL, key)
            print(f"[+] Supabase connected using {key_name}.")
            return client, key_name
        except Exception as e:
            print(f"[!] Supabase rejected {key_name}: {e}")
    print("[!] Supabase connection failed — running on the in-memory store.")
    return None, None


supabase: Client
supabase, SUPABASE_KEY_NAME = _connect_supabase()
if supabase and SUPABASE_KEY_NAME != "SUPABASE_SECRET_KEY":
    print("[!] Warning: not using SUPABASE_SECRET_KEY. After applying schema.sql, "
          "the public key is blocked by Row Level Security.")


# ==================================================
# DATA ACCESS HELPERS
# ==================================================
# In-memory storage fallback when Supabase is not connected
MOCK_DB = {
    "customers": [],
    "products": [],
    "orders": [],
    "collections": [],
    "users": [],
}

ID_FIELDS = {
    "customers": "customer_id",
    "products": "product_id",
    "orders": "order_id",
    "collections": "collection_id",
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
    """Update delivery status of an order.
    Returns True on success, None if the order does not exist, False on error."""
    if supabase:
        try:
            res = supabase.table("orders").update({"status": new_status}).eq("order_id", order_id).execute()
            return True if res.data else None
        except Exception as e:
            print(f"Error updating order: {e}")
            return False
    for order in MOCK_DB.get("orders", []):
        if order.get("order_id") == order_id:
            order["status"] = new_status
            return True
    return None


def delete_record(table, record_id):
    """Delete a record by ID."""
    id_field = ID_FIELDS[table]
    if supabase:
        try:
            res = supabase.table(table).delete().eq(id_field, record_id).execute()
            return True if res.data else None
        except Exception as e:
            print(f"Error deleting from {table}: {e}")
            return False
    records = MOCK_DB.get(table, [])
    for i, rec in enumerate(records):
        if rec.get(id_field) == record_id:
            del records[i]
            return True
    return None


def get_next_id(table, prefix):
    """Generate the next sequential ID like C001, O002.
    Uses the HIGHEST existing number + 1, so deleting records never causes duplicates."""
    id_field = ID_FIELDS[table]
    pattern = re.compile(rf"^{re.escape(prefix)}(\d+)$")
    highest = 0
    for record in fetch_all(table):
        match = pattern.match(str(record.get(id_field, "")))
        if match:
            highest = max(highest, int(match.group(1)))
    return f"{prefix}{highest + 1:03d}"


def scope_to_user(records):
    """Customers only see their own records; admin/delivery see everything."""
    user = current_user()
    if user["role"] == "customer":
        return [r for r in records if r.get("customer_id") == user.get("customer_id")]
    return records


# ==================================================
# INPUT PARSING HELPERS
# ==================================================
def get_json_body():
    """Return the JSON body as a dict (never None, never raises)."""
    data = request.get_json(silent=True)
    return data if isinstance(data, dict) else {}


def clean_str(data, key):
    value = data.get(key, "")
    return value.strip() if isinstance(value, str) else ""


def parse_int(value, default=None):
    """Parse a whole number. Raises ValueError for bools, decimals, or junk."""
    if value is None or value == "":
        if default is None:
            raise ValueError("missing")
        return default
    if isinstance(value, bool) or (isinstance(value, float) and not value.is_integer()):
        raise ValueError("not an integer")
    return int(value)


def parse_float(value, default=0.0):
    if value is None or value == "":
        return default
    if isinstance(value, bool):
        raise ValueError("not a number")
    return float(value)


def error(status, message):
    return jsonify({"status": status, "error": message}), status


# ==================================================
# USER ACCOUNTS (hashed passwords)
# ==================================================
def find_user(email):
    """Look up a login account by email."""
    if supabase:
        try:
            res = supabase.table("users").select("*").eq("email", email).limit(1).execute()
            return res.data[0] if res.data else None
        except Exception as e:
            print(f"[!] users table unavailable ({e}) — using in-memory accounts. Run schema.sql in Supabase.")
    return next((u for u in MOCK_DB["users"] if u["email"] == email), None)


def save_user(record):
    """Store a login account (falls back to memory if the users table is missing)."""
    if supabase:
        try:
            supabase.table("users").insert(record).execute()
            return True
        except Exception as e:
            print(f"[!] Could not save user to Supabase ({e}) — storing in memory.")
    MOCK_DB["users"].append(record)
    return True


def create_account(email, password, full_name, role, contact_number="", address=""):
    """Create a login account. Customers also get a linked customer record."""
    customer_id = None
    if role == "customer":
        customer_id = get_next_id("customers", "C")
        cust_record = {
            "customer_id": customer_id,
            "full_name": full_name,
            "contact_number": contact_number,
            "address": address,
            "container_owned": 0,
            "registration_date": str(datetime.date.today()),
        }
        if not insert_record("customers", cust_record):
            return None
    user = {
        "email": email,
        "password_hash": generate_password_hash(password),
        "full_name": full_name,
        "role": role,
        "customer_id": customer_id,
    }
    save_user(user)
    return user


def public_user(user):
    """User info that is safe to send to the browser (no password hash)."""
    return {
        "email": user["email"],
        "name": user["full_name"],
        "role": user["role"],
        "customer_id": user.get("customer_id"),
    }


# Demo accounts — only created when DEMO_MODE=true (classroom demos)
DEMO_ACCOUNTS = [
    {"email": "admin@aquaflow.com", "password": "admin123", "full_name": "System Admin", "role": "admin", "label": "Admin"},
    {"email": "delivery@aquaflow.com", "password": "staff123", "full_name": "Delivery Team", "role": "delivery", "label": "Collector"},
    {"email": "customer@aquaflow.com", "password": "user123", "full_name": "Juan Dela Cruz", "role": "customer", "label": "Customer"},
]
DEMO_PRESETS = []  # demo accounts usable from the login page preset buttons


def seed_accounts():
    """Create the admin account (from env) and, in demo mode, the demo accounts."""
    admin_email = os.getenv("ADMIN_EMAIL", "").strip().lower()
    admin_password = os.getenv("ADMIN_PASSWORD", "")
    if admin_email and admin_password and not find_user(admin_email):
        create_account(admin_email, admin_password, "System Admin", "admin")
        print(f"[+] Admin account created: {admin_email}")

    if DEMO_MODE:
        for demo in DEMO_ACCOUNTS:
            existing = find_user(demo["email"])
            if not existing:
                existing = create_account(demo["email"], demo["password"], demo["full_name"], demo["role"])
            # Only offer a preset button if the demo password actually works
            if existing and check_password_hash(existing["password_hash"], demo["password"]):
                DEMO_PRESETS.append({k: demo[k] for k in ("email", "password", "role", "label")})
        print(f"[i] DEMO_MODE on — {len(DEMO_PRESETS)} demo login preset(s) available.")


# ==================================================
# AUTH GUARDS
# ==================================================
def current_user():
    return session.get("user")


def login_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if not current_user():
            return error(401, "Login required")
        return fn(*args, **kwargs)
    return wrapper


def roles_required(*roles):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            user = current_user()
            if not user:
                return error(401, "Login required")
            if user["role"] not in roles:
                return error(403, "You do not have permission to do this")
            return fn(*args, **kwargs)
        return wrapper
    return decorator


# ==================================================
# ROUTES — CUSTOMERS
# ==================================================
@app.route("/api/customers", methods=["GET"])
@login_required
def get_customers():
    customers = scope_to_user(fetch_all("customers"))
    return jsonify({"status": 200, "data": customers})


@app.route("/api/customers", methods=["POST"])
@roles_required("admin")
def add_customer():
    data = get_json_body()
    full_name = clean_str(data, "full_name")
    if not full_name:
        return error(422, "full_name is required")
    try:
        container_owned = parse_int(data.get("container_owned"), default=0)
    except (TypeError, ValueError):
        return error(422, "container_owned must be a whole number")
    if container_owned < 0:
        return error(422, "container_owned cannot be negative")

    new_id = get_next_id("customers", "C")
    record = {
        "customer_id": new_id,
        "full_name": full_name,
        "contact_number": clean_str(data, "contact_number"),
        "address": clean_str(data, "address"),
        "container_owned": container_owned,
        "registration_date": str(datetime.date.today())
    }
    if insert_record("customers", record):
        return jsonify({"status": 201, "message": f"Customer {new_id} created", "data": record}), 201
    return error(500, "Failed to save customer")


# ==================================================
# ROUTES — PRODUCTS
# ==================================================
@app.route("/api/products", methods=["GET"])
@login_required
def get_products():
    products = fetch_all("products")
    return jsonify({"status": 200, "data": products})


@app.route("/api/products", methods=["POST"])
@roles_required("admin")
def add_product():
    data = get_json_body()
    product_name = clean_str(data, "product_name")
    if not product_name:
        return error(422, "product_name is required")
    try:
        price = parse_float(data.get("price_per_unit"), default=0.0)
        stock = parse_int(data.get("stock_available"), default=0)
    except (TypeError, ValueError):
        return error(422, "price_per_unit must be a number and stock_available a whole number")
    if price < 0:
        return error(422, "price_per_unit cannot be negative")
    if stock < 0:
        return error(422, "stock_available cannot be negative")

    new_id = get_next_id("products", "P")
    record = {
        "product_id": new_id,
        "product_name": product_name,
        "price_per_unit": price,
        "description": clean_str(data, "description"),
        "stock_available": stock
    }
    if insert_record("products", record):
        return jsonify({"status": 201, "message": f"Product {new_id} created", "data": record}), 201
    return error(500, "Failed to save product")


# ==================================================
# ROUTES — ORDERS
# ==================================================
@app.route("/api/orders", methods=["GET"])
@login_required
def get_orders():
    orders = scope_to_user(fetch_all("orders"))
    return jsonify({"status": 200, "data": orders})


@app.route("/api/orders", methods=["POST"])
@roles_required("admin", "customer", "delivery")
def add_order():
    data = get_json_body()
    user = current_user()
    customer_id = clean_str(data, "customer_id")
    product_id = clean_str(data, "product_id")

    # Customers can only place orders for themselves
    if user["role"] == "customer":
        if customer_id and customer_id != user.get("customer_id"):
            return error(403, "Customers can only place orders for their own account")
        customer_id = user.get("customer_id")

    if not customer_id or not product_id:
        return error(422, "customer_id and product_id are required")
    try:
        quantity = parse_int(data.get("quantity"))
        total_amount = parse_float(data.get("total_amount"), default=0.0)
    except (TypeError, ValueError):
        return error(422, "quantity must be a whole number and total_amount a number")
    if quantity < 1:
        return error(422, "quantity must be at least 1")
    if total_amount < 0:
        return error(422, "total_amount cannot be negative")

    new_id = get_next_id("orders", "O")
    record = {
        "order_id": new_id,
        "customer_id": customer_id,
        "product_id": product_id,
        "quantity": quantity,
        "total_amount": total_amount,
        "order_date": str(datetime.date.today()),
        "status": "Pending"
    }
    if insert_record("orders", record):
        return jsonify({"status": 201, "message": f"Order {new_id} created", "data": record}), 201
    return error(500, "Failed to save order")


@app.route("/api/orders/<order_id>", methods=["PATCH"])
@roles_required("admin", "delivery")
def patch_order_status(order_id):
    data = get_json_body()
    new_status = data.get("status")
    allowed = sorted(ALLOWED_ORDER_STATUSES)
    if new_status not in ALLOWED_ORDER_STATUSES:
        return error(422, f"status must be one of: {', '.join(allowed)}")
    result = update_order_status(order_id, new_status)
    if result is None:
        return error(404, f"Order {order_id} not found")
    if result:
        return jsonify({"status": 200, "message": f"Order {order_id} updated to {new_status}"})
    return error(500, "Failed to update order")


@app.route("/api/orders/<order_id>", methods=["DELETE"])
@roles_required("admin")
def delete_order(order_id):
    result = delete_record("orders", order_id)
    if result is None:
        return error(404, f"Order {order_id} not found")
    if result:
        return jsonify({"status": 200, "message": f"Order {order_id} deleted"})
    return error(500, "Failed to delete order")


# ==================================================
# ROUTES — COLLECTIONS
# ==================================================
@app.route("/api/collections", methods=["GET"])
@login_required
def get_collections():
    collections = scope_to_user(fetch_all("collections"))
    return jsonify({"status": 200, "data": collections})


@app.route("/api/collections", methods=["POST"])
@roles_required("admin", "delivery")
def add_collection():
    data = get_json_body()
    customer_id = clean_str(data, "customer_id")
    if not customer_id:
        return error(422, "customer_id is required")
    try:
        empty_returned = parse_int(data.get("empty_jugs_returned"), default=0)
        filled_released = parse_int(data.get("filled_jugs_released"), default=0)
    except (TypeError, ValueError):
        return error(422, "jug counts must be whole numbers")
    if empty_returned < 0 or filled_released < 0:
        return error(422, "jug counts cannot be negative")

    balance = filled_released - empty_returned
    if balance < 0:
        return error(422, "container_balance cannot be negative")

    new_id = get_next_id("collections", "CL")
    record = {
        "collection_id": new_id,
        "customer_id": customer_id,
        "order_id": clean_str(data, "order_id") or None,
        "empty_jugs_returned": empty_returned,
        "filled_jugs_released": filled_released,
        "container_balance": balance,
        "collection_date": str(datetime.date.today()),
        "collected_by": clean_str(data, "collected_by") or current_user()["name"]
    }
    if insert_record("collections", record):
        return jsonify({"status": 201, "message": f"Collection {new_id} recorded", "data": record}), 201
    return error(500, "Failed to save collection")


# ==================================================
# PAGE ROUTES — serve the HTML frontend
# ==================================================
@app.route("/")
def dashboard():
    if not current_user():
        return redirect(url_for("login_page"))
    return render_template("index.html")


@app.route("/orders")
def orders_page():
    if not current_user():
        return redirect(url_for("login_page"))
    return render_template("orders.html")


@app.route("/login")
def login_page():
    if current_user():
        return redirect(url_for("dashboard"))
    return render_template("login.html", demo_accounts=DEMO_PRESETS)


@app.route("/register")
def register_page():
    if current_user():
        return redirect(url_for("dashboard"))
    return render_template("register.html")


# ==================================================
# AUTHENTICATION API
# ==================================================
@app.route("/api/login", methods=["POST"])
def api_login():
    data = get_json_body()
    email = clean_str(data, "email").lower()
    password = data.get("password") if isinstance(data.get("password"), str) else ""

    user = find_user(email) if email else None
    if user and check_password_hash(user["password_hash"], password):
        session.clear()
        session.permanent = True
        session["user"] = public_user(user)
        return jsonify({"status": 200, "message": "Login successful", "user": session["user"]})
    return error(401, "Invalid email or password")


@app.route("/api/logout", methods=["POST"])
def api_logout():
    session.clear()
    return jsonify({"status": 200, "message": "Logged out"})


@app.route("/api/me", methods=["GET"])
@login_required
def api_me():
    return jsonify({"status": 200, "user": current_user()})


@app.route("/api/register", methods=["POST"])
def api_register():
    data = get_json_body()
    email = clean_str(data, "email").lower()
    password = data.get("password") if isinstance(data.get("password"), str) else ""
    full_name = clean_str(data, "full_name")
    role = clean_str(data, "role").lower() or "customer"

    if not email or not password or not full_name:
        return error(422, "Name, email, and password are required")
    if not EMAIL_RE.match(email):
        return error(422, "Please enter a valid email address")
    if len(password) < MIN_PASSWORD_LENGTH:
        return error(422, f"Password must be at least {MIN_PASSWORD_LENGTH} characters")
    if role not in ROLES:
        return error(422, "role must be customer or delivery")
    if role not in SELF_REGISTER_ROLES:
        return error(403, "Admin accounts cannot be self-registered")
    if find_user(email):
        return error(409, "Account with this email already exists")

    user = create_account(
        email, password, full_name, role,
        contact_number=clean_str(data, "contact_number"),
        address=clean_str(data, "address"),
    )
    if not user:
        return error(500, "Failed to create account")

    session.clear()
    session.permanent = True
    session["user"] = public_user(user)
    return jsonify({
        "status": 201,
        "message": f"Account registered successfully as {role.upper()}",
        "user": session["user"]
    }), 201


# ==================================================
# HEALTH CHECK
# ==================================================
@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({
        "status": 200,
        "message": "AquaFlow Tracker API is running",
        "supabase_connected": supabase is not None,
        "demo_mode": DEMO_MODE,
        "version": "1.1.0"
    })


# Create admin / demo accounts at startup
seed_accounts()


# ==================================================
# ENTRY POINT (local development — production uses gunicorn, see Procfile)
# ==================================================
if __name__ == "__main__":
    app.run(
        host=os.getenv("HOST", "127.0.0.1"),
        port=int(os.getenv("PORT", "5000")),
        debug=env_flag("FLASK_DEBUG"),
    )
