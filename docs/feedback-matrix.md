# Feedback Matrix
Defines loading → success → error states for all async actions

| Action         | Loading State                          | Success State                                  | Error State                                                                 |
|----------------|----------------------------------------|-------------------------------------------------|-----------------------------------------------------------------------------|
| Create Order   | Button disabled, "Saving…" + spinner   | New row appears, success toast "Order created" | 422 Validation → inline field errors<br/>Network → "Check connection" + retry |
| Read / Load List | Skeleton / list spinner              | Rows render, list fully populated               | 404 → "No orders found"<br/>Network → "Failed to load" + retry button       |
| Edit Order     | Form inputs disabled, "Updating…"      | Row updates, toast "Order updated"              | 422 → inline field errors<br/>404 → "Order not found"<br/>Network → retry    |
| Delete Order   | Delete btn disabled, "Deleting…"        | Row removed, toast "Order deleted"              | 404 → "Order already deleted"<br/>500 → "Couldn't delete"<br/>Network → retry |

# Feedback Matrix — Aquaflow Tracker
Defines loading → success → error states for all async actions

| Action | Loading State | Success State | Error State |
|---|---|---|---|
| Create Customer | Button disabled, "Saving…" + spinner | New row appears, toast "Customer added" | 422 → inline field errors<br/>Network → "Check connection" + retry |

# Feedback Matrix — Aquaflow Tracker
Defines loading → success → error states for all async actions

| Action | Loading State | Success State | Error State |
|---|---|---|---|
| **Create Customer** | Button disabled, "Saving…" + spinner | New row appears, toast "Customer added" | Duplicate ID → inline message<br/>Network → "Check connection" + retry |
| **Load Customers** | Skeleton placeholders | List renders all customers | Network → "Failed to load" + Retry |
| **Edit Customer** | Form disabled, "Updating…" | Row updates, toast "Updated" | Not found → "Customer may be deleted"<br/>Network → Retry |
| **Delete Customer** | Button disabled, "Deleting…" | Row removed, toast "Deleted" | Already gone → "Not found"<br/>Server/Network → "Couldn't delete" + Retry |
| **Create Order** | Button disabled, "Saving…" | New row appears, toast "Order created" | 422/validation → inline per-field errors<br/>Network → Retry |
| **Load Orders** | Skeleton placeholders | List renders with customer/product names | Network → "Failed to load orders" + Retry |
| **Edit Order** | Form disabled, "Updating…" | Row updates, toast "Order updated" | Not found → "Order not found"<br/>Network → Retry |
| **Delete Order** | Delete btn disabled, "Deleting…" | Row removed, toast "Order deleted" | Already gone → "Order already removed"<br/>Server/Network → "Couldn't delete" + Retry |
| Read/Load Customers | Skeleton placeholder | List renders all customers | 404 → "No customers found"<br/>Network → "Failed to load" + retry |
| Edit Customer | Form disabled, "Updating…" | Row updates, toast "Customer updated" | 422 → inline errors<br/>404 → "Customer not found"<br/>Network → retry |
| Delete Customer | Delete btn disabled, "Deleting…" | Row removed, toast "Customer deleted" | 404 → "Customer already deleted"<br/>500 → "Couldn't delete"<br/>Network → retry |

# Feedback & Error Handling Matrix — Phase 3

## Coverage Promise
Every async action → loading shown; every failure → specific human message;
no raw codes / stack traces reach the user.

---

## HTTP Response Handling

| Status | Meaning | Message Shown | Where Handled | Tested |
|---|---|---|---|---|
| **200 / 201** | Success | ✅ "Station saved successfully!" | Form submit | ✅ |
| **400** | Bad request | "Please check your input values and try again." | API fetch | ✅ |
| **422** | Validation failed | "Name and location are required. Please fill both fields." | Create/Edit forms | ✅ |
| **404** | Not found | "This station doesn't exist or may have been removed." | Detail / Edit load | ✅ |
| **500** | Server error | "Something went wrong on our end. Please try again in a moment." | All requests | ✅ |
| **(Network)** | Offline / unreachable | "Can't connect to the server. Check your connection and retry." | Catch-all | ✅ |

---

## Per-Action Feedback

| Action | While Pending | On Success | On Failure Type |
|---|---|---|---|
| **Load List** | Spinner → "Loading stations..." | Shows list or "No stations added yet" | 500 / Network → banner |
| **Load Detail** | Spinner → "Loading station info..." | Full card display | 404 / 500 / Network |
| **Create** | "Saving station..." — button disabled | ✅ "Station created!" → redirect to Detail | 422 inline / 500 / Network |
| **Update** | "Updating..." — button disabled | ✅ "Changes saved" → refresh data | 404 / 422 / 500 / Network |
| **Delete** | "Deleting..." — button disabled | ✅ "Station removed" → redirect to List | 404 / 500 / Network |

---

## Message Standards
- **Voice**: Plain, helpful, AquaFlow consistent
- **No**: `Error 422`, `Internal Server Error`, stack traces
- **Yes**: Action-oriented, what went wrong + what to do next
- **Inline validation**: Near the field, not just top of form
- **Persist**: Error messages stay until resolved; success messages auto-clear
