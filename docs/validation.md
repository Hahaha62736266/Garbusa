# Aquaflow Tracker — Validation Rules & Specification

> **Rule**: Every `POST` and `PUT` route passes its body through validation middleware BEFORE reaching the controller. Invalid input returns **HTTP 422** immediately with `error` and `field` set.

---

## 🧑 Customers Validation

### Create (`POST /customers`)
| Field | Rule |
|---|---|
| `customer_id` | Required; format `C###` (C + 3 digits) |
| `full_name` | Required; string 2–100 characters |
| `contact_number` | Required; format `09XX-XXX-XXXX` |
| `address` | Required; minimum 5 characters |
| `container_owned` | Required; integer ≥ 0 |

### Update (`PUT /customers/{customer_id}`)
- `customer_id` in URL must match format `C###`
- Fields optional when provided — but validated per Create rules above

---

## 🧴 Products Validation

### Create (`POST /products`)
| Field | Rule |
|---|---|
| `product_id` | Required; format `P###` |
| `product_name` | Required; string 2–100 characters |
| `price_per_unit` | Required; number ≥ `0.00` |
| `stock_available` | Required; integer ≥ 0 |

### Update (`PUT /products/{product_id}`)
- `product_id` in URL must match format `P###`
- Fields optional — validated if present

---

## 📋 Orders Validation

### Create (`POST /orders`)
| Field | Rule |
|---|---|
| `order_id` | Required; format `O###` |
| `customer_id` | Required; format `C###` |
| `product_id` | Required; format `P###` |
| `quantity` | Required; integer 1–999 |
| `status` | Required; `Pending` or `Delivered` |

### Update (`PUT /orders/{order_id}`)
- `order_id` in URL must match format `O###`
- Fields optional — validated if present

---

## 📦 Collections Validation

### Create (`POST /collections`)
| Field | Rule |
|---|---|
| `collection_id` | Required; format `CL###` |
| `customer_id` | Required; format `C###` |
| `order_id` | Optional; format `O###` if provided |
| `empty_jugs_returned` | Required; integer ≥ 0 |
| `filled_jugs_released` | Required; integer ≥ 0 |
| `container_balance` | Required; integer ≥ 0 |
| `collected_by` | Required; minimum 2 characters |

### Update (`PUT /collections/{collection_id}`)
- `collection_id` in URL must match format `CL###`
- Fields optional — validated if present

---

## ⚠️ Error Response Shape (Standardized)
```json
{
  "status": 422,
  "error": "Human-readable message",
  "field": "field_name"
}
