import streamlit as st
import pandas as pd
import datetime

# ==================================================
# PAGE CONFIG
# ==================================================
st.set_page_config(
    page_title="Aquaflow Tracker",
    page_icon="💧",
    layout="wide"
)

# ==================================================
# PROJECT IDENTITY — AQUAFLOW TRACKER
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
# INITIALIZE DATABASES (Session State)
# ==================================================
if "customers_db" not in st.session_state:
    st.session_state.customers_db = [
        {"customer_id": "C001", "full_name": "Maria Santos", "contact_number": "0917-123-4567", 
         "address": "Brgy. 25, CdeO", "container_owned": 2, "registration_date": "2026-01-10"},
        {"customer_id": "C002", "full_name": "Juan Dela Cruz", "contact_number": "0918-987-6543", 
         "address": "Brgy. Lapasan, CdeO", "container_owned": 3, "registration_date": "2026-02-15"}
    ]

if "products_db" not in st.session_state:
    st.session_state.products_db = [
        {"product_id": "P001", "product_name": "5-Gal Purified", "price_per_unit": 35.00, 
         "description": "Refill only", "stock_available": 120},
        {"product_id": "P002", "product_name": "5-Gal Distilled", "price_per_unit": 45.00, 
         "description": "Best for drinking", "stock_available": 85},
        {"product_id": "P003", "product_name": "New 5-Gal Jug", "price_per_unit": 180.00, 
         "description": "Empty plastic jug", "stock_available": 40}
    ]

if "orders_db" not in st.session_state:
    st.session_state.orders_db = [
        {"order_id": "O001", "customer_id": "C001", "product_id": "P002", "quantity": 2, 
         "total_amount": 90.00, "order_date": "2026-07-03", "status": "Delivered"},
        {"order_id": "O002", "customer_id": "C002", "product_id": "P001", "quantity": 3, 
         "total_amount": 105.00, "order_date": "2026-07-03", "status": "Pending"}
    ]

if "collections_db" not in st.session_state:
    st.session_state.collections_db = [
        {"collection_id": "CL001", "customer_id": "C001", "order_id": "O001", 
         "empty_jugs_returned": 2, "filled_jugs_released": 2, "container_balance": 2,
         "collection_date": "2026-07-03", "collected_by": "Staff A"}
    ]

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
    
    # Add New Customer Form
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
            new_id = f"C{len(st.session_state.customers_db)+1:03d}"
            new_customer = {
                "customer_id": new_id,
                "full_name": full_name,
                "contact_number": contact_number,
                "address": address,
                "container_owned": container_owned,
                "registration_date": str(datetime.date.today())
            }
            st.session_state.customers_db.append(new_customer)
            st.success(f"Customer {new_id} — {full_name} added successfully!")
    
    # Display All Customers
    st.subheader("Customer Records")
    df_customers = pd.DataFrame(st.session_state.customers_db)
    st.dataframe(df_customers, use_container_width=True, hide_index=True)

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
            new_id = f"P{len(st.session_state.products_db)+1:03d}"
            new_product = {
                "product_id": new_id,
                "product_name": product_name,
                "price_per_unit": price_per_unit,
                "description": description,
                "stock_available": stock_available
            }
            st.session_state.products_db.append(new_product)
            st.success(f"Product {new_id} — {product_name} added!")
    
    st.subheader("Product List")
    df_products = pd.DataFrame(st.session_state.products_db)
    st.dataframe(df_products, use_container_width=True, hide_index=True)

