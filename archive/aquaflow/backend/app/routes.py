from flask import Blueprint, jsonify, request

api_bp = Blueprint("api", __name__)

# ------------------------------
# DASHBOARD STATS
# ------------------------------
@api_bp.route("/dashboard/stats", methods=["GET"])
def dashboard_stats():
    return jsonify({
        today_orders: 24,
        active_stations: 8,
        water_stock_liters: 4250,
        monthly_revenue: 28450
    })

# ------------------------------
# ORDERS
# ------------------------------
@api_bp.route("/orders", methods=["GET"])
def get_orders():
    orders = [
        {"id": 1, "customer": "Maria Santos", "liters": 20, "status": "delivered", "date": "2026-10-03"},
        {"id": 2, "customer": "Juan Dela Cruz", "liters": 10, "status": "pending", "date": "2026-10-03"},
        {"id": 3, "customer": "Ana Reyes", "liters": 30, "status": "delivered", "date": "2026-10-02"}
    ]
    return jsonify(orders)

@api_bp.route("/orders", methods=["POST"])
def create_order():
    data = request.get_json()
    if not data or "customer" not in data or "liters" not in data:
        return jsonify({"error": "Missing customer or liters"}), 400

    new_order = {
        "id": 4,
        "customer": data["customer"],
        "liters": data["liters"],
        "status": "pending",
        "date": "2026-10-03"
    }
    return jsonify(new_order), 201

# ------------------------------
# INVENTORY
# ------------------------------
@api_bp.route("/inventory", methods=["GET"])
def get_inventory():
    items = [
        {"id": 1, "item": "5-Gallon Bottle", "stock": 120, "price": 35.00},
        {"id": 2, "item": "Refill (5Gal)", "stock": 4250, "price": 20.00},
        {"id": 3, "item": "250ml Pouch", "stock": 500, "price": 10.00}
    ]
    return jsonify(items)

# ------------------------------
# USERS
# ------------------------------
@api_bp.route("/users", methods=["GET"])
def get_users():
    users = [
        {"id": 1, "name": "Admin", "role": "admin", "station": "Main Branch"},
        {"id": 2, "name": "Jayson", "role": "manager", "station": "Cagayan de Oro"},
        {"id": 3, "name": "Delivery Team A", "role": "staff", "station": "Main Branch"}
    ]
    return jsonify(users)
