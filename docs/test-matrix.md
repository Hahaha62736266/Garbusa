# QA Test Matrix & Adversarial Testing

**Project:** Aquaflow Tracker
**Phase:** 4 (Manual QA)
**Date:** 2026-10-03

---

## 🧪 1. Manual QA Test Matrix

This matrix maps core features against various scenarios (Happy Path, Boundary, Invalid Data, Permissions).

| Feature / Action | Happy Path (Expected) | Boundary / Empty | Invalid Data / Adversarial | Permissions (Admin vs. Customer) |
| :--- | :--- | :--- | :--- | :--- |
| **Login** | Valid credentials redirects to `/`. | Empty fields prevent submission (HTML5 `required`). | Wrong password shows inline error. | Works for all roles. |
| **View Orders List** | Data table populates correctly. | Empty state shows "No orders found" graphic if 0 records. | N/A | Customers see only their own orders. Admins see all. |
| **Create Order** | Valid inputs save order, show toast, and table updates. | Qty = 1 (Boundary) works. Empty product/customer caught by frontend. | Negative Qty (-5) caught by backend (422 error shown). | Admins can select any customer. Customers restricted (if implemented). |
| **Update Order Status** | Changing to "Delivered" saves and updates UI badge. | N/A | Submitting a status not in the dropdown (via API manipulation) yields 422. | Only Admin/Delivery can update status. Customers get 403. |
| **Delete Order** | Clicking delete opens modal, confirming removes row. | N/A | Trying to delete a non-existent ID yields 404. | Only Admin can delete. Customer gets 403. |

---

## 😈 2. Adversarial Testing Session Log

**Goal:** Try to break the application through weird inputs, network issues, and out-of-order actions.

1.  **Test:** Submit "Emoji" and "HTML tags" into the Order Total field.
    *   *Result:* Frontend `type="number"` blocks it. Bypassing frontend (Postman) results in backend throwing a `ValueError` during float conversion, safely returning a 422 error.
    *   *Status:* PASS 🟢
2.  **Test:** Double-click the "Save Order" button extremely fast to create duplicate records.
    *   *Result:* The button is disabled (`btn.disabled = true`) on the very first click, preventing the second click from registering while the network request is pending.
    *   *Status:* PASS 🟢
3.  **Test:** Simulate a slow network / backend crash (shut down Flask server mid-request).
    *   *Result:* The `catch (err)` block in `handleCreateSubmit` catches the fetch failure. The UI displays "Network error occurred" in the red error box, and the loading spinner disappears, unblocking the UI.
    *   *Status:* PASS 🟢
4.  **Test:** Navigate directly to `/orders` without being logged in.
    *   *Result:* Flask's `@login_required` middleware detects no session and redirects immediately to `/login`.
    *   *Status:* PASS 🟢
5.  **Test:** Customer trying to delete an order via raw API request.
    *   *Result:* `DELETE /api/orders/<id>` is guarded by `@roles_required("admin")`. The backend rejects the request with a 403 Forbidden.
    *   *Status:* PASS 🟢

All critical paths degrade gracefully and no data loss occurs.
