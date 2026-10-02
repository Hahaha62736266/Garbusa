from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy

# ==============================================
# ONE App — Only One Place
# ==============================================
app = Flask(__name__)
app.secret_key = "dev_only_replace_in_production"

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///aqua_flow.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# ==============================================
# Farm Records
# ==============================================
class FarmRecord:
    def __init__(self, rid, name, record_type, location, area_ha, primary_crop, notes):
        self.id = rid
        self.name = name
        self.record_type = record_type
        self.location = location
        self.area_ha = area_ha
        self.primary_crop = primary_crop
        self.notes = notes

records_db = []
record_counter = 1


def validate_record(data):
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

# ==============================================
# AquaFlow Model — Only One Definition
# ==============================================
class AquaFlowRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    device_id = db.Column(db.String(50), nullable=False)
    location = db.Column(db.String(100), nullable=True)
    flow_rate = db.Column(db.Float, nullable=False)
    water_level = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(30), nullable=False)
    notes = db.Column(db.Text, nullable=True)
    recorded_at = db.Column(db.DateTime, default=db.func.now())

    def to_dict(self):
        return {
            "id": self.id,
            "device_id": self.device_id,
            "location": self.location,
            "flow_rate": self.flow_rate,
            "water_level": self.water_level,
            "status": self.status,
            "notes": self.notes,
            "recorded_at": self.recorded_at.strftime('%Y-%m-%d %H:%M:%S')
        }

with app.app_context():
    db.create_all()

# ==============================================
# ROUTES — All Unique, No Duplicates
# ==============================================

@app.route("/")
def index():
    return render_template("index.html", records=records_db)

@app.route("/create", methods=["GET", "POST"])
def create():
    global record_counter
    if request.method == "POST":
        errors = validate_record(request.form)
        if errors:
            return render_template("create.html", errors=errors, form_data=request.form), 422
        rec = FarmRecord(
            rid=str(record_counter),
            name=request.form["name"],
            record_type=request.form.get("record_type", ""),
            location=request.form["location"],
            area_ha=float(request.form["area_ha"]),
            primary_crop=request.form.get("primary_crop", ""),
            notes=request.form.get("notes", "")
        )
        record_counter += 1
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

# --- DASHBOARD — ONLY ONE ---
@app.route('/dashboard')
def dashboard():
    records = AquaFlowRecord.query.all()
    stats = {
        "total_records": len(records),
        "normal": sum(1 for r in records if r.status == 'normal'),
        "low_flow": sum(1 for r in records if r.status == 'low_flow'),
        "high_flow": sum(1 for r in records if r.status == 'high_flow'),
        "alert": sum(1 for r in records if r.status == 'alert')
    }
    return render_template('dashboard.html', records=records, stats=stats)

@app.route('/dashboard/stats')
def dashboard_stats_page():  # ✅ Unique name — NO conflict
    return render_template('stats.html')

# --- API — Only One ---
@app.route('/api/aqua-flow', methods=['POST'])
def create_aqua_record():
    data = request.get_json() or {}
    errors = {}
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
    if errors:
        return jsonify({"success": False, "message": "Please fix the errors below", "errors": errors}), 422
    try:
        new_record = AquaFlowRecord(
            device_id=data.get('device_id', ''),
            location=data.get('location', ''),
            flow_rate=float(data['flow_rate']),
            water_level=float(data['water_level']),
            status=data['status'],
            notes=data.get('notes', '')
        )
        db.session.add(new_record)
        db.session.commit()
        return jsonify({"success": True, "message": "Aqua Flow record saved!", "data": new_record.to_dict()}), 201
    except Exception:
        db.session.rollback()
        return jsonify({"success": False, "message": "System error. Could not save record."}), 500

# ==============================================
# ONE Run — Only At Bottom
# ==============================================
if __name__ == '__main__':
    app.run(debug=True)
