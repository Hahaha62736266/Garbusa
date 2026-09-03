# Validation Matrix

> Rule Vocabulary: **presence, type, length/range, format, allowed values, referential**

---

## POST /customers — Create
| Field | Presence | Type | Length/Range | Format | Allowed Values | Referential |
|---|---|---|---|---|---|---|
| customer_id | required | string | — | C### | — | unique |
| full_name | required | string | 2–100 chars | plain text | — | — |
| contact_number | required | string | — | 09XX-XXX-XXXX | — | — |
| address | required | string | min 5 chars | plain text | — | — |
| container_owned | required | integer | ≥ 0 | whole number | — | — |

## PUT /customers/:customer_id — Update
| Field | Presence | Type | Length/Range | Format | Allowed Values | Referential |
|---|---|---|---|---|---|---|
| customer_id (URL) | required | string | — | C### | — | must exist |
| full_name | optional | string | 2–100 chars | plain text | — | — |
| contact_number | optional | string | — | 09XX-XXX-XXXX | — | — |
| address | optional | string | min 5 chars | plain text | — | — |
| container_owned | optional | integer | ≥ 0 | whole number | — | — |

---

## POST /products — Create
| Field | Presence | Type | Length/Range | Format | Allowed Values | Referential |
|---|---|---|---|---|---|---|
| product_id | required | string | — | P### | — | unique |
| product_name | required | string | 2–100 chars | plain text | — | — |
| price_per_unit | required | decimal | ≥ 0.00 | numeric | — | — |
| stock_available | required | integer | ≥ 0 | whole number | — | — |

## PUT /products/:product_id — Update
| Field | Presence | Type | Length/Range | Format | Allowed Values | Referential |
|---|---|---|---|---|---|---|
| product_id (URL) | required | string | — | P### | — | must exist |
| product_name | optional | string | 2–100 chars | plain text | — | — |
| price_per_unit | optional | decimal | ≥ 0.00 | numeric | — | — |
| stock_available | optional | integer | ≥ 0 | whole number | — | — |

---

## POST /orders — Create
| Field | Presence | Type | Length/Range | Format | Allowed Values | Referential |
|---|---|---|---|---|---|---|
| order_id | required | string | — | O### | — | unique |
| customer_id | required | string | — | C### | — | references Customers |
| product_id | required | string | — | P### | — | references Products |
| quantity | required | integer | 1–999 | whole number | — | — |
| status | required | string | — | exact match | Pending, Delivered | — |

## PUT /orders/:order_id — Update
| Field | Presence | Type | Length/Range | Format | Allowed Values | Referential |
|---|---|---|---|---|---|---|
| order_id (URL) | required | string | — | O### | — | must exist |
| customer_id | optional | string | — | C### | — | references Customers |
| product_id | optional | string | — | P### | — | references Products |
| quantity | optional | integer | 1–999 | whole number | — | — |
| status | optional | string | — | exact match | Pending, Delivered | — |

---

## POST /collections — Create
| Field | Presence | Type | Length/Range | Format | Allowed Values | Referential |
|---|---|---|---|---|---|---|
| collection_id | required | string | — | CL### | — | unique |
| customer_id | required | string | — | C### | — | references Customers |
| order_id | optional | string | — | O### | — | references Orders |
| empty_jugs_returned | required | integer | ≥ 0 | whole number | — | — |
| filled_jugs_released | required | integer | ≥ 0 | whole number | — | — |
| container_balance | required | integer | ≥ 0 | whole number | — | — |
| collected_by | required | string | min 2 chars | plain text | — | — |

## PUT /collections/:collection_id — Update
| Field | Presence | Type | Length/Range | Format | Allowed Values | Referential |
|---|---|---|---|---|---|---|
| collection_id (URL) | required | string | — | CL### | — | must exist |
| customer_id | optional | string | — | C### | — | references Customers |
| order_id | optional | string | — | O### | — | references Orders |
| empty_jugs_returned | optional | integer | ≥ 0 | whole number | — | — |
| filled_jugs_released | optional | integer | ≥ 0 | whole number | — | — |
| container_balance | optional | integer | ≥ 0 | whole number | — | — |
| collected_by | optional | string | min 2 chars | plain text | — | — |

---

## ⚠️ Standard Error Response Format

> **Every validation failure returns EXACTLY this shape:**


### ✅ AFTER PASTING:
> **Save the file** (Ctrl+S) ✅

---

## 🪜 STEP 2 — Add Safety Error Handler to App
### 📍 WHERE TO PASTE:
> Open your **main app file** → usually named `app.py` or `main.py`
> 
> **PASTE THIS AT THE TOP of the file** — right below your existing imports, BEFORE your routes/functions

### 👇 COPY THIS BLOCK & PASTE IT THERE:
```python
# ==================================================
# ✅ STANDARD ERROR HANDLER — PREVENT STACK TRACES LEAKING
# ==================================================
from flask import jsonify

@app.errorhandler(422)
def bad_request(e):
    return jsonify({
        "status": 422,
        "error": str(e.description) if hasattr(e, "description") else "Validation failed",
        "field": getattr(e, "field", "unknown")
    }), 422

@app.errorhandler(Exception)
def handle_all_errors(e):
    # NEVER show raw errors to client
    return jsonify({
        "status": 500,
        "error": "Internal server error. Please check your input or try again.",
        "field": "server"
    }), 500

```json
{
  "status": 422,
  "error": "description of what went wrong",
  "field": "field_name_that_failed"
}
