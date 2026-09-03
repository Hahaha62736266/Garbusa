# Aquaflow Tracker — Validation Rules

> POST/PUT routes run validation BEFORE controller. Returns **422** with `error` + `field` on failure.

---

## 🧑 Customers
### Create
- `customer_id`: Required; format `C###`
- `full_name`: Required; string 2–100 chars
- `contact_number`: Required; format `09XX-XXX-XXXX`
- `address`: Required; min 5 characters
- `container_owned`: Required; integer ≥ 0

### Update
- `customer_id` (URL): Must be `C###`
- Fields optional — validated if provided

---

## 🧴 Products
### Create
- `product_id`: Required; format `P###`
- `product_name`: Required; string 2–100 chars
- `price_per_unit`: Required; number ≥ `0.00`
- `stock_available`: Required; integer ≥ 0

### Update
- `product_id` (URL): Must be `P###`
- Fields optional — validated if present

---

## 📋 Orders
### Create
- `order_id`: Required; format `O###`
- `customer_id`: Required; format `C###`
- `product_id`: Required; format `P###`
- `quantity`: Required; integer 1–999
- `status`: Required; `Pending` or `Delivered`

### Update
- `order_id` (URL): Must be `O###`
- Fields optional — validated if present

---

## 📦 Collections
### Create
- `collection_id`: Required; format `CL###`
- `customer_id`: Required; format `C###`
- `order_id`: Optional; `O###` if provided
- `empty_jugs_returned`: Required; integer ≥ 0
- `filled_jugs_released`: Required; integer ≥ 0
- `container_balance`: Required; integer ≥ 0
- `collected_by`: Required; min 2 characters

### Update
- `collection_id` (URL): Must be `CL###`
- Fields optional — validated if present

---

## ⚠️ Standard Error Shape
```json
{"status":422, "error":"message", "field":"field_name"}
