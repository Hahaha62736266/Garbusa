from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy

from flask import Flask, render_template, request, redirect, url_for, flash, get_flashed_messages
from models import FarmRecord, records_db

app = Flask(__name__)
app.secret_key = "dev_only_replace_in_production"  # Required for flash messages

def validate_record(data):
    """Return dict of field errors; empty dict = valid"""
    errors = {}
    name = data.get("name", "").strip()
    location = data.get("location", "").strip()
    area_raw = data.get("area_ha", "").strip()

    if not name:
        errors["name"] = "Name is required"
    if len(location) < 6:
        errors["location"] = "Location must be at least 6 characters"
    if not area_raw:
        errors["area_ha"] = "Area is required"
    else:
        try:
            area_val = float(area_raw)
            if area_val <= 0:
                errors["area_ha"] = "Area must be greater than 0"
        except ValueError:
            errors["area_ha"] = "Must be a valid number"
    return errors

@app.route("/")
def index():
    return render_template("index.html", records=records_db)

@app.route("/create", methods=["GET", "POST"])
def create():
    if request.method == "POST":
        errors = validate_record(request.form)
        if errors:
            # 422 = Unprocessable Entity → matches test requirement
            return render_template("create.html", errors=errors, form_data=request.form), 422
        
        rec = FarmRecord(
            name=request.form["name"],
            record_type=request.form.get("record_type", ""),
            location=request.form["location"],
            area_ha=float(request.form["area_ha"]),
            primary_crop=request.form.get("primary_crop", ""),
            notes=request.form.get("notes", "")
        )
        records_db.append(rec)
        flash("Record created successfully!", "success")
        return redirect(url_for("index"))
    
    return render_template("create.html", errors={}, form_data={})

@app.route("/edit/<record_id>", methods=["GET", "POST"])
def edit(record_id):
    rec = next((r for r in records_db if r.id == record_id), None)
    if not rec:
        flash("Record not found", "error")
        return redirect(url_for("index"))

    if request.method == "POST":
        errors = validate_record(request.form)
        if errors:
            return render_template("edit.html", errors=errors, record=rec, form_data=request.form), 422
        
        rec.name = request.form["name"]
        rec.record_type = request.form.get("record_type", "")
        rec.location = request.form["location"]
        rec.area_ha = float(request.form["area_ha"])
        rec.primary_crop = request.form.get("primary_crop", "")
        rec.notes = request.form.get("notes", "")
        flash("Record updated successfully!", "success")
        return redirect(url_for("index"))
    
    # Pre‑populate form with existing values
    form_defaults = {
        "name": rec.name,
        "record_type": rec.record_type,
        "location": rec.location,
        "area_ha": str(rec.area_ha),
        "primary_crop": rec.primary_crop,
        "notes": rec.notes,
    }
    return render_template("edit.html", errors={}, record=rec, form_data=form_defaults)

@app.route("/delete/<record_id>", methods=["POST"])
def delete(record_id):
    global records_db
    records_db = [r for r in records_db if r.id != record_id]
    flash("Record deleted", "info")
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)

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
    location = db.Column(db.String(100), nullable=True)  # ← Your original field
    flow_rate = db.Column(db.Float, nullable=False)
    water_level = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(30), nullable=False)
    notes = db.Column(db.Text, nullable=True)
    recorded_at = db.Column(db.DateTime, default=db.func.now())

    def to_dict(self):
        return {
            "id": self.id,
            "device_id": self.device_id,
            "location": self.location,  # ← Included
            "flow_rate": self.flow_rate,
            "water_level": self.water_level,
            "status": self.status,
            "notes": self.notes,
            "recorded_at": self.recorded_at.strftime('%Y-%m-%d %H:%M:%S')
        }

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
# First route
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

# Second route — change function name
@app.route('/dashboard/stats')
def dashboard_stats():  # ✅ Unique name
    return render_template('stats.html')
    
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
        # ✅ PASTE YOUR CODE HERE — between these lines
        new_record = AquaFlowRecord(
            device_id=data.get('device_id',''),
            location=data.get('location',''),
            flow_rate=float(data['flow_rate']),
            water_level=float(data['water_level']),
            status=data['status'],
            notes=data.get('notes','')
        )
        # ✅ End of paste section
        
        db.session.add(new_record)
        db.session.commit()

        # Success Response
        return jsonify({
            "success": True,
            "message": "Aqua Flow record saved successfully!",
            "data": new_record.to_dict()
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({
            "success": False,
            "message": "System error. Could not save record. Please try again."
        }), 500
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
