# Error Handling & Feedback Matrix

**Project:** Aquaflow Tracker — Water Refilling Station Management System
**Phase:** 3 (Error Handling & User Feedback)
**Date:** 2026-10-03

---

## 🎯 Purpose
This matrix defines how the user interface responds during every asynchronous action's lifecycle (Loading, Success, Error). Consistent feedback ensures the user always knows what the system is doing, preventing double-submissions and confusion.

---

## 📊 The Feedback Matrix

| Action / Request | Loading State | Success State | Error State |
| :--- | :--- | :--- | :--- |
| **Load Orders (GET)** | Full-container spinner with "Loading orders..." | Orders render in table; UI unblocks. | Full-container warning icon with "Failed to load data" & Retry button. |
| **Create Order (POST)** | "Save Order" button disabled & opacity-75; button spinner spins. | Modal closes; Table refreshes; Success Toast ("Order created successfully!"). | Modal stays open; red error box appears above buttons with API message (e.g., 422). |
| **Update Order (PATCH)** | "Update" button disabled & opacity-75; button spinner spins. | Modal closes; Table refreshes; Success Toast ("Order updated successfully!"). | Modal stays open; red error box appears above buttons with API message. |
| **Delete Order (DELETE)** | "Delete" button disabled & opacity-75; button spinner spins. | Modal closes; Row vanishes on refresh; Success Toast ("Order deleted successfully"). | Modal stays open; red error box appears above buttons with API message. |
| **Login (POST)** | "Sign In" button disabled. | Redirect to Dashboard (`/`). | Inline red text ("Invalid email or password"). |
| **Register (POST)** | "Register" button disabled. | Redirect to Dashboard (`/`). | Inline red text below form with 422 error details. |

---

## 🛠️ Feedback Patterns Implemented

### 1. Loading Indicators
*   **Initial Page Load:** We use a full-container overlay (`#loading-state`) so the user doesn't see broken tables while data fetches.
*   **Forms/Modals:** Action buttons disable themselves (`btn.disabled = true`, `cursor-not-allowed`) to prevent double-clicks, and a FontAwesome spinner (`fa-circle-notch fa-spin`) appears inside the button.

### 2. Error Visibility
*   **General/Network Errors (500):** Addressed via the form-level error boxes (`#create-error`, `#edit-error`, `#delete-error`) that display "Network error occurred" or the server's 500 error string.
*   **Validation Errors (422):** The backend returns `{ "error": "quantity must be at least 1" }`. The frontend reads this JSON and displays it in the same form-level error box. (Currently implemented as form-level, but easily extendable to field-level by mapping error strings to field IDs).

### 3. Destructive Action Confirmation
*   **Delete Modal:** Before sending a `DELETE /api/orders/<id>` request, a confirmation modal (`#delete-modal`) forces the user to confirm. It prominently displays the ID of the record being deleted and warns that the action is irreversible.

### 4. Success Toasts
*   A sliding notification element (`#toast`) at the bottom right of the screen provides non-intrusive feedback for successful POST, PATCH, and DELETE operations. It auto-hides after 3 seconds.
