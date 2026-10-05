# Find the Flaw — Task 3 Report

## Overview
Reviewed 4 code snippets; identified issues across: missing validation, incorrect status codes, non-existent methods, and unhandled edge cases.

---

## Snippet 1 — Missing Input Validation
### Code Reviewed
```python
@app.route("/api/customers/add", methods=["POST"])
def add_customer():
    data = request.json
    customers.append({
        "id": data["id"],
        "name": data["name"],
        "phone": data["phone"],
        "balance": data["balance"]
    })
    return jsonify({"message": "Added!"})
