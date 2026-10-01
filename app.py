from app import app  # matches filename where app = Flask(...) is

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False, port=5000)

import streamlit as st
import pandas as pd
import datetime
from supabase import create_client, Client

# ==================================================
# SUPABASE CONNECTION — PASTE YOUR KEYS HERE 🔑
# ==================================================
SUPABASE_URL = "https://YOUR-PROJECT.supabase.co"       # ← Your URL
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." # ← Your anon key

def init_supabase() -> Client:
    return create_client(SUPABASE_URL, SUPABASE_KEY)

supabase = init_supabase()

# ==================================================
# PAGE CONFIG
# ==================================================
st.set_page_config(
    page_title="Aquaflow Tracker",
    page_icon="💧",
    layout="wide"
)

# ==================================================
# PROJECT IDENTITY
# ==================================================
st.title("💧 Aquaflow Tracker")
st.subheader("Water Refilling Station Management System")

st.markdown("""
A lightweight web application designed to **digitalize daily operations** for local water refilling stations.

### ✅ What We Track
- 🧑‍🤝‍🧑 **Customer Records** – profiles, contact details, and container balances
- 📋 **Orders & Deliveries** – order queue, status tracking, and payment logs
- 🫙 **Gallon Inventory** – real-time stock and loaned-out container counts
- 💰 **Daily Sales & Collections** – revenue, returns, and container exchange records

### ❌ Not What It Is
This system is **not** a water flow sensor or hydrology monitoring tool — it manages the *business and inventory* side of water refilling operations.
""")

st.divider()

# ==================================================
# DATABASE HELPER FUNCTIONS
# ==================================================
def fetch_all(table):
    """Get all records from a Supabase table"""
    try:
        res = supabase.table(table).select("*").execute()
        return res.data or []
    except Exception as e:
        st.error(f"Error loading {table}: {e}")
        return []

def insert_record(table, data):
    """Add a new record"""
    try:
        supabase.table(table).insert(data).execute()
        return True
    except Exception as e:
        st.error(f"Error saving to {table}: {e}")
        return False

def update_order_status(order_id, new_status):
    """Update order status"""
    try:
        supabase.table("orders").update({"status": new_status}).eq("order_id", order_id).execute()
        return True
    except Exception as e:
        st.error(f"Error updating order: {e}")
        return False

def get_next_id(table, prefix):
    """Generate next ID like C001, O002"""
    records = fetch_all(table)
    count = len(records) + 1
    return f"{prefix}{count:03d}"

# ==================================================
# NAVIGATION TABS
# ==================================================
tab1, tab2, tab3, tab4 = st.tabs([
    "👥 Customers", 
    "📦 Products", 
    "📋 Orders", 
    "🫙 Collections & Inventory"
])

# ==================================================
# TAB 1: CUSTOMERS
# ==================================================
with tab1:
    st.header("Customer Management")
    
    with st.form("add_customer_form", clear_on_submit=True):
        st.subheader("Register New Customer")
        col1, col2 = st.columns(2)
        
        with col1:
            full_name = st.text_input("Full Name")
            contact_number = st.text_input("Contact Number")
        
        with col2:
            address = st.text_input("Delivery Address")
            container_owned = st.number_input("Empty Jugs Owned", min_value=0, value=0)
        
        submitted = st.form_submit_button("✅ Add Customer")
        
        if submitted:
            new_id = get_next_id("customers", "C")
            data = {
                "customer_id": new_id,
                "full_name": full_name,
                "contact_number": contact_number,
                "address": address,
                "container_owned": container_owned,
                "registration_date": str(datetime.date.today())
            }
            if insert_record("customers", data):
                st.success(f"Customer {new_id} — {full_name} saved to database!")
                st.rerun()
    
    st.subheader("Customer Records")
    customers = fetch_all("customers")
    if customers:
        st.dataframe(pd.DataFrame(customers), use_container_width=True, hide_index=True)
    else:
        st.info("No customers yet. Add your first one above!")

# ==================================================
# TAB 2: PRODUCTS
# ==================================================
with tab2:
    st.header("Product & Inventory Management")
    
    with st.form("add_product_form", clear_on_submit=True):
        st.subheader("Add New Product")
        product_name = st.text_input("Product Name")
        price_per_unit = st.number_input("Price (₱)", min_value=0.0, step=5.0)
        description = st.text_input("Description")
        stock_available = st.number_input("Stock Available", min_value=0, value=0)
        
        submitted = st.form_submit_button("✅ Add Product")
        
        if submitted:
            new_id = get_next_id("products", "P")
            data = {
                "product_id": new_id,
                "product_name": product_name,
                "price_per_unit": float(price_per_unit),
                "description": description,
                "stock_available": stock_available
            }
            if insert_record("products", data):
                st.success(f"Product {new_id} — {product_name} saved!")
                st.rerun()
    
    st.subheader("Product List")
    products = fetch_all("products")
    if products:
        st.dataframe(pd.DataFrame(products), use_container_width=True, hide_index=True)
    else:
        st.info("No products yet.")

