# Aquaflow Tracker — API Route Specification

## Base URL
All routes follow consistent REST pattern: `METHOD /resource-name`

---

## Customers
| Method | Route | Description | Validation | Auth |
|---|---|---|---|---|
| GET | `/customers` | List all customers | — | — |
| POST | `/customers` | Create new customer | ✅ Full validation | — |
| GET | `/customers/{customer_id}` | Get single customer | ID format check | — |
| PUT | `/customers/{customer_id}` | Update customer info | ✅ Full validation | — |
| DELETE | `/customers/{customer_id}` | Remove customer | ID format check | ✅ Owner |

---

## Products
| Method | Route | Description | Validation | Auth |
|---|---|---|---|---|
| GET | `/products` | List all products | — | — |
| POST | `/products` | Add new product | ✅ Full validation | — |
| GET | `/products/{product_id}` | Get single product | ID format check | — |
| PUT | `/products/{product_id}` | Update product details | ✅ Full validation | — |
| DELETE | `/products/{product_id}` | Remove product | ID format check | — |

---

## Orders
| Method | Route | Description | Validation | Auth |
|---|---|---|---|---|
| GET | `/orders` | List all orders | — | — |
| POST | `/orders` | Place new order | ✅ Full validation | — |
| GET | `/orders/{order_id}` | Get single order | ID format check | — |
| PUT | `/orders/{order_id}` | Update order status/qty | ✅ Full validation | — |
| DELETE | `/orders/{order_id}` | Cancel order | ID format check | ✅ Owner |

---

## Collections
| Method | Route | Description | Validation | Auth |
|---|---|---|---|---|
| GET | `/collections` | List all records | — | — |
| POST | `/collections` | Log delivery/collection | ✅ Full validation | — |
| GET | `/collections/{collection_id}` | Get single record | ID format check | — |
| PUT | `/collections/{collection_id}` | Update record | ✅ Full validation | — |
| DELETE | `/collections/{collection_id}` | Remove record | ID format check | — |

---

## Standards
- Validation runs FIRST on every POST/PUT → returns standardized 422 before controller
- ID formats: `C###` Customers · `P###` Products · `O###` Orders · `CL###` Collections
- Response shape: Success `{status, data}` · Validation fail `{status:422, error, field}`
