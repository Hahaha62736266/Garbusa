from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)

# ========== HELPER: PAYLOAD VALIDATION ==========
def validate_json_payload(required_fields=None):
    """
    Validate incoming JSON payload.
    - Returns (data, None) if valid
    - Returns (None, error_response) if invalid → caller returns immediately
    """
    data = request.json
    if not data:
        return None, {"error": "Empty payload — JSON body required"}, 400
    
    if required_fields:
        missing = [field for field in required_fields if field not in data or str(data[field]).strip() == ""]
        if missing:
            return None, {"error": f"Missing or empty required fields: {', '.join(missing)}"}, 400
    
    return data, None

# ========== IN-MEMORY DATA STORE ==========
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

# ========== WEB DASHBOARD ROUTES ==========
@app.route('/')
def home():
    return "<h1 style='color:green;'>✅ Garbusa IS WORKING!</h1><p>Go to <a href='/dashboard'>/dashboard</a> or <a href='/api/customers'>/api/customers</a></p>"

@app.route('/dashboard')
def dashboard():
    return """
    <h1>💧 Aquaflow Tracking Dashboard</h1>
    <p>If you see this, your setup is correct!</p>
    <form method='POST'>
      <div>
        <label>Location:</label>
        <input type='text' name='location' required>
      </div>
      <div>
        <label>Water Level (m):</label>
        <input type='number' step='0.01' name='water_level' required>
      </div>
      <button type='submit'>Submit</button>
    </form>
    """

@app.route('/dashboard', methods=['POST'])
def dashboard_submit():
    loc = request.form.get('location', '').strip()
    level = request.form.get('water_level', '').strip()
    
    if not loc or not level:
        return "<h3 style='color:red;'>❌ Error: Both fields are required!</h3><a href='/dashboard'>Go back</a>"
    
    return f"<h3>✅ Saved!</h3><p>Location: {loc}<br>Level: {level}m</p><a href='/dashboard'>Submit another</a>"

# ========== API ROUTES ==========
@app.route("/api/customers", methods=["GET"])
def list_customers():
    return jsonify(customers)

@app.route("/api/customers/<customer_id>/return", methods=["POST"])
def record_return(customer_id):
    data, err = validate_json_payload()
    if err: return jsonify(err[0]), err[1]
    
    for c in customers:
        if c["id"] == customer_id:
            c["borrowedSlim"] = max(0, c["borrowedSlim"] - data.get("slim_returned", 0))
            c["borrowedRound"] = max(0, c["borrowedRound"] - data.get("round_returned", 0))
            return jsonify({"message": "Recorded", "customer": c})
    return jsonify({"error": "Customer not found"}), 404

@app.route("/api/orders", methods=["GET"])
def list_orders():
    return jsonify(orders)

@app.route("/api/orders", methods=["POST"])
def create_order():
    data, err = validate_json_payload(["customer_id", "product_id", "quantity"])
    if err: return jsonify(err[0]), err[1]
    
    order = {
        "id": f"O{len(orders)+1:03d}",
        "customer_id": data["customer_id"],
        "product_id": data["product_id"],
        "quantity": data["quantity"],
        "total_amount": data.get("total_amount"),
        "order_date": datetime.now().strftime("%Y-%m-%d"),
        "status": data.get("status", "Pending"),
        "paymentStatus": data.get("payment_status", "Unpaid")
    }
    orders.insert(0, order)
    return jsonify(order), 201

@app.route("/api/orders/<order_id>/status", methods=["POST"])
def update_status(order_id):
    data, err = validate_json_payload(["status"])
    if err: return jsonify(err[0]), err[1]
    
    for o in orders:
        if o["id"] == order_id:
            o["status"] = data["status"]
            return jsonify(o)
    return jsonify({"error": "Order not found"}), 404

@app.route("/api/orders/<order_id>/payment", methods=["POST"])
def update_payment(order_id):
    data, err = validate_json_payload(["payment_status"])
    if err: return jsonify(err[0]), err[1]
    
    for o in orders:
        if o["id"] == order_id:
            o["paymentStatus"] = data["payment_status"]
            return jsonify(o)
    return jsonify({"error": "Order not found"}), 404

@app.route("/api/expenses", methods=["GET"])
def list_expenses():
    return jsonify(expenses)

@app.route("/api/expenses", methods=["POST"])
def add_expense():
    data, err = validate_json_payload(["category", "amount"])
    if err: return jsonify(err[0]), err[1]
    
    exp = {
        "id": len(expenses) + 1,
        "category": data["category"],
        "amount": float(data["amount"]),
        "note": data.get("note", ""),
        "date": data.get("date", datetime.now().strftime("%Y-%m-%d"))
    }
    expenses.insert(0, exp)
    return jsonify(exp), 201

@app.route("/api/station", methods=["GET"])
def get_station():
    return jsonify(station)

@app.route("/api/station/meters", methods=["POST"])
def update_meters():
    data, err = validate_json_payload()
    if err: return jsonify(err[0]), err[1]
    
    if "raw_water_meter" not in data and "purified_water_meter" not in data:
        return jsonify({"error": "Provide at least one meter reading"}), 400
    
    if "raw_water_meter" in data:
        station["raw_water_meter"] = data["raw_water_meter"]
    if "purified_water_meter" in data:
        station["purified_water_meter"] = data["purified_water_meter"]
    
    return jsonify(station)

if __name__ == "__main__":
    print("💧 AquaFlow Backend Starting...")
    app.run(host="0.0.0.0", debug=True, use_reloader=False, port=5000)