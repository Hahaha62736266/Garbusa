def updateCustomer(request):
    data = request.body or {}
    customer_id = request.params.get("customer_id", "")  # ← ID from URL
                                                          #
    # ==================================================
    # ✅ PASTE EVERYTHING BELOW THIS LINE ↓
    # ==================================================

        # 🔒 AUTHORIZATION GUARD — Only owner can delete
    current_user_id = request.headers.get("X-User-ID", "")  # ← Current logged-in user
    target_customer_id = customer_id  # ← Record being deleted

    # If current user does NOT own this record → FORBIDDEN
    if current_user_id != target_customer_id:
        return {
            "status": 403,
            "error": "You are not allowed to delete this record",
            "field": "authorization"
        }, 403

    # ✅ ALLOWED — proceed with delete

    def deleteCustomer(request):
    customer_id = request.params.get("customer_id", "")  # ← from URL

    # 🔒 Authorization Guard — RUNS FIRST
    current_user_id = request.headers.get("X-User-ID", "")
    if current_user_id != customer_id:
        return {
            "status": 403,
            "error": "You are not allowed to delete this record",
            "field": "authorization"
        }, 403

    # ✅ Allowed → run validation → then delete
    # ... your existing delete code runs here ...

       # 🔒 GUARD CLAUSES — Validation checks FIRST
    import re

    # Validate URL customer_id FIRST
    if not re.match(r"^C\d{3}$", customer_id):
        return {"status": 422, "error": "customer_id must be C followed by 3 digits (e.g. C001)", "field": "customer_id"}

    # Validate full_name IF provided
    if "full_name" in data:
        if not isinstance(data["full_name"], str) or len(data["full_name"]) < 2 or len(data["full_name"]) > 100:
            return {"status": 422, "error": "full_name must be 2–100 characters", "field": "full_name"}

    # Validate contact_number IF provided
    if "contact_number" in data:
        if not re.match(r"^09\d{2}-\d{3}-\d{4}$", data["contact_number"]):
            return {"status": 422, "error": "contact_number must use format 09XX-XXX-XXXX", "field": "contact_number"}

    # Validate address IF provided
    if "address" in data and len(data["address"]) < 5:
        return {"status": 422, "error": "address must be at least 5 characters", "field": "address"}

    # Validate container_owned IF provided
    if "container_owned" in data:
        if not isinstance(data["container_owned"], int) or data["container_owned"] < 0:
            return {"status": 422, "error": "container_owned must be a non-negative integer", "field": "container_owned"}

    # ✅ ALL VALIDATION PASSED — your existing code below runs now
def createProduct(request):
    data = request.body or {}

    # 🔒 GUARDS
    if not data.get("product_id"):
        return {"status":422, "error":"product_id is required", "field":"product_id"}
    if not re.match(r"^P\d{3}$", data["product_id"]):
        return {"status":422, "error":"product_id must be P###", "field":"product_id"}

    if not data.get("product_name"):
        return {"status":422, "error":"product_name is required", "field":"product_name"}
    if len(data["product_name"]) < 2 or len(data["product_name"]) > 100:
        return {"status":422, "error":"product_name must be 2–100 chars", "field":"product_name"}

    if "price_per_unit" not in data:
        return {"status":422, "error":"price_per_unit is required", "field":"price_per_unit"}
    if data["price_per_unit"] < 0:
        return {"status":422, "error":"price must be ≥ 0", "field":"price_per_unit"}

    if "stock_available" not in data:
        return {"status":422, "error":"stock_available is required", "field":"stock_available"}
    if data["stock_available"] < 0:
        return {"status":422, "error":"stock must be ≥ 0", "field":"stock_available"}

    # ✅ Proceed to create...

def createOrder(request):
    data = request.body or {}

    # 🔒 GUARDS
    if not data.get("order_id"):
        return {"status":422, "error":"order_id is required", "field":"order_id"}
    if not re.match(r"^O\d{3}$", data["order_id"]):
        return {"status":422, "error":"order_id must be O###", "field":"order_id"}

    if not data.get("customer_id"):
        return {"status":422, "error":"customer_id is required", "field":"customer_id"}
    if not re.match(r"^C\d{3}$", data["customer_id"]):
        return {"status":422, "error":"customer_id must be C###", "field":"customer_id"}

    if not data.get("product_id"):
        return {"status":422, "error":"product_id is required", "field":"product_id"}
    if not re.match(r"^P\d{3}$", data["product_id"]):
        return {"status":422, "error":"product_id must be P###", "field":"product_id"}

    if "quantity" not in data:
        return {"status":422, "error":"quantity is required", "field":"quantity"}
    if data["quantity"] < 1 or data["quantity"] > 999:
        return {"status":422, "error":"quantity must be 1–999", "field":"quantity"}

    if data.get("status") not in ["Pending", "Delivered"]:
        return {"status":422, "error":"status must be Pending or Delivered", "field":"status"}

    # ✅ Proceed to create...

