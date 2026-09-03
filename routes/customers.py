def createCustomer(request):
    data = request.body or {}

    # ========== 🔒 GUARD CLAUSES — ADD THIS BLOCK HERE ==========

    # Guard 1: Check customer_id
    if not data.get("customer_id"):
        return {"status":422, "error":"customer_id is required", "field":"customer_id"}
    if not re.match(r"^C\d{3}$", data["customer_id"]):
        return {"status":422, "error":"customer_id must be C followed by 3 digits", "field":"customer_id"}

    # Guard 2: Check full_name
    if not data.get("full_name"):
        return {"status":422, "error":"full_name is required", "field":"full_name"}
    if not isinstance(data["full_name"], str) or len(data["full_name"]) < 2 or len(data["full_name"]) > 100:
        return {"status":422, "error":"full_name must be 2–100 characters", "field":"full_name"}

    # Guard 3: Check contact_number
    if not data.get("contact_number"):
        return {"status":422, "error":"contact_number is required", "field":"contact_number"}
    if not re.match(r"^09\d{2}-\d{3}-\d{4}$", data["contact_number"]):
        return {"status":422, "error":"contact_number must be 09XX-XXX-XXXX", "field":"contact_number"}

    # Guard 4: Check address
    if not data.get("address") or len(data["address"]) < 5:
        return {"status":422, "error":"address is required (min 5 chars)", "field":"address"}

    # Guard 5: Check container_owned
    if "container_owned" not in data:
        return {"status":422, "error":"container_owned is required", "field":"container_owned"}
    if not isinstance(data["container_owned"], int) or data["container_owned"] < 0:
        return {"status":422, "error":"container_owned must be ≥ 0", "field":"container_owned"}

    # ✅ ALL GUARDS PASSED — ONLY NOW RUN YOUR BUSINESS LOGIC
    # ... your existing code to create the customer goes here ...
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
