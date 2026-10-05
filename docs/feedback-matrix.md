# Feedback Matrix
Defines loading → success → error states for all async actions

| Action         | Loading State                          | Success State                                  | Error State                                                                 |
|----------------|----------------------------------------|-------------------------------------------------|-----------------------------------------------------------------------------|
| Create Order   | Button disabled, "Saving…" + spinner   | New row appears, success toast "Order created" | 422 Validation → inline field errors<br/>Network → "Check connection" + retry |
| Read / Load List | Skeleton / list spinner              | Rows render, list fully populated               | 404 → "No orders found"<br/>Network → "Failed to load" + retry button       |
| Edit Order     | Form inputs disabled, "Updating…"      | Row updates, toast "Order updated"              | 422 → inline field errors<br/>404 → "Order not found"<br/>Network → retry    |
| Delete Order   | Delete btn disabled, "Deleting…"        | Row removed, toast "Order deleted"              | 404 → "Order already deleted"<br/>500 → "Couldn't delete"<br/>Network → retry |