def createCollection(request):
    data = request.body or {}

    # 🔒 GUARDS
    if not data.get("collection_id"):
        return {"status":422, "error":"collection_id is required", "field":"collection_id"}
    if not re.match(r"^CL\d{3}$", data["collection_id"]):
        return {"status":422, "error":"collection_id must be CL###", "field":"collection_id"}

    if not data.get("customer_id"):
        return {"status":422, "error":"customer_id is required", "field":"customer_id"}
    if not re.match(r"^C\d{3}$", data["customer_id"]):
        return {"status":422, "error":"customer_id must be C###", "field":"customer_id"}

    if data.get("order_id") and not re.match(r"^O\d{3}$", data["order_id"]):
        return {"status":422, "error":"order_id must be O###", "field":"order_id"}

    if data.get("collected_by") and len(data["collected_by"]) < 2:
        return {"status":422, "error":"collected_by min 2 chars", "field":"collected_by"}

    # ✅ Proceed to create...

def updateCustomer(request):
    data = request.body or {}
    customer_id = request.params.get("customer_id", "")  # from URL

    # 🔒 GUARD 1: Validate URL param FIRST
    if not re.match(r"^C\d{3}$", customer_id):
        return {"status":422, "error":"customer_id must be C###", "field":"customer_id"}

    # 🔒 GUARD 2: Validate ONLY IF field is present
    if "full_name" in data:
        if len(data["full_name"]) < 2 or len(data["full_name"]) > 100:
            return {"status":422, "error":"full_name must be 2–100 chars", "field":"full_name"}

    if "contact_number" in data:
        if not re.match(r"^09\d{2}-\d{3}-\d{4}$", data["contact_number"]):
            return {"status":422, "error":"bad format", "field":"contact_number"}

    # ✅ All guards passed — proceed to update

# Save all your files first (Ctrl+S)

# Stage your changes
git add routes/

# Commit
git commit -m "Task 2: Guard-clause validation on all create/update routes"

# Push
git push origin main



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

import streamlit as st
import pandas as pd
import datetime

# ======================================
# 1️⃣ INITIALIZE DATABASE (Mock)
# ======================================
if "customers_db" not in st.session_state:
    st.session_state.customers_db = [
        {
            "customer_id": "C001",
            "full_name": "Maria Santos",
            "contact_number": "0917-123-4567",
            "address": "Brgy. 25, Cagayan de Oro",
            "container_owned": 2,
            "registration_date": "2026-01-10"
        },
        {
            "customer_id": "C002",
            "full_name": "Juan Dela Cruz",
            "contact_number": "0918-987-6543",
            "address": "Brgy. Lapasan, Cagayan de Oro",
            "container_owned": 3,
            "registration_date": "2026-02-15"
        }
    ]

# ======================================
# 2️⃣ PAGE HEADER
# ======================================
st.title("💧 Aquaflow Tracker — Customer Management")

# ======================================
# 3️⃣ FORM & UI ("Route")
# ======================================
with st.form("add_customer_form", clear_on_submit=True):
    st.subheader("Register New Customer")

    full_name = st.text_input("Full Name")
    contact_number = st.text_input("Contact Number")
    address = st.text_area("Delivery Address")
    container_owned = st.number_input(
        "Empty Jugs Currently Held",
        min_value=0,
        value=0,
        step=1
    )

    submitted = st.form_submit_button("✅ Save Customer")

    # ======================================
    # 4️⃣ VALIDATION ("Validation Layer")
    # ======================================
    if submitted:
        errors = []

        if not full_name or len(full_name.strip()) < 2:
            errors.append("• Full Name must be at least 2 characters")

        if not contact_number or len(contact_number.strip()) < 7:
            errors.append("• Enter a valid Contact Number")

        if not address or len(address.strip()) < 5:
            errors.append("• Address must be at least 5 characters")

        # ❌ Show errors & stop
        if errors:
            for err in errors:
                st.error(err)
            st.stop()

        # ======================================
        # 5️⃣ CONTROLLER — Save Record
        # ======================================
        new_index = len(st.session_state.customers_db) + 1
        new_customer_id = f"C{new_index:03d}"

        new_customer = {
            "customer_id": new_customer_id,
            "full_name": full_name.strip(),
            "contact_number": contact_number.strip(),
            "address": address.strip(),
            "container_owned": container_owned,
            "registration_date": str(datetime.date.today())
        }

        st.session_state.customers_db.append(new_customer)
        st.success(f"✅ Customer {new_customer_id} saved successfully!")

# ======================================
# 6️⃣ DISPLAY ALL RECORDS
# ======================================
st.divider()
st.subheader("📋 Customer Records")

if st.session_state.customers_db:
    df = pd.DataFrame(st.session_state.customers_db)
    st.dataframe(df, use_container_width=True)
else:
    st.info("No customers registered yet.")
