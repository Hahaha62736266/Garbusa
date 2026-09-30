from flask import Blueprint, request
from middleware.validation import validate_customer_data
from middleware.auth_guard import require_auth
from controllers import customer_controller

customer_bp = Blueprint("customers", __name__)

# CREATE — with validation + auth guard
@customer_bp.route("/", methods=["POST"])
@require_auth  # ✅ Authorization guard → returns 403 if unauthorized
def create_customer():
    data = request.get_json()
    validation_error = validate_customer_data(data)
    
    if validation_error:
        return validation_error, 422  # ✅ Consistent 422 shape, no 500/crash
    
    result = customer_controller.create_customer(data)
    return result, 201

# UPDATE — with validation + auth guard
@customer_bp.route("/<customer_id>", methods=["PUT"])
@require_auth
def update_customer(customer_id):
    data = request.get_json()
    validation_error = validate_customer_data(data, is_update=True)
    
    if validation_error:
        return validation_error, 422  # ✅ Consistent error handling
    
    result = customer_controller.update_customer(customer_id, data)
    return result, 200