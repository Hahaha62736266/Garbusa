# Aquaflow Tracker — API Route Specification

## Base URL
All routes follow the pattern: `METHOD /resource-name`

---

## 🧑 Customers
| Method | Route | Description | Validation | Auth |
|---|---|---|---|---|
| GET | `/customers` | List all customers | — | — |
| POST | `/customers` | Create new customer | ✅ Full validation | — |
| GET | `/customers/{customer_id}` | Get single customer by ID | ID format check | — |
| PUT | `/customers/{customer_id}` | Update customer info | ✅ Full validation | — |
| DELETE | `/customers/{customer_id}` | Remove customer | ID format check | ✅ Owner |

---

## 🧴 Products
| Method | Route | Description | Validation | Auth |
|---|---|---|---|---|
| GET | `/products` | List all products | — | — |
| POST | `/products` | Add new product | ✅ Full validation | — |
| GET | `/products/{product_id}` | Get single product by ID | ID format check | — |
| PUT | `/products/{product_id}` | Update product details | ✅ Full validation | — |
| DELETE | `/products/{product_id}` | Remove product | ID format check | — |

---

## 📋 Orders
| Method | Route | Description | Validation | Auth |
|---|---|---|---|---|
| GET | `/orders` | List all orders | — | — |
| POST | `/orders` | Place new order | ✅ Full validation | — |
| GET | `/orders/{order_id}` | Get single order by ID | ID format check | — |
| PUT | `/orders/{order_id}` | Update order status/qty | ✅ Full validation | — |
| DELETE | `/orders/{order_id}` | Cancel order | ID format check | ✅ Owner |

---

## 📦 Collections
| Method | Route | Description | Validation | Auth |
|---|---|---|---|---|
| GET | `/collections` | List all collection records | — | — |
| POST | `/collections` | Log a delivery/collection | ✅ Full validation | — |
| GET | `/collections/{collection_id}` | Get single record by ID | ID format check | — |
| PUT | `/collections/{collection_id}` | Update collection record | ✅ Full validation | — |
| DELETE | `/collections/{collection_id}` | Remove record | ID format check | — |

---

## ✅ Standards & Conventions
- **Consistent pattern**: All 4 entities use identical route structure
- **Validation runs FIRST**: Every `POST` / `PUT` body validated → returns `422` before controller
- **ID format rules**:
  - `C###` → Customers
  - `P###` → Products
  - `O###` → Orders
  - `CL###` → Collections
- **Response shape**:
  - Success → `{"status":200/201, "data": {...}}`
  - Validation fail → `{"status":422, "error": "...", "field": "..."}`
  - Not found → `{"status":404, "error": "..."}`
  - Forbidden → `{"status":403, "error": "..."}`
