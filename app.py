<<<<<<< HEAD
from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)

# In-memory storage — replace with Supabase/SQLAlchemy later
customers = [
    {"id": "CUST-001", "name": "Maria Santos", "phone": "0917-123-4567", 
     "address": "Poblacion Zone 3, Maramag", "borrowedSlim": 4, "borrowedRound": 2,
     "totalOrders": 38, "balance": 0},
    {"id": "CUST-002", "name": "Barangay Health Center", "phone": "0928-888-9911", 
     "address": "Main St, Maramag", "borrowedSlim": 12, "borrowedRound": 0,
     "totalOrders": 112, "balance": 350},
    {"id": "CUST-003", "name": "Juan Dela Cruz", "phone": "0905-555-2233", 
     "address": "Subdivision Phase 2, Maramag", "borrowedSlim": 2, "borrowedRound": 1,
     "totalOrders": 14, "balance": 0},
    {"id": "CUST-004", "name": "Garbusa Eatery", "phone": "0919-777-3344", 
     "address": "Public Market Site, Maramag", "borrowedSlim": 8, "borrowedRound": 5,
     "totalOrders": 85, "balance": 120},
]
orders = []
expenses = [
    {"id": 1, "category": "Electricity", "amount": 3400, "note": "Power bill for RO Filtration Pumps", "date": "2026-10-01"},
    {"id": 2, "category": "Gasoline", "amount": 850, "note": "Delivery Trike Refuel", "date": "2026-10-02"},
    {"id": 3, "category": "Staff Payroll", "amount": 1500, "note": "Daily wages", "date": "2026-10-02"},
    {"id": 4, "category": "Filter Replacement", "amount": 1200, "note": "Sediment Pre-Filter", "date": "2026-09-28"},
]
station = {
    "purified_tank_liters": 3800,
    "tds": 12,
    "ph": 7.4,
    "turbidity": 0.2,
    "raw_water_meter": 14520,
    "purified_water_meter": 11840
}

# ========== API ROUTES ==========
@app.route("/api/customers", methods=["GET"])
def list_customers():
    return jsonify(customers)

@app.route("/api/customers/<customer_id>/return", methods=["POST"])
def record_return(customer_id):
    data = request.json
    for c in customers:
        if c["id"] == customer_id:
            c["borrowedSlim"] = max(0, c["borrowedSlim"] - data.get("slim_returned", 0))
            c["borrowedRound"] = max(0, c["borrowedRound"] - data.get("round_returned", 0))
            return jsonify({"message": "Recorded", "customer": c})
    return jsonify({"error": "Not found"}), 404

@app.route("/api/orders", methods=["GET"])
def list_orders():
    return jsonify(orders)

@app.route("/api/orders", methods=["POST"])
def create_order():
    order = request.json
    orders.insert(0, order)
    return jsonify(order), 201

@app.route("/api/orders/<order_id>/status", methods=["POST"])
def update_status(order_id):
    data = request.json
    for o in orders:
        if o["id"] == order_id:
            o["status"] = data["status"]
            return jsonify(o)
    return jsonify({"error": "Not found"}), 404

@app.route("/api/orders/<order_id>/payment", methods=["POST"])
def update_payment(order_id):
    data = request.json
    for o in orders:
        if o["id"] == order_id:
            o["paymentStatus"] = data["payment_status"]
            return jsonify(o)
    return jsonify({"error": "Not found"}), 404

@app.route("/api/expenses", methods=["GET"])
def list_expenses():
    return jsonify(expenses)

@app.route("/api/expenses", methods=["POST"])
def add_expense():
    exp = request.json
    exp["id"] = len(expenses) + 1
    expenses.insert(0, exp)
    return jsonify(exp), 201

@app.route("/api/station", methods=["GET"])
def get_station():
    return jsonify(station)

@app.route("/api/station/meters", methods=["POST"])
def update_meters():
    data = request.json
    station["raw_water_meter"] = data.get("raw_water_meter", station["raw_water_meter"])
    station["purified_water_meter"] = data.get("purified_water_meter", station["purified_water_meter"])
    return jsonify(station)

if __name__ == "__main__":
    print("💧 AquaFlow Backend Starting...")
    app.run(debug=True, port=5000)
=======
from flask import Flask
app = Flask(__name__)

@app.route('/')
def home():
    return "<h1 style='color:green;'>✅ Garbusa IS WORKING!</h1><p>Go to <a href='/dashboard'>/dashboard</a></p>"

@app.route('/dashboard')
def dashboard():
    return """
    <h1>💧 Acquaflow Tracking Dashboard</h1>
    <p>If you see this, your setup is correct!</p>
    <form method='POST'>
      <div>
        <label>Location:</label>
        <input type='text' name='location'>
      </div>
      <div>
        <label>Water Level:</label>
        <input type='number' step='0.01' name='water_level'>
      </div>
      <button type='submit'>Submit</button>
    </form>
    """

@app.route('/dashboard', methods=['POST'])
def dashboard_submit():
    loc = request.form.get('location')
    level = request.form.get('water_level')
    return f"<h3>✅ Saved!</h3><p>Location: {loc}<br>Level: {level}m</p>"

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, use_reloader=False, port=5000)
>>>>>>> a9e222e (Flask base server working)
