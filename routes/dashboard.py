<<<<<<< HEAD
from flask import Blueprint, render_template, request, jsonify
import os
from dotenv import load_dotenv

load_dotenv()

bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')

# ─── Initialize Supabase ───
try:
    from supabase import create_client, Client
    SUPABASE_URL = os.getenv("SUPABASE_URL")
    SUPABASE_KEY = os.getenv("SUPABASE_ANON_KEY")
    
    if SUPABASE_URL and SUPABASE_KEY:
        supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
        print("✅ Supabase connected successfully")
    else:
        supabase = None
        print("⚠️ Supabase credentials missing — running without database")
        
except Exception as e:
    supabase = None
    print(f"⚠️ Supabase init failed: {e}")

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
        location = data.get('location', '').strip()
        water_level = data.get('water_level', '').strip()
        status = data.get('status', 'normal')

        if not location:
            errors['location'] = "Location is required"
        if not water_level:
            errors['water_level'] = "Water level reading is required"
        else:
            try:
                water_level_float = float(water_level)
                if water_level_float < 0:
                    errors['water_level'] = "Water level cannot be negative"
            except ValueError:
                errors['water_level'] = "Please enter a valid number"

        if errors:
            return validation_error(errors)

        # 2. Prepare data
        reading = {
            "location": location,
            "water_level": float(water_level),
            "status": status,
            "recorded_at": "now()"  # Supabase will handle timestamp
        }

        # 3. Save to Supabase
        if supabase:
            result = supabase.table("acquaflow_readings").insert(reading).execute()
            
            if result.data:
                return success_response(
                    data={
                        "id": result.data[0].get('id'),
                        "reading": reading
                    },
                    message="✅ Acquaflow reading recorded successfully!"
                )
            else:
                return server_error("Failed to save reading — no response from database")
        else:
            # Development fallback without DB
            return success_response(
                data={"reading": reading, "note": "Demo mode — not saved to DB"},
                message="✅ Reading validated (demo mode)"
            )

    except Exception as e:
        print("[SERVER ERROR]", str(e))
        return server_error(f"Error: {str(e)}")
=======
from flask import Blueprint, render_template

bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')

@bp.route('/')
def main():
    return render_template('dashboard.html')
>>>>>>> a9e222e (Flask base server working)
