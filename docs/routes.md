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

# RESTful Routes — Aquaflow Tracker
> Generated for Deliverable 2 — Task 1
> Follows REST conventions: GET=read, POST=create, PUT=update, DELETE=remove

---

## Customers
| Method | Path | Handler | Purpose |
|---|---|---|---|
| GET | /customers | listCustomers | View all customers |
| GET | /customers/:customer_id | showCustomer | View one customer |
| POST | /customers | createCustomer | Add new customer |
| PUT | /customers/:customer_id | updateCustomer | Update customer info |
| DELETE | /customers/:customer_id | deleteCustomer | Delete customer |

---

## Products
| Method | Path | Handler | Purpose |
|---|---|---|---|
| GET | /products | listProducts | View all products |
| GET | /products/:product_id | showProduct | View one product |
| POST | /products | createProduct | Add new product |
| PUT | /products/:product_id | updateProduct | Update product details |
| DELETE | /products/:product_id | deleteProduct | Remove product |

---

## Orders
| Method | Path | Handler | Purpose |
|---|---|---|---|
| GET | /orders | listOrders | View all orders |
| GET | /orders/:order_id | showOrder | View one order |
| POST | /orders | createOrder | Place new order |
| PUT | /orders/:order_id | updateOrder | Update order/status |
| DELETE | /orders/:order_id | deleteOrder | Cancel order |

---

## Collections
| Method | Path | Handler | Purpose |
|---|---|---|---|
| GET | /collections | listCollections | View all transactions |
| GET | /collections/:collection_id | showCollection | View one transaction |
| POST | /collections | createCollection | Log jug return/release |
| PUT | /collections/:collection_id | updateCollection | Edit transaction |
| DELETE | /collections/:collection_id | deleteCollection | Remove record |