# ==================================================
# TAB 3: ORDERS
# ==================================================
with tab3:
    st.header("Order Management")
    
    # Dropdown options
    customer_list = [f"{c['customer_id']} — {c['full_name']}" for c in st.session_state.customers_db]
    product_list = [f"{p['product_id']} — {p['product_name']} (₱{p['price_per_unit']})" 
                    for p in st.session_state.products_db]
    price_map = {p['product_id']: p['price_per_unit'] for p in st.session_state.products_db}
    
    with st.form("add_order_form", clear_on_submit=True):
        st.subheader("Create New Order")
        selected_cust = st.selectbox("Select Customer", customer_list)
        selected_prod = st.selectbox("Select Product", product_list)
        quantity = st.number_input("Quantity", min_value=1, value=1)
        
        # Calculate total
        prod_code = selected_prod.split(" — ")[0]
        unit_price = price_map[prod_code]
        total_amount = unit_price * quantity
        st.info(f"💰 Total: ₱{total_amount:.2f}")
        
        submitted = st.form_submit_button("✅ Log Order")
        
        if submitted:
            cust_code = selected_cust.split(" — ")[0]
            new_id = f"O{len(st.session_state.orders_db)+1:03d}"
            new_order = {
                "order_id": new_id,
                "customer_id": cust_code,
                "product_id": prod_code,
                "quantity": quantity,
                "total_amount": total_amount,
                "order_date": str(datetime.date.today()),
                "status": "Pending"
            }
            st.session_state.orders_db.append(new_order)
            st.success(f"Order {new_id} created successfully!")
    
    # Update Order Status
    st.subheader("Update Order Status")
    if st.session_state.orders_db:
        order_list = [f"{o['order_id']} — {o['status']}" for o in st.session_state.orders_db]
        selected_order = st.selectbox("Select Order to Update", order_list)
        new_status = st.selectbox("New Status", ["Pending", "Delivered", "Cancelled"])
        
        if st.button("🔄 Update Status"):
            order_code = selected_order.split(" — ")[0]
            for o in st.session_state.orders_db:
                if o["order_id"] == order_code:
                    o["status"] = new_status
                    st.success(f"Order {order_code} updated to {new_status}!")
                    break
    
    st.subheader("Active Orders")
    df_orders = pd.DataFrame(st.session_state.orders_db)
    st.dataframe(df_orders, use_container_width=True, hide_index=True)

# ==================================================
# TAB 4: COLLECTIONS
# ==================================================
with tab4:
    st.header("Collections & Container Tracking")
    
    if st.session_state.orders_db and st.session_state.customers_db:
        order_list = [f"{o['order_id']}" for o in st.session_state.orders_db]
        customer_list = [f"{c['customer_id']}" for c in st.session_state.customers_db]
        
        with st.form("add_collection_form", clear_on_submit=True):
            st.subheader("Record Collection / Exchange")
            col1, col2 = st.columns(2)
            
            with col1:
                selected_cust = st.selectbox("Customer ID", customer_list)
                selected_order = st.selectbox("Linked Order (Optional)", ["—"] + order_list)
                empty_returned = st.number_input("Empty Jugs Returned", min_value=0, value=0)
            
            with col2:
                filled_released = st.number_input("Filled Jugs Given", min_value=0, value=0)
                collected_by = st.text_input("Collected By")
            
            balance = filled_released - empty_returned
            st.info(f"📊 Container Balance Change: **{balance:+d}**")
            
            submitted = st.form_submit_button("✅ Save Collection")
            
            if submitted:
                new_id = f"CL{len(st.session_state.collections_db)+1:03d}"
                order_ref = None if selected_order == "—" else selected_order
                new_collection = {
                    "collection_id": new_id,
                    "customer_id": selected_cust,
                    "order_id": order_ref,
                    "empty_jugs_returned": empty_returned,
                    "filled_jugs_released": filled_released,
                    "container_balance": balance,
                    "collection_date": str(datetime.date.today()),
                    "collected_by": collected_by
                }
                st.session_state.collections_db.append(new_collection)
                st.success(f"Collection {new_id} saved!")
    
    st.subheader("Collection Logs")
    if st.session_state.collections_db:
        df_collections = pd.DataFrame(st.session_state.collections_db)
        st.dataframe(df_collections, use_container_width=True, hide_index=True)
    else:
        st.info("No collections recorded yet.")

# ==================================================
# FOOTER
# ==================================================
st.divider()
st.caption("💧 Aquaflow Tracker — Water Refilling Station Management System | Capstone Project")