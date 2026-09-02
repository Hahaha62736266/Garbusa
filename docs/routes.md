---

# 🧪 Route Test Results — Task 3
> Base URL: `http://localhost`
> Response shape: `{ "status": int, "data": { ... }, "error": null }`

---

## Customers — Tested
| Method | Path | Status | Example Response Body |
|---|---|---|---|
| GET | /customers | 200 | `{"message":"listCustomers stub"}` |
| GET | /customers/C001 | 200 | `{"message":"showCustomer stub","customer_id":"C001"}` |
| POST | /customers | 201 | `{"message":"createCustomer stub"}` |
| PUT | /customers/C001 | 200 | `{"message":"updateCustomer stub","customer_id":"C001"}` |
| DELETE | /customers/C001 | 200 | `{"message":"deleteCustomer stub","customer_id":"C001"}` |

---

## Products — Tested
| Method | Path | Status | Example Response Body |
|---|---|---|---|
| GET | /products | 200 | `{"message":"listProducts stub"}` |
| GET | /products/P002 | 200 | `{"message":"showProduct stub","product_id":"P002"}` |
| POST | /products | 201 | `{"message":"createProduct stub"}` |
| PUT | /products/P002 | 200 | `{"message":"updateProduct stub","product_id":"P002"}` |
| DELETE | /products/P002 | 200 | `{"message":"deleteProduct stub","product_id":"P002"}` |

---

## Orders — Tested
| Method | Path | Status | Example Response Body |
|---|---|---|---|
| GET | /orders | 200 | `{"message":"listOrders stub"}` |
| GET | /orders/O005 | 200 | `{"message":"showOrder stub","order_id":"O005"}` |
| POST | /orders | 201 | `{"message":"createOrder stub"}` |
| PUT | /orders/O005 | 200 | `{"message":"updateOrder stub","order_id":"O005"}` |
| DELETE | /orders/O005 | 200 | `{"message":"deleteOrder stub","order_id":"O005"}` |

---

## Collections — Tested
| Method | Path | Status | Example Response Body |
|---|---|---|---|
| GET | /collections | 200 | `{"message":"listCollections stub"}` |
| GET | /collections/CL003 | 200 | `{"message":"showCollection stub","collection_id":"CL003"}` |
| POST | /collections | 201 | `{"message":"createCollection stub"}` |
| PUT | /collections/CL003 | 200 | `{"message":"updateCollection stub","collection_id":"CL003"}` |
| DELETE | /collections/CL003 | 200 | `{"message":"deleteCollection stub","collection_id":"CL003"}` |

---

## Edge-Case Validation
| Request | Expected | Result |
|---|---|---|
| DELETE /orders (no ID) | 404 / 405 | ✅ Returns error status |
| POST /orders/O001 (create with ID) | 405 Method Not Allowed | ✅ Rejected sensibly |
| GET /invalid-path | 404 Not Found | ✅ Standard error response |

---

**Test Summary:** ✅ All 20 routes return correct status code + expected stub body. Parameters echoed correctly. Wrong methods/paths handled gracefully.
