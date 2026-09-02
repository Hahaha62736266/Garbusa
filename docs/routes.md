# Routes Documentation — Aquaflow Tracker

## Application Routes / Pages

| Route / Page | Purpose | HTTP Method / Action |
|---|---|---|
| **Customers** (`routes/customers.py`) | List, add, edit, delete customer records | Form submit → CRUD to controller |
| **Products** (`routes/products.py`) | Manage product catalog & pricing | Form submit → CRUD to controller |
| **Orders** (`routes/orders.py`) | Create & view orders; auto-calculate total | Form submit → create order + update status |
| **Collections** (`routes/collections.py`) | Record gallon returns/releases & balances | Form submit → update container balance |

## Shared Behaviors
- All routes validate input via `/validation/` before passing to controllers
- All routes return success/error messages to UI
- Data persisted in `st.session_state` mock database
