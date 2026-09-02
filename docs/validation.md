# Validation Rules — Aquaflow Tracker

## Customers
| Field | Rule | Error Message |
|---|---|---|
| customer_id | Format `C###`, unique | Must be C001–C999; already exists |
| full_name | Min 2 chars, letters/spaces only | Name too short; invalid characters |
| contact_number | PH format: 09XX-XXX-XXXX | Use 09XX-XXX-XXXX format |
| address | Min 5 chars | Address too short |
| container_owned | Integer ≥ 0 | Cannot be negative |

## Products
| Field | Rule | Error Message |
|---|---|---|
| product_id | Format `P###`, unique | Must be P001–P999; already exists |
| product_name | Required, unique | Name required; already exists |
| price_per_unit | PHP ≥ 0.00, 2 decimals | Price must be ≥ 0.00 PHP |
| stock_available | Integer ≥ 0 | Stock cannot be negative |

## Orders
| Field | Rule | Error Message |
|---|---|---|
| order_id | Format `O###`, unique | Must be O001–O999; already exists |
| customer_id | Must exist in Customers | Customer ID not found |
| product_id | Must exist in Products | Product ID not found |
| quantity | Integer ≥ 1 | Min quantity = 1 |
| total_amount | Auto-calc: price × quantity | Must match calculated total |
| status | Pending / Delivered | Invalid status value |

## Collections
| Field | Rule | Error Message |
|---|---|---|
| collection_id | Format `CL###`, unique | Must be CL001–CL999; already exists |
| empty_jugs_returned | Integer ≥ 0 | Cannot be negative |
| filled_jugs_released | Integer ≥ 0 | Cannot be negative |
| container_balance | Integer ≥ 0 | Balance cannot be negative |
