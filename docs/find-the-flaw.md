# Find the Flaw — Task 3 Report

## Snippet 1: Missing Input Validation
| Item | Details |
|---|---|
| **Location** | `/api/customers/add` |
| **Flaw** | No validation of required fields, types, or duplicates. Missing status codes. |
| **Why it matters** | Missing keys cause `KeyError` crashes. Negative/string values corrupt data. Duplicate IDs break lookups. Caller can't distinguish success/fail. |
| **Fix** | Check all required keys exist; validate `balance` ≥ 0; reject duplicate IDs; return `201 Created` on success, `400 Bad Request` / `409 Conflict` on errors. |

## Snippet 2: Wrong Status Code & Unhandled 404
| Item | Details |
|---|---|
| **Location** | `/api/orders/<order_id>` GET |
| **Flaw** | "Not found" returns HTTP 200 instead of 404. |
| **Why it matters** | API consumers can't detect missing resources. Logs/metrics won't show actual not-found errors. |
| **Fix** | Add `, 404` to the not-found return line. |

## Snippet 3: Hallucinated Method & Empty Edge Case
| Item | Details |
|---|---|
| **Location** | `/api/expenses/total` |
| **Flaw** | Uses `.sum()` — a method that doesn't exist on Python lists. No error handling. |
| **Why it matters** | Causes `AttributeError` → server returns 500 Internal Server Error to user. Empty list edge case not considered. |
| **Fix** | Use built-in `sum()` function: `sum(item.get("amount", 0) for item in expenses)`. Wrap in try/except → return `500` with message on failure. Returns `0` for empty list. |

## Snippet 4: No Quantity Guard
| Item | Details |
|---|---|
| **Location** | `/api/customers/<cid>/borrow` |
| **Flaw** | Accepts any value including negative numbers. No type check. Missing 404 status. |
| **Why it matters** | Negative quantity silently reduces stock → data corruption. No status code makes debugging hard. |
| **Fix** | Require `quantity` as positive integer → `400` if invalid. Add `, 404` to customer-not-found return. |

## Summary Table
| Snippet | Flaw Category | Severity | Status |
|---|---|---|---|
| 1 | Validation / Duplicates | 🔴 Critical | ✅ Fixed |
| 2 | Wrong Status Code | ⚠️ Medium | ✅ Fixed |
| 3 | Non-existent Method / Edge Case | 🔴 Critical | ✅ Fixed |
| 4 | Missing Guard / Edge Case | 🔴 Critical | ✅ Fixed |

## Key Lessons
- Always validate **every** input from users — never trust it
- Return **correct HTTP status codes**: `200` OK, `201` Created, `400` Bad Input, `404` Not Found, `500` Server Error
- Test **edge cases**: empty lists, zero, negative, missing data
- Python lists use `sum()`, not `.sum()` — check your methods!
- Every error path needs a **specific message + correct code**
