# Garbusa
# Aquaflow Tracker - Water Refilling Station Management System
A lightweight, CRUD-shaped web application designed to digitalize daily sales, deliveries, and container balances for local water refilling stations.

---

## 👥 Team Roster & Roles (Sprint 1)

*   **Repo Lead:** Pepito — *Branch protection, merge hygiene, and repository health.*
*   **Board Lead:** Taylaran — *Task board upkeep, ticket assignment, and progress tracking.*
*   **Scribe:** Apostol — *Decision log documentation and sprint retrospective notes.*
*   **Builder 1:** Baydal — *Core application feature development.*
*   **Builder 2:** Obiasad — *Core application feature development.*

---

## 📝 Problem Statement

Local water refilling stations heavily rely on manual paper logbooks or loose whiteboards to track custom deliveries, walk-in orders, and customer-borrowed slim/round gallons. This manual approach leads to missing delivery windows, unaccounted-for container inventory, and inaccurate calculations of outstanding customer balances. 

**Aquaflow Tracker** provides a lightweight management portal that digitalizes daily order queues, logs customer purchase profiles, and keeps a real-time count of containers currently out on loan, ensuring smoother logistics and zero lost inventory over a 12-week development scope.

---

## 🗄️ Core CRUD Entities & Record Types

The application manages data workflows across three tightly related record types:

1.  **Customer Records (CRUD)**
    *   *Fields:* Customer ID, Name, Delivery Address, Contact Number, Outstanding Gallon Balance.
2.  **Order Logs (CRUD)**
    *   *Fields:* Order ID, Customer ID (Foreign Key), Order Date, Delivery Status (`Pending` / `Delivered`), Total Price, Payment Status.
3.  **Gallon Inventory Tracker (CRUD)**
    *   *Fields:* Container ID, Type (`Slim 5-Gallon` / `Round 5-Gallon`), Physical Stock Available, Total Containers Loaned Out.

---

## 🛠️ Tech Stack & Setup (To Be Updated in Week 3)

