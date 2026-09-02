# routes/customers.py (example wiring)
from middleware.validation import validateCustomerCreate
from controllers.customer_controller import createCustomer

def POST_customers(request):
    # Step 1: Run validation FIRST
    error = validateCustomerCreate(request)
    if error:
        return error  # ❌ Returns 422 — NEVER reaches controller

    # Step 2: Only if NO error → call controller
    return createCustomer(request)  # ✅ request.validatedBody already set

# routes/customers.py — DELETE example
from middleware.validation import authorizeDeleteCustomer
from controllers.customer_controller import deleteCustomer

def DELETE_customers(request):
    # Step 1: VALIDATION (if needed) → 422
    # Step 2: AUTHORIZATION → 403
    authError = authorizeDeleteCustomer(request)
    if authError:
        return authError  # ❌ 403 FORBIDDEN — never reaches controller

    # Step 3: Only if ALLOWED → call controller
    return deleteCustomer(request)  # ✅ Permission granted

# ==========================================================
# ROUTES: Customers
# Pipeline: Validation → Authorization → Controller
# ==========================================================

from middleware.validation import (
    validateCustomerCreate,
    validateCustomerUpdate,
    authorizeDeleteCustomer
)
from controllers.customer_controller import (
    listCustomers,
    showCustomer,
    createCustomer,
    updateCustomer,
    deleteCustomer
)

def GET_customers(request):
    """GET /customers — List all"""
    return listCustomers(request)

def GET_customer_by_id(request):
    """GET /customers/:customer_id — Show one"""
    return showCustomer(request)

def POST_customers(request):
    """POST /customers — Create (validate → controller)"""
    # Step 1: Validate input → returns 422 if invalid
    error = validateCustomerCreate(request)
    if error:
        return error

    # Step 2: Valid → pass to controller
    return createCustomer(request)

def PUT_customer_by_id(request):
    """PUT /customers/:customer_id — Update (validate → controller)"""
    # Step 1: Validate input → 422
    error = validateCustomerUpdate(request)
    if error:
        return error

    # Step 2: Valid → pass to controller
    return updateCustomer(request)

def DELETE_customer_by_id(request):
    """DELETE /customers/:customer_id — Delete (validate → authorize → controller)"""
    # Step 1: Authorization → 403 if not owner
    authError = authorizeDeleteCustomer(request)
    if authError:
        return authError

    # Step 2: Allowed → pass to controller
    return deleteCustomer(request)