# ==================================================
# TAB 3: ORDERS
# ==================================================
with tab3:
    st.header("Order Management")
    
    customers = fetch_all("customers")
    products = fetch_all("products")
    orders = fetch_all("orders")
    
    price_map = {p["product_id"]: p["price_per_unit"] for p in products}
    
    with st.form("add_order_form", clear_on_submit=True):
        st.subheader("Create New Order")
        cust_options = [f"{c['customer_id']} — {c['full_name']}" for c in customers] if customers else []
        prod_options = [f"{p['product_id']} — {p['product_name']} (₱{p['price_per_unit']})" for p in products] if products else []
        
        if cust_options and prod_options:
            selected_cust = st.selectbox("Select Customer", cust_options)
            selected_prod = st.selectbox("Select Product", prod_options)
            quantity = st.number_input("Quantity", min_value=1, value=1)
            
            prod_code = selected_prod.split(" — ")[0]
            unit_price = price_map[prod_code]
            total_amount = unit_price * quantity
            st.info(f"💰 Total: ₱{total_amount:.2f}")
            
            submitted = st.form_submit_button("✅ Log Order")
            
            if submitted:
                cust_code = selected_cust.split(" — ")[0]
                new_id = get_next_id("orders", "O")
                data = {
                    "order_id": new_id,
                    "customer_id": cust_code,
                    "product_id": prod_code,
                    "quantity": quantity,
                    "total_amount": float(total_amount),
                    "order_date": str(datetime.date.today()),
                    "status": "Pending"
                }
                if insert_record("orders", data):
                    st.success(f"Order {new_id} saved to database!")
                    st.rerun()
        else:
            st.warning("⚠️ Add Customers and Products first before creating orders.")
    
    st.subheader("Update Order Status")
    if orders:
        order_options = [f"{o['order_id']} — {o['status']}" for o in orders]
        selected_order = st.selectbox("Select Order", order_options)
        new_status = st.selectbox("New Status", ["Pending", "Delivered", "Cancelled"])
        
        if st.button("🔄 Update Status"):
            order_code = selected_order.split(" — ")[0]
            if update_order_status(order_code, new_status):
                st.success(f"Order {order_code} updated to {new_status}!")
                st.rerun()
    
    st.subheader("Active Orders")
    if orders:
        st.dataframe(pd.DataFrame(orders), use_container_width=True, hide_index=True)
    else:
        st.info("No orders yet.")

# ==================================================
# TAB 4: COLLECTIONS
# ==================================================
with tab4:
    st.header("Collections & Container Tracking")
    
    customers = fetch_all("customers")
    orders = fetch_all("orders")
    collections = fetch_all("collections")
    
    with st.form("add_collection_form", clear_on_submit=True):
        st.subheader("Record Collection / Exchange")
        
        cust_options = [c["customer_id"] for c in customers] if customers else []
        order_options = ["—"] + [o["order_id"] for o in orders] if orders else ["—"]
        
        if cust_options:
            col1, col2 = st.columns(2)
            
            with col1:
                selected_cust = st.selectbox("Customer ID", cust_options)
                selected_order = st.selectbox("Linked Order (Optional)", order_options)
                empty_returned = st.number_input("Empty Jugs Returned", min_value=0, value=0)
            
            with col2:
                filled_released = st.number_input("Filled Jugs Given", min_value=0, value=0)
                collected_by = st.text_input("Collected By")
            
            balance = filled_released - empty_returned
            st.info(f"📊 Container Balance Change: **{balance:+d}**")
            
            submitted = st.form_submit_button("✅ Save Collection")
            
            if submitted:
                new_id = get_next_id("collections", "CL")
                order_ref = None if selected_order == "—" else selected_order
                data = {
                    "collection_id": new_id,
                    "customer_id": selected_cust,
                    "order_id": order_ref,
                    "empty_jugs_returned": empty_returned,
                    "filled_jugs_released": filled_released,
                    "container_balance": balance,
                    "collection_date": str(datetime.date.today()),
                    "collected_by": collected_by
                }
                if insert_record("collections", data):
                    st.success(f"Collection {new_id} saved permanently!")
                    st.rerun()
        else:
            st.warning("⚠️ Add customers and orders above first.")
    
    st.subheader("Collection Logs")
    if collections:
        st.dataframe(pd.DataFrame(collections), use_container_width=True, hide_index=True)
    else:
        st.info("No collections recorded yet.")

# ==================================================
# FOOTER
# ==================================================
st.divider()
st.caption("💧 Aquaflow Tracker — Water Refilling Station Management System | Permanent Storage: Supabase")

# Import the app instance — adjust the module name to match your project
from Garbusa import app  # or from app import app

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False, port=5000)
