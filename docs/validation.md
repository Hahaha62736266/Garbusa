# Validation Rules & Error Responses — Aquaflow Tracker
> Error shape: { "status": 400, "data": null, "error": "message" }

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
