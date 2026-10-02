from flask import jsonify, request

from flask import Flask, jsonify, request
from your_app import db  # import your SQLAlchemy instance

# Aqua Flow Record Model (if not already defined)
class AquaFlowRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    device_id = db.Column(db.String(50), nullable=False)
    flow_rate = db.Column(db.Float, nullable=False)
    water_level = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(30), nullable=False)
    notes = db.Column(db.Text, nullable=True)
    recorded_at = db.Column(db.DateTime, default=db.func.now())

# ------------------------------
# Submit Route
# ------------------------------
@app.route('/api/aqua-flow', methods=['POST'])
def create_aqua_flow():
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

    # 🔴 422 Validation Errors
    if errors:
        return jsonify({
            "success": False,
            "message": "Please fix the errors below",
            "errors": errors
        }), 422

    try:
        # Save record
        new_record = AquaFlowRecord(
            device_id=data['device_id'],
            flow_rate=float(data['flow_rate']),
            water_level=float(data['water_level']),
            status=data['status'],
            notes=data.get('notes', '')
        )
        db.session.add(new_record)
        db.session.commit()

        # ✅ Success Response
        return jsonify({
            "success": True,
            "message": "Aqua Flow record saved successfully!",
            "data": {
                "id": new_record.id,
                "device_id": new_record.device_id,
                "recorded_at": new_record.recorded_at.strftime('%Y-%m-%d %H:%M:%S')
            }
        }), 201

    except Exception as e:
        # 🔴 500 Server Error
        db.session.rollback()
        return jsonify({
            "success": False,
            "message": "System error. Could not save record. Please try again."
        }), 500

# ------------------------------
# Aqua Flow Tracking — Submit Route
# ------------------------------
@app.route('/api/aqua-flow', methods=['POST'])
def create_aqua_record():
    data = request.get_json() or {}
    errors = {}

    # --- Validation Rules ---
    if not data.get('device_id'):
        errors['device_id'] = ["Device ID is required"]
    if not data.get('flow_rate'):
        errors['flow_rate'] = ["Flow rate is required"]
    elif not isinstance(data.get('flow_rate'), (int, float)):
        errors['flow_rate'] = ["Flow rate must be a valid number"]
    if not data.get('water_level'):
        errors['water_level'] = ["Water level is required"]
    if not data.get('status'):
        errors['status'] = ["Status is required"]

    # 🔴 422 — Validation Errors
    if errors:
        return jsonify({
            "success": False,
            "message": "Please fix the errors below",
            "errors": errors
        }), 422

    try:
        # --- Save to Database ---
        new_record = AquaFlowRecord(
            device_id=data['device_id'],
            flow_rate=data['flow_rate'],
            water_level=data['water_level'],
            status=data['status'],
            notes=data.get('notes', '')
        )
        db.session.add(new_record)
        db.session.commit()

        # ✅ Success Response
        return jsonify({
            "success": True,
            "message": "Aqua Flow record saved successfully!",
            "data": {
                "id": new_record.id,
                "device_id": new_record.device_id,
                "recorded_at": new_record.recorded_at.isoformat() if hasattr(new_record, 'recorded_at') else None
            }
        }), 201

    except Exception as e:
        # 🔴 500 — Server/DB Error
        db.session.rollback()
        return jsonify({
            "success": False,
            "message": "System error. Could not save record. Please try again."
        }), 500
