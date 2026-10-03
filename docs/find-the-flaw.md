# Code Review & Bug Hunting (Find the Flaw)

**Project:** Aquaflow Tracker
**Phase:** 4 (Code Review & Manual QA)
**Date:** 2026-10-03

---

## 🔍 Found Flaws (AI Generated Snippets & Planted Bugs)

### Flaw 1: Missing Validation on Quantity Update (Backend)
*   **The Flaw:** When an order is created, the quantity is checked to be `>= 1`. However, there was a scenario where a missing total amount calculation allowed negative values.
*   **The Fix:** Added strict type checking and `value < 0` validation checks in `app.py` for both `quantity` and `total_amount`.

### Flaw 2: Silent Failures on AJAX (Frontend)
*   **The Flaw:** Initially, the `fetch()` call for creating an order was wrapped in a try/catch, but if the backend returned a 422 Unprocessable Entity, the `res.ok` check failed, and the catch block triggered a generic "Network error occurred". The specific validation error from the server was lost.
*   **The Fix:** Updated the `handleCreateSubmit` function. It now parses the response JSON regardless of the 201 status, and specifically extracts `data.error` to display in the `#create-error` box if `res.status !== 201`.

### Flaw 3: Double-Submit Race Condition (Frontend)
*   **The Flaw:** A user could click the "Save Order" button multiple times quickly while the network request was pending, creating duplicate orders.
*   **The Fix:** Immediately set `btn.disabled = true` and `btn.classList.add('cursor-not-allowed')` at the beginning of the `handleCreateSubmit` function, and re-enable it in the `finally` block.

### Flaw 4: RLS Bypass with Anon Key (Security)
*   **The Flaw:** Using the public `SUPABASE_KEY` (anon key) for server-side logic when RLS policies are enabled on the `users` table resulted in connection failures. 
*   **The Fix:** Configured the backend to use `SUPABASE_SECRET_KEY` (service_role key) instead, allowing the Flask application to manage database records fully, while applying role-based access control inside the Flask routes (`@roles_required`).
