from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# ------------------------------
# Database Configuration
# ------------------------------
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///aqua_flow.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# ------------------------------
# Aqua Flow Record Model
# ------------------------------
class AquaFlowRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    device_id = db.Column(db.String(50), nullable=False)
    flow_rate = db.Column(db.Float, nullable=False)
    water_level = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(30), nullable=False)
    notes = db.Column(db.Text, nullable=True)
    recorded_at = db.Column(db.DateTime, default=db.func.now())

    def to_dict(self):
        return {
            "id": self.id,
            "device_id": self.device_id,
            "flow_rate": self.flow_rate,
            "water_level": self.water_level,
            "status": self.status,
            "notes": self.notes,
            "recorded_at": self.recorded_at.strftime('%Y-%m-%d %H:%M:%S')
        }

# ------------------------------
# Create Database Tables
# ------------------------------
with app.app_context():
    db.create_all()

# ------------------------------
# Landing Page
# ------------------------------
@app.route('/')
def home():
    return render_template('index.html')

# ------------------------------
# Dashboard Page
# ------------------------------
@app.route('/dashboard')
def dashboard():
    # Get all records from DB (newest first)
    records = AquaFlowRecord.query.order_by(AquaFlowRecord.recorded_at.desc()).all()
    
    # Statistics
    total = len(records)
    normal_count = sum(1 for r in records if r.status == 'normal')
    low_flow_count = sum(1 for r in records if r.status == 'low_flow')
    high_flow_count = sum(1 for r in records if r.status == 'high_flow')
    alert_count = sum(1 for r in records if r.status == 'alert')
    
    stats = {
        "total_records": total,
        "normal": normal_count,
        "low_flow": low_flow_count,
        "high_flow": high_flow_count,
        "alert": alert_count
    }
    
    return render_template('dashboard.html', records=records, stats=stats)

# ------------------------------
# API: Get All Records
# ------------------------------
@app.route('/api/aqua-flow/records', methods=['GET'])
def get_records():
    try:
        records = AquaFlowRecord.query.order_by(AquaFlowRecord.recorded_at.desc()).all()
        return jsonify({
            "success": True,
            "count": len(records),
            "data": [r.to_dict() for r in records]
        }), 200
    except Exception as e:
        return jsonify({"success": False, "message": "Failed to load records"}), 500

# ------------------------------
# API: Create New Record
# ------------------------------
@app.route('/api/aqua-flow', methods=['POST'])
def create_record():
    data = request.get_json() or {}
    errors = {}

    # Validation
    if not data.get('device_id'):
        errors['device_id'] = ["Device ID is required"]
    if not data.get('flow_rate'):
        errors['flow_rate'] = ["Flow rate is required"]
    elif not isinstance(data.get('flow_rate'), (int, float)):
        errors['flow_rate'] = ["Flow rate must be a valid number"]
    if not data.get('water_level'):
        errors['water_level'] = ["Water level is required"]
    elif not isinstance(data.get('water_level'), (int, float)):
        errors['water_level'] = ["Water level must be a valid number"]
    if not data.get('status'):
        errors['status'] = ["Status is required"]

    # 422 Validation Error
    if errors:
        return jsonify({
            "success": False,
            "message": "Please fix the errors below",
            "errors": errors
        }), 422

    try:
        # Save to Database
        new_record = AquaFlowRecord(
            device_id=data['device_id'],
            flow_rate=float(data['flow_rate']),
            water_level=float(data['water_level']),
            status=data['status'],
            notes=data.get('notes', '')
        )
        db.session.add(new_record)
        db.session.commit()

        # Success Response
        return jsonify({
            "success": True,
            "message": "Aqua Flow record saved successfully!",
            "data": new_record.to_dict()
        }), 201

    except Exception as e:
        # 500 Server Error
        db.session.rollback()
        return jsonify({
            "success": False,
            "message": "System error. Could not save record. Please try again."
        }), 500

if __name__ == '__main__':
    app.run(debug=True)
