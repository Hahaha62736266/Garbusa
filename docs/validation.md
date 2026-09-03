# Aquaflow Tracker — Validation Rules

> Every POST/PUT route validates input BEFORE reaching the controller. Returns **422** with `error` and `field` on failure.

---

## Customers
### Create
- `customer_id`: Required; format `C###`
- `full_name`: Required; string 2–100 characters
- `contact_number`: Required; format `09XX-XXX-XXXX`
- `address`: Required; minimum 5 characters
- `container_owned`: Required; integer ≥ 0

### Update
- `customer_id` (URL): Must match `C###`
- Fields optional — validated if provided

---

## Products
### Create
- `product_id`: Required; format `P###`
- `product_name`: Required; string 2–100 characters
- `price_per_unit`: Required; number ≥ `0.00`
- `stock_available`: Required; integer ≥ 0

### Update
- `product_id` (URL): Must match `P###`
- Fields optional — validated if present

---

## Orders
### Create
- `order_id`: Required; format `O###`
- `customer_id`: Required; format `C###`
- `product_id`: Required; format `P###`
- `quantity`: Required; integer 1–999
- `status`: Required; `Pending` or `Delivered`

### Update
- `order_id` (URL): Must match `O###`
- Fields optional — validated if present

---

## Collections
### Create
- `collection_id`: Required; format `CL###`
- `customer_id`: Required; format `C###`
- `order_id`: Optional; format `O###` if provided
- `empty_jugs_returned`: Required; integer ≥ 0
- `filled_jugs_released`: Required; integer ≥ 0
- `container_balance`: Required; integer ≥ 0
- `collected_by`: Required; minimum 2 characters

### Update
- `collection_id` (URL): Must match `CL###`
- Fields optional — validated if present

---


# Aquaflow Tracker — Validation Matrix

> Rule Vocabulary: **Presence** · **Type** · **Length/Range** · **Format** · **Allowed Values** · **Referential**

---

## 🧑 CUSTOMERS

### POST /customers — Create
| Field | Presence | Type | Length / Range | Format | Allowed Values | Referential |
|---|---|---|---|---|---|---|
| customer_id | Required | String | — | `C###` (C + 3 digits) | — | Must be unique |
| full_name | Required | String | 2–100 characters | Plain text | — | — |
| contact_number | Required | String | 13 characters | `09XX-XXX-XXXX` | — | — |
| address | Required | String | Min 5 characters | Plain text | — | — |
| container_owned | Required | Integer | ≥ 0 | Whole number | — | — |

### PUT /customers/{customer_id} — Update
| Field | Presence | Type | Length / Range | Format | Allowed Values | Referential |
|---|---|---|---|---|---|---|
| customer_id (URL) | Required | String | — | `C###` | — | Must exist |
| full_name | Optional | String | 2–100 characters | Plain text | — | — |
| contact_number | Optional | String | 13 characters | `09XX-XXX-XXXX` | — | — |
| address | Optional | String | Min 5 characters | Plain text | — | — |
| container_owned | Optional | Integer | ≥ 0 | Whole number | — | — |

---

## 🧴 PRODUCTS

### POST /products — Create
| Field | Presence | Type | Length / Range | Format | Allowed Values | Referential |
|---|---|---|---|---|---|---|
| product_id | Required | String | — | `P###` (P + 3 digits) | — | Must be unique |
| product_name | Required | String | 2–100 characters | Plain text | — | — |
| price_per_unit | Required | Decimal | ≥ 0.00 | Numeric, 2 decimal places | — | — |
| stock_available | Required | Integer | ≥ 0 | Whole number | — | — |

### PUT /products/{product_id} — Update
| Field | Presence | Type | Length / Range | Format | Allowed Values | Referential |
|---|---|---|---|---|---|---|
| product_id (URL) | Required | String | — | `P###` | — | Must exist |
| product_name | Optional | String | 2–100 characters | Plain text | — | — |
| price_per_unit | Optional | Decimal | ≥ 0.00 | Numeric, 2 decimal places | — | — |
| stock_available | Optional | Integer | ≥ 0 | Whole number | — | — |

---

## 📋 ORDERS

### POST /orders — Create
| Field | Presence | Type | Length / Range | Format | Allowed Values | Referential |
|---|---|---|---|---|---|---|
| order_id | Required | String | — | `O###` (O + 3 digits) | — | Must be unique |
| customer_id | Required | String | — | `C###` | — | References Customers |
| product_id | Required | String | — | `P###` | — | References Products |
| quantity | Required | Integer | 1–999 | Whole number | — | — |
| status | Required | String | — | Exact match | `Pending`, `Delivered` | — |

### PUT /orders/{order_id} — Update
| Field | Presence | Type | Length / Range | Format | Allowed Values | Referential |
|---|---|---|---|---|---|---|
| order_id (URL) | Required | String | — | `O###` | — | Must exist |
| customer_id | Optional | String | — | `C###` | — | References Customers |
| product_id | Optional | String | — | `P###` | — | References Products |
| quantity | Optional | Integer | 1–999 | Whole number | — | — |
| status | Optional | String | — | Exact match | `Pending`, `Delivered` | — |

---

## 📦 COLLECTIONS

### POST /collections — Create
| Field | Presence | Type | Length / Range | Format | Allowed Values | Referential |
|---|---|---|---|---|---|---|
| collection_id | Required | String | — | `CL###` (CL + 3 digits) | — | Must be unique |
| customer_id | Required | String | — | `C###` | — | References Customers |
| order_id | Optional | String | — | `O###` | — | References Orders |
| empty_jugs_returned | Required | Integer | ≥ 0 | Whole number | — | — |
| filled_jugs_released | Required | Integer | ≥ 0 | Whole number | — | — |
| container_balance | Required | Integer | ≥ 0 | Whole number | — | — |
| collected_by | Required | String | Min 2 characters | Plain text | — | — |

### PUT /collections/{collection_id} — Update
| Field | Presence | Type | Length / Range | Format | Allowed Values | Referential |
|---|---|---|---|---|---|---|
| collection_id (URL) | Required | String | — | `CL###` | — | Must exist |
| customer_id | Optional | String | — | `C###` | — | References Customers |
| order_id | Optional | String | — | `O###` | — | References Orders |
| empty_jugs_returned | Optional | Integer | ≥ 0 | Whole number | — | — |
| filled_jugs_released | Optional | Integer | ≥ 0 | Whole number | — | — |
| container_balance | Optional | Integer | ≥ 0 | Whole number | — | — |
| collected_by | Optional | String | Min 2 characters | Plain text | — | — |

---

## ⚠️ Standard Error Response
> When ANY rule fails → return **HTTP 422**:
```json
{"status": 422, "error": "description", "field": "field_name"}
