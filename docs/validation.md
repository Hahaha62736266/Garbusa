# Validation Rules & Error Responses — Aquaflow Tracker


## Customers
| Field | Rule | Error Message |
|---|---|---|
| customer_id | Format C###, unique | Must be C+3 digits, unique |
| full_name | Min 2 chars | Min 2 characters required |
| contact_number | 09XX-XXX-XXXX | Use format 09XX-XXX-XXXX |
| address | Min 5 chars | Min 5 characters required |
| container_owned | Integer ≥ 0 | Cannot be negative |

## Products
| Field | Rule | Error Message |
|---|---|---|
| product_id | Format P###, unique | Must be P+3 digits, unique |
| product_name | Min 2 chars, unique | Min 2 chars, must be unique |
| price_per_unit | ≥0.00, 2 decimals | Price ≥ 0.00 PHP |
| stock_available | Integer ≥ 0 | Cannot be negative |

## Orders
| Field | Rule | Error Message |
|---|---|---|
| order_id | Format O###, unique | Must be O+3 digits, unique |
| customer_id | Must exist in Customers | Customer ID not found |
| product_id | Must exist in Products | Product ID not found |
| quantity | ≥ 1 | Min quantity = 1 |
| status | Pending / Delivered | Must be Pending or Delivered |

## Collections
| Field | Rule | Error Message |
|---|---|---|
| collection_id | Format CL###, unique | Must be CL+3 digits, unique |
| customer_id | Must exist in Customers | Customer ID not found |
| empty_jugs_returned | Integer ≥ 0 | Cannot be negative |
| filled_jugs_released | Integer ≥ 0 | Cannot be negative |
| container_balance | Integer ≥ 0 | Cannot be negative |


# Validation Matrix — Aquaflow Tracker
> Task 1: Validation Rules for Create & Update Routes Only
> Vocabulary: presence · type · length/range · format · allowed values · referential

---

## POST /customers & PUT /customers/:customer_id
| Field | Presence | Type | Length / Range | Format | Allowed Values | Referential |
|---|---|---|---|---|---|---|
| customer_id | required | string | 5 chars exactly | C + 3 digits (C001–C999) | unique | — |
| full_name | required | string | 2–100 chars | letters & spaces only | — | — |
| contact_number | required | string | 12 chars exactly | 09XX-XXX-XXXX | PH format | — |
| address | required | string | min 5 chars | plain text | — | — |
| container_owned | required | integer | ≥ 0 | whole number | — | — |

---

## POST /products & PUT /products/:product_id
| Field | Presence | Type | Length / Range | Format | Allowed Values | Referential |
|---|---|---|---|---|---|---|
| product_id | required | string | 5 chars exactly | P + 3 digits (P001–P999) | unique | — |
| product_name | required | string | 2–100 chars | plain text | unique | — |
| price_per_unit | required | decimal | ≥ 0.00, 2 decimals max | PHP currency | — | — |
| description | optional | string | 0–200 chars | plain text | — | — |
| stock_available | required | integer | ≥ 0 | whole number | — | — |

---

## POST /orders & PUT /orders/:order_id
| Field | Presence | Type | Length / Range | Format | Allowed Values | Referential |
|---|---|---|---|---|---|---|
| order_id | required | string | 5 chars exactly | O + 3 digits (O001–O999) | unique | — |
| customer_id | required | string | 5 chars exactly | C### format | — | exists in Customers |
| product_id | required | string | 5 chars exactly | P### format | — | exists in Products |
| quantity | required | integer | 1–999 | whole number | — | — |
| total_amount | required | decimal | ≥ 0.00 | price × quantity | matches calculation | — |
| status | required | string | — | — | Pending, Delivered | — |

---

## POST /collections & PUT /collections/:collection_id
| Field | Presence | Type | Length / Range | Format | Allowed Values | Referential |
|---|---|---|---|---|---|---|
| collection_id | required | string | 7 chars exactly | CL + 3 digits (CL001–CL999) | unique | — |
| customer_id | required | string | 5 chars exactly | C### format | — | exists in Customers |
| order_id | optional | string | 5 chars exactly | O### format | — | if given, exists in Orders |
| empty_jugs_returned | required | integer | ≥ 0 | whole number | — | — |
| filled_jugs_released | required | integer | ≥ 0 | whole number | — | — |
| container_balance | required | integer | ≥ 0 | whole number | — | — |
| collected_by | required | string | 2–50 chars | staff name | — | — |

# Aquaflow Tracker — Validation Rules

## Customers
- customer_id: required, format C###
- full_name: required, string 2–100 chars
- contact_number: required, format 09XX-XXX-XXXX
- address: required, min 5 chars
- container_owned: required, integer ≥ 0

## Products
- product_id: required, format P###
- product_name: required, string 2–100 chars
- price_per_unit: required, number ≥ 0.00
- stock_available: required, integer ≥ 0

## Orders
- order_id: required, format O###
- customer_id: required, format C###
- product_id: required, format P###
- quantity: required, integer 1–999
- status: required, one of: Pending, Delivered

## Collections
- collection_id: required, format CL###
- customer_id: required, format C###
- order_id: optional, format O### if provided
- empty_jugs_returned: required, integer ≥ 0
- filled_jugs_released: required, integer ≥ 0
- container_balance: required, integer ≥ 0
- collected_by: required, min 2 chars

✅ All POST/PUT routes validated; returns 422 + error + field on failure.
