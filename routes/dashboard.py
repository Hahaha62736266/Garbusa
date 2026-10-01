from flask import Blueprint, render_template, request, jsonify

bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')

# ─── Standard Response Helpers ───
def success_response(data=None, message="Success", status=200):
    return jsonify({
        "success": True,
        "message": message,
        "data": data or {}
    }), status

def validation_error(errors, message="Validation failed"):
    return jsonify({
        "success": False,
        "message": message,
        "errors": errors
    }), 422

def server_error(message="An unexpected error occurred"):
    return jsonify({
        "success": False,
        "message": message
    }), 500

# ─── Dashboard Page ───
@bp.route('/')
def main():
    return render_template('dashboard.html')

# ─── Acquaflow Tracking Submit ───
@bp.route('/acquaflow/submit', methods=['POST'])
def acquaflow_submit():
    try:
        data = request.form or request.json

        # 1. Validation
        errors = {}
        if not data.get('location'):
            errors['location'] = "Location is required"
        if not data.get('water_level'):
            errors['water_level'] = "Water level reading is required"
        if data.get('water_level') and float(data.get('water_level', 0)) < 0:
            errors['water_level'] = "Water level cannot be negative"

        if errors:
            return validation_error(errors)

        # 2. Process & Save (replace with your Supabase code)
        reading = {
            "location": data.get('location'),
            "water_level": data.get('water_level'),
            "status": data.get('status', 'normal')
        }

        # TODO: Add Supabase insert here
        # supabase.table("acquaflow_readings").insert(reading).execute()

        return success_response(
            data={"reading": reading, "tracking_id": "AF-" + str(hash(str(reading)))[-6:]},
            message="✅ Acquaflow reading recorded successfully!"
        )

    except Exception as e:
        print("[SERVER ERROR]", str(e))
        return server_error()