> 💡 *Note: This project scaffolding is configured for a Python/Streamlit ecosystem (or your team's chosen alternative).*

### Prerequisites
*   Python 3.10+
*   Git

### Local Installation
1. Clone the repository:
   ```bash
   git clone <your-repository-url>
   cd <repository-folder-name>

   # Customer Records

# Customers
- customer_id (PK, unique)
- full_name
- contact_number
- address
- container_owned (empty 5gal jugs)
- registration_date

## Sample Records
| customer_id | full_name       | contact      | address                  | container_owned | registration_date |
|---|---|---|---|---|---|
| C001        | Maria Santos    | 0917-123-4567 | Brgy. 25, CdeO           | 2               | 2026-01-10 |
| C002        | Juan Dela Cruz  | 0918-987-6543 | Brgy. Lapasan, CdeO      | 3               | 2026-02-15 |

# Products
- product_id (PK, unique)
- product_name
- price_per_unit (PHP)
- description
- stock_available

## Sample Records
| product_id | product_name       | price | description          | stock_available |
|---|---|---|---|---|
| P001       | 5-Gal Purified     | 35.00 | Refill only          | 120 |
| P002       | 5-Gal Distilled    | 45.00 | Best for drinking    | 85 |
| P003       | New 5-Gal Jug      | 180.00 | Empty plastic jug   | 40 |

# Orders
- order_id (PK, unique)
- customer_id (FK → Customers)
- product_id (FK → Products)
- quantity
- total_amount
- order_date
- status

## Sample Records
| order_id | customer_id | product_id | quantity | total | order_date | status |
|---|---|---|---|---|---|---|
| O001     | C001        | P002       | 2        | 90.00 | 2026-07-03 | Delivered |
| O002     | C002        | P001       | 3        | 105.00 | 2026-07-03 | Pending |


# Collections
- collection_id (PK, unique)
- customer_id (FK → Customers)
- order_id (FK → Orders, optional)
- empty_jugs_returned
- filled_jugs_released
- container_balance
- collection_date
- collected_by

## Sample Records
| collection_id | customer_id | order_id | empty_jugs_returned | filled_jugs_released | container_balance | collection_date | collected_by |
|---------------|-------------|----------|---------------------|----------------------|-------------------|-----------------|--------------|
| CL001         | C001        | O001     | 2                   | 2                    | 2                 | 2026-07-03      | Staff A      |
| CL002         | C002        | O002     | 3                   | 0                    | 3                 | 2026-07-03      | Staff B      
import streamlit as st
import pandas as pd
import datetime

# Mock database
if "decision_logs_db" not in st.session_state:
    st.session_state.decision_logs_db = []

st.title("💧 Aquaflow Tracker - Decision Log Documentation")

with st.form("add_decision_form", clear_on_submit=True):
    st.subheader("New Decision Log")

    decision_title = st.text_input("Decision Title")
    description = st.text_area("Decision Description")
    decided_by = st.text_input("Decided By")

    submitted = st.form_submit_button("Save Decision")

    if submitted:
        new_decision_id = f"D{len(st.session_state.decision_logs_db)+1:03d}"

        decision_payload = {
            "decision_id": new_decision_id,
            "title": decision_title,
            "description": description,
            "decided_by": decided_by,
            "decision_date": str(datetime.date.today())
        }

        st.session_state.decision_logs_db.append(decision_payload)

        st.success(f"Decision {new_decision_id} saved successfully!")

st.write("### Decision Log Records")

if st.session_state.decision_logs_db:
    st.dataframe(pd.DataFrame(st.session_state.decision_logs_db))
else:
    st.info("No decision logs recorded yet.")

import streamlit as st
import pandas as pd
import datetime

# Mock database
if "retrospective_db" not in st.session_state:
    st.session_state.retrospective_db = []

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

        retrospective_payload = {
            "note_id": new_note_id,
            "sprint": sprint_name,
            "went_well": went_well,
            "needs_improvement": needs_improvement,
            "action_items": action_items,
            "date": str(datetime.date.today())
        }

        st.session_state.retrospective_db.append(retrospective_payload)

        st.success(f"Sprint retrospective {new_note_id} saved successfully!")

st.write("### Sprint Retrospective Records")

if st.session_state.retrospective_db:
    st.dataframe(pd.DataFrame(st.session_state.retrospective_db))
else:
    st.info("No sprint retrospective notes recorded yet.")
    
# Mock database connections
if "orders_db" not in st.session_state:
    st.session_state.orders_db = []

st.title("💧 Aquaflow Tracker - Create Order")

with st.form("add_order_form", clear_on_submit=True):
    st.subheader("New Order Information")
    
    # Form Input Controls
    customer_id = st.selectbox("Select Customer ID", ["C001 (Maria Santos)", "C002 (Juan Dela Cruz)"])
    product_id = st.selectbox("Select Product", ["P001 - 5-Gal Purified (₱35)", "P002 - 5-Gal Distilled (₱45)", "P003 - New 5-Gal Jug (₱180)"])
    quantity = st.number_input("Quantity", min_value=1, value=1, step=1)
    
    # Simple pricing calculator matrix
    price_map = {"P001": 35.00, "P002": 45.00, "P003": 180.00}
    selected_prod_code = product_id.split(" ")[0]
    total_amount = price_map[selected_prod_code] * quantity
    
    st.info(f"Estimated Total: ₱{total_amount:.2f}")
    
    # Form submission action
    submitted = st.form_submit_button("Log Order")
    if submitted:
        new_order_id = f"O{len(st.session_state.orders_db) + 1:03d}"
        order_payload = {
            "order_id": new_order_id,
            "customer_id": customer_id.split(" ")[0],
            "product_id": selected_prod_code,
            "quantity": quantity,
            "total": total_amount,
            "order_date": str(datetime.date.today()),
            "status": "Pending"
        }
        st.session_state.orders_db.append(order_payload)
        st.success(f"Order {new_order_id} added successfully to the active queue!")

# Display current workflow orders queue
st.write("### Active Orders Log View")
if st.session_state.orders_db:
    st.dataframe(pd.DataFrame(st.session_state.orders_db))
else:
    st.info("No orders captured today yet.")
