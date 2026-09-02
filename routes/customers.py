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
