import streamlit as st
import pandas as pd
import datetime
import time

# ==============================================
# PAGE SETUP
# ==============================================
st.set_page_config(page_title="Aquaflow Tracker", layout="wide")

# ==============================================
# INITIALIZE DATABASES
# ==============================================
if "decision_logs_db" not in st.session_state:
    st.session_state.decision_logs_db = []

if "retrospective_db" not in st.session_state:
    st.session_state.retrospective_db = []

if "orders_db" not in st.session_state:
    st.session_state.orders_db = []

if "is_saving_order" not in st.session_state:
    st.session_state.is_saving_order = False

if "is_saving_decision" not in st.session_state:
    st.session_state.is_saving_decision = False

# ==============================================
# DECISION LOGS — With Loading
# ==============================================
st.title("💧 Aquaflow Tracker - Decision Log Documentation")

with st.form("add_decision_form", clear_on_submit=True):
    st.subheader("New Decision Log")
    decision_title = st.text_input("Decision Title", disabled=st.session_state.is_saving_decision)
    description = st.text_area("Decision Description", disabled=st.session_state.is_saving_decision)
    decided_by = st.text_input("Decided By", disabled=st.session_state.is_saving_decision)
    
    submit_text = "Saving…" if st.session_state.is_saving_decision else "Save Decision"
    submitted = st.form_submit_button(submit_text, disabled=st.session_state.is_saving_decision)

    if submitted:
        st.session_state.is_saving_decision = True
        st.rerun()

if st.session_state.is_saving_decision:
    with st.spinner("Saving decision log..."):
        time.sleep(1)
        new_decision_id = f"D{len(st.session_state.decision_logs_db)+1:03d}"
        st.session_state.decision_logs_db.append({
            "decision_id": new_decision_id,
            "title": decision_title,
            "description": description,
            "decided_by": decided_by,
            "decision_date": str(datetime.date.today())
        })
        st.session_state.is_saving_decision = False
        st.success(f"✅ Decision {new_decision_id} saved!")
        st.rerun()

st.write("### Decision Log Records")
if st.session_state.decision_logs_db:
    st.dataframe(pd.DataFrame(st.session_state.decision_logs_db))
else:
    st.info("No decision logs recorded yet.")

# ==============================================
# SPRINT RETROSPECTIVE — Original (kept)
# ==============================================
st.title("💧 Aquaflow Tracker - Sprint Retrospective Notes")

with st.form("add_retrospective_form", clear_on_submit=True):
    st.subheader("Sprint Retrospective")
    sprint_name = st.text_input("Sprint Name")
    went_well = st.text_area("What Went Well?")
    needs_improvement = st.text_area("Needs Improvement")
    action_items = st.text_area("Action Items")
    submitted = st.form_submit_button("Save Notes")
    
    if submitted:
        new_note_id = f"SR{len(st.session_state.retrospective_db)+1:03d}"
        st.session_state.retrospective_db.append({
            "note_id": new_note_id,
            "sprint": sprint_name,
            "went_well": went_well,
            "needs_improvement": needs_improvement,
            "action_items": action_items,
            "date": str(datetime.date.today())
        })
        st.success(f"Sprint retrospective {new_note_id} saved successfully!")

st.write("### Sprint Retrospective Records")
if st.session_state.retrospective_db:
    st.dataframe(pd.DataFrame(st.session_state.retrospective_db))
else:
    st.info("No sprint retrospective notes recorded yet.")

# ==============================================
# CREATE ORDER — With Loading Indicators
# ==============================================
st.title("💧 Aquaflow Tracker - Create Order")

with st.form("add_order_form", clear_on_submit=True):
    st.subheader("New Order Information")

    customer_id = st.selectbox(
        "Select Customer ID",
        ["C001 (Maria Santos)", "C002 (Juan Dela Cruz)"],
        disabled=st.session_state.is_saving_order
    )
    product_id = st.selectbox(
        "Select Product",
        ["P001 - 5-Gal Purified (₱35)", "P002 - 5-Gal Distilled (₱45)", "P003 - New 5-Gal Jug (₱180)"],
        disabled=st.session_state.is_saving_order
    )
    quantity = st.number_input(
        "Quantity",
        min_value=1, value=1, step=1,
        disabled=st.session_state.is_saving_order
    )

    price_map = {"P001": 35.00, "P002": 45.00, "P003": 180.00}
    selected_prod_code = product_id.split(" ")[0]
    total_amount = price_map[selected_prod_code] * quantity
    st.info(f"Estimated Total: ₱{total_amount:.2f}")

    submit_label = "Saving…" if st.session_state.is_saving_order else "Log Order"
    submitted = st.form_submit_button(submit_label, disabled=st.session_state.is_saving_order)

    if submitted:
        st.session_state.is_saving_order = True
        st.rerun()

if st.session_state.is_saving_order:
    with st.spinner("Saving order..."):
        time.sleep(1.2)
        new_order_id = f"O{len(st.session_state.orders_db) + 1:03d}"
        st.session_state.orders_db.append({
            "order_id": new_order_id,
            "customer_id": customer_id.split(" ")[0],
            "product_id": selected_prod_code,
            "quantity": quantity,
            "total": total_amount,
            "order_date": str(datetime.date.today()),
            "status": "Pending"
        })
        st.session_state.is_saving_order = False
        st.success(f"✅ Order {new_order_id} added successfully!")
        st.rerun()

# ==============================================
# ORDERS LIST — With Loading Skeleton
# ==============================================
st.write("### Active Orders Log View")

if len(st.session_state.orders_db) == 0:
    with st.status("Loading orders...", expanded=True):
        st.info("⏳ Fetching order records...")
        for _ in range(3):
            st.markdown("▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓")
else:
    st.dataframe(pd.DataFrame(st.session_state.orders_db))
