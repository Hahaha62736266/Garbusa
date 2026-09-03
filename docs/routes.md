# Routes Documentation — Aquaflow Tracker

description: |
  Correct text starts on a new line and is 
  indented by two spaces under the key.
next_line: value

## Application Routes / Pages (Streamlit UI)
| Route / Page | Purpose | HTTP Method / Action |
|---|---|---|
| **Customers** (`routes/customers.py`) | List, add, edit, delete customer records | Form submit → CRUD to controller |
| **Products** (`routes/products.py`) | Manage product catalog & pricing | Form submit → CRUD to controller |
| **Orders** (`routes/orders.py`) | Create & view orders; auto-calculate total | Form submit → create order + update status |
| **Collections** (`routes/collections.py`) | Record gallon returns/releases & balances | Form submit → update container balance |

### Shared Behaviors
- All routes validate input via `/validation/` before passing to controllers
- All routes return success/error messages to UI
- Data persisted in `st.session_state` mock database

---

## RESTful API Specification
> Standard Response shape: `{ "status": int, "data": {...}, "error": null }`

### Customers
| Method | Path | Handler | Status | Example Response |
|---|---|---|---|---|
| GET | /customers | listCustomers | 200 | {"status":200,"data":{"message":"listCustomers stub"},"error":null} |
| GET | /customers/:customer_id | showCustomer | 200 | {"status":200,"data":{"message":"showCustomer stub","customer_id":"C001"},"error":null} |
| POST | /customers | createCustomer | 201 | {"status":201,"data":{"message":"createCustomer stub"},"error":null} |
| PUT | /customers/:customer_id | updateCustomer | 200 | {"status":200,"data":{"message":"updateCustomer stub","customer_id":"C001"},"error":null} |
| DELETE | /customers/:customer_id | deleteCustomer | 200 | {"status":200,"data":{"message":"deleteCustomer stub","customer_id":"C001"},"error":null} |

### Products
| Method | Path | Handler | Status | Example Response |
|---|---|---|---|---|
| GET | /products | listProducts | 200 | {"status":200,"data":{"message":"listProducts stub"},"error":null} |
| GET | /products/:product_id | showProduct | 200 | {"status":200,"data":{"message":"showProduct stub","product_id":"P002"},"error":null} |
| POST | /products | createProduct | 201 | {"status":201,"data":{"message":"createProduct stub"},"error":null} |
| PUT | /products/:product_id | updateProduct | 200 | {"status":200,"data":{"message":"updateProduct stub","product_id":"P002"},"error":null} |
| DELETE | /products/:product_id | deleteProduct | 200 | {"status":200,"data":{"message":"deleteProduct stub","product_id":"P002"},"error":null} |

### Orders
| Method | Path | Handler | Status | Example Response |
|---|---|---|---|---|
| GET | /orders | listOrders | 200 | {"status":200,"data":{"message":"listOrders stub"},"error":null} |
| GET | /orders/:order_id | showOrder | 200 | {"status":200,"data":{"message":"showOrder stub","order_id":"O005"},"error":null} |
| POST | /orders | createOrder | 201 | {"status":201,"data":{"message":"createOrder stub"},"error":null} |
| PUT | /orders/:order_id | updateOrder | 200 | {"status":200,"data":{"message":"updateOrder stub","order_id":"O005"},"error":null} |
| DELETE | /orders/:order_id | deleteOrder | 200 | {"status":200,"data":{"message":"deleteOrder stub","order_id":"O005"},"error":null} |

### Collections
| Method | Path | Handler | Status | Example Response |
|---|---|---|---|---|
| GET | /collections | listCollections | 200 | {"status":200,"data":{"message":"listCollections stub"},"error":null} |
| GET | /collections/:collection_id | showCollection | 200 | {"status":200,"data":{"message":"showCollection stub","collection_id":"CL003"},"error":null} |
| POST | /collections | createCollection | 201 | {"status":201,"data":{"message":"createCollection stub"},"error":null} |
| PUT | /collections/:collection_id | updateCollection | 200 | {"status":200,"data":{"message":"updateCollection stub","collection_id":"CL003"},"error":null} |
| DELETE | /collections/:collection_id | deleteCollection | 200 | {"status":200,"data":{"message":"deleteCollection stub","collection_id":"CL003"},"error":null} |


# Aquaflow Tracker — Route Specification

## Customers
GET    /customers          → List all
POST   /customers          → Create (validated)
GET    /customers/:id      → Get one
PUT    /customers/:id      → Update (validated)
DELETE /customers/:id      → Delete (authorized)

## Products
GET    /products
POST   /products           → Create (validated)
GET    /products/:id
PUT    /products/:id       → Update (validated)
DELETE /products/:id

## Orders
GET    /orders
POST   /orders             → Create (validated)
GET    /orders/:id
PUT    /orders/:id         → Update (validated)
DELETE /orders/:id

## Collections
GET    /collections
POST   /collections        → Create (validated)
GET    /collections/:id
PUT    /collections/:id     → Update (validated)
DELETE /collections/:id

✅ All routes follow identical pattern; validation runs on POST/PUT before controller.
