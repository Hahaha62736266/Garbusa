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
