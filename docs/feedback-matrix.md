# Feedback Matrix
**Project:** Aquaflow Tracker — Water Refilling Station Management System
**Purpose:** Defines UI feedback behavior for all core actions across Loading → Success → Error states

| Action               | Loading State                                                                 | Success State                                                                 | Error State                                                                 |
|----------------------|-------------------------------------------------------------------------------|-------------------------------------------------------------------------------|-----------------------------------------------------------------------------|
| **Create Order**     | "Saving…" message + spinner; submit button disabled                          | New row appears in Orders Log; toast: "Order O### added successfully!"       | 422 validation → highlight fields; toast: "Please check required fields"   |
| **Read / View List** | Skeleton placeholders / "Loading orders…" indicator                          | Orders table renders fully; all rows displayed                                | Network failure → show retry button; "Failed to load orders — tap to retry"|
| **Edit Order**       | "Updating…" + spinner; save button disabled                                  | Changes reflected in table instantly; toast: "Order updated"                 | 422 invalid data → inline messages; toast: "Update failed — check entries" |
| **Delete Order**     | Delete button disabled; "Deleting…" message                                   | Row removed from list; toast: "Order deleted successfully"                   | 500 / not found → toast: "Couldn't delete. Try again"                       |
| **Load Customer**    | "Loading customer…" spinner; fields disabled                                  | Customer details populate form; data ready for edit                           | 404 → toast: "Customer not found"; 500 → "Failed to load customer"          |
| **Create Customer**  | "Saving…" + spinner; submit disabled                                          | Customer added; toast: "Customer C### registered"                             | 422 duplicate/invalid → field errors; "Check contact/ID format"            |
| **Load List**        | Skeleton / spinner shown                                                      | Rows rendered; totals displayed                                               | Offline → retry button; "No internet — check connection"                   |
