# 🎨 WIREFRAME SPECIFICATION — Aquaflow Tracker
## Team: Garbusa | Deliverable 1 — Task 4
**Folder:** `/docs/wireframes/`
**Rule:** Low‑fidelity only — boxes + labels. Every file labeled with **Screen Name / Related Stories / Designer**.
**Commit:** Branch → PR → Review — never push to main.

---

## 👤 CUSTOMER MODULE — Designer: Apostol
| File Name | Label | Layout Guide |
|---|---|---|
| `customer-list-normal.png` | **Screen:** Customer List — Normal<br>**Stories:** Customer Read‑List<br>**Designer:** Apostol | Header → [+ Add Customer] + Search → Table: ID / Name / Contact / Gallon Balance |
| `customer-list-empty.png` | **Screen:** Customer List — Empty<br>**Stories:** Customer Read‑List<br>**Designer:** Apostol | Header → Centered: *No customers added yet.* → [+ Add First Customer] |
| `customer-list-error.png` | **Screen:** Customer List — Error<br>**Stories:** Customer Read‑List<br>**Designer:** Apostol | Header → Alert: *⚠️ Could not load list.* → [Retry] |
| `customer-detail.png` | **Screen:** Customer Profile — Normal<br>**Stories:** Customer Read‑Detail<br>**Designer:** Apostol | Header → Fields → History → [Edit] [Delete] |
| `customer-detail-error.png` | **Screen:** Customer Profile — Error<br>**Stories:** Customer Read‑Detail<br>**Designer:** Apostol | Header → Alert: *⚠️ Record not found.* → [Back] |
| `customer-create.png` | **Screen:** Add New Customer<br>**Stories:** Customer Create<br>**Designer:** Apostol | Header → Form → [Save] [Cancel] |
| `customer-create-error.png` | **Screen:** Add New Customer — Error<br>**Stories:** Customer Create<br>**Designer:** Apostol | Form + alert: *⚠️ Fill all fields / Duplicate contact.* |
| `customer-edit.png` | **Screen:** Edit Customer<br>**Stories:** Customer Update<br>**Designer:** Apostol | Header → Pre‑filled form → [Update] [Cancel] |
| `customer-edit-error.png` | **Screen:** Edit Customer — Error<br>**Stories:** Customer Update<br>**Designer:** Apostol | Form + alert: *⚠️ Record no longer editable.* |
| `customer-delete-confirm.png` | **Screen:** Delete Confirm — Customer<br>**Stories:** Customer Delete<br>**Designer:** Apostol | Pop‑up: *Delete? History retained.* → [Cancel] [Yes, Delete] |

---

## 🛒 PRODUCT MODULE — Designer: Pepito
| File Name | Label | Layout Guide |
|---|---|---|
| `product-list-normal.png` | **Screen:** Product Catalog — Normal<br>**Stories:** Product Read‑List<br>**Designer:** Pepito | Header → [+ Add Product] → Table: ID / Name / Price / Stock |
| `product-list-empty.png` | **Screen:** Product Catalog — Empty<br>**Stories:** Product Read‑List<br>**Designer:** Pepito | Header → *No products added yet.* → [+ Add First Product] |
| `product-list-error.png` | **Screen:** Product Catalog — Error<br>**Stories:** Product Read‑List<br>**Designer:** Pepito | Header → *⚠️ Failed to load catalog.* → [Retry] |
| `product-detail.png` | **Screen:** Product Details — Normal<br>**Stories:** Product Read‑Detail<br>**Designer:** Pepito | Header → Fields → [Edit] [Delete] |
| `product-detail-error.png` | **Screen:** Product Details — Error<br>**Stories:** Product Read‑Detail<br>**Designer:** Pepito | Header → *⚠️ Product not found.* → [Back] |
| `product-create.png` | **Screen:** Add New Product<br>**Stories:** Product Create<br>**Designer:** Pepito | Header → Form → [Save] [Cancel] |
| `product-create-error.png` | **Screen:** Add New Product — Error<br>**Stories:** Product Create<br>**Designer:** Pepito | Form + alert: *⚠️ Price/stock cannot be negative.* |
| `product-edit.png` | **Screen:** Edit Product<br>**Stories:** Product Update<br>**Designer:** Pepito | Header → Pre‑filled form → [Update] [Cancel] |
| `product-edit-error.png` | **Screen:** Edit Product — Error<br>**Stories:** Product Update<br>**Designer:** Pepito | Form + alert: *⚠️ Product unavailable.* |
| `product-delete-confirm.png` | **Screen:** Delete Confirm — Product<br>**Stories:** Product Delete<br>**Designer:** Pepito | Pop‑up: *Remove product? Orders safe.* → [Cancel] [Delete] |

---

## 📝 ORDER MODULE — Designer: Taylaran
| File Name | Label | Layout Guide |
|---|---|---|
| `order-list-normal.png` | **Screen:** Orders Queue — Normal<br>**Stories:** Order Read‑List<br>**Designer:** Taylaran | Header → [+ New Order] + Filter → Table |
| `order-list-empty.png` | **Screen:** Orders Queue — Empty<br>**Stories:** Order Read‑List<br>**Designer:** Taylaran | Header → *No orders logged yet.* → [+ Log First] |
| `order-list-error.png` | **Screen:** Orders Queue — Error<br>**Stories:** Order Read‑List<br>**Designer:** Taylaran | Header → *⚠️ Could not load orders.* → [Retry] |
| `order-detail.png` | **Screen:** Order Details — Normal<br>**Stories:** Order Read‑Detail<br>**Designer:** Taylaran | Header → Details → [Edit] [Delete] |
| `order-detail-error.png` | **Screen:** Order Details — Error<br>**Stories:** Order Read‑Detail<br>**Designer:** Taylaran | Header → *⚠️ Order not found.* → [Back] |
| `order-create.png` | **Screen:** Create New Order<br>**Stories:** Order Create<br>**Designer:** Taylaran | Header → Dropdowns → Qty → Total → [Log] [Cancel] |
| `order-create-empty.png` | **Screen:** Create Order — Empty<br>**Stories:** Order Create<br>**Designer:** Taylaran | Form + alert: *⚠️ Add customer & product first.* |
| `order-create-error.png` | **Screen:** Create Order — Error<br>**Stories:** Order Create<br>**Designer:** Taylaran | Form + alert: *⚠️ Select valid entries.* |
| `order-edit.png` | **Screen:** Update Order<br>**Stories:** Order Update<br>**Designer:** Taylaran | Header → Pre‑filled form → [Update] [Cancel] |
| `order-edit-error.png` | **Screen:** Update Order — Error<br>**Stories:** Order Update<br>**Designer:** Taylaran | Form + alert: *⚠️ Already delivered.* |
| `order-delete-confirm.png` | **Screen:** Delete Confirm — Order<br>**Stories:** Order Delete<br>**Designer:** Taylaran | Pop‑up: *Cancel order? Cannot undo.* → [Cancel] [Yes] |

---

## 🧴 COLLECTION MODULE — Designer: Baydal
| File Name | Label | Layout Guide |
|---|---|---|
| `collection-list-normal.png` | **Screen:** Collection Log — Normal<br>**Stories:** Collection Read‑List<br>**Designer:** Baydal | Header → [+ Log Collection] → Table |
| `collection-list-empty.png` | **Screen:** Collection Log — Empty<br>**Stories:** Collection Read‑List<br>**Designer:** Baydal | Header → *No collections recorded.* → [+ Log First] |
| `collection-list-error.png` | **Screen:** Collection Log — Error<br>**Stories:** Collection Read‑List<br>**Designer:** Baydal | Header → *⚠️ Failed to load log.* → [Retry] |
| `collection-detail.png` | **Screen:** Collection Record — Normal<br>**Stories:** Collection Read‑Detail<br>**Designer:** Baydal | Header → Details + balance → [Edit] [Delete] |
| `collection-detail-error.png` | **Screen:** Collection Record — Error<br>**Stories:** Collection Read‑Detail<br>**Designer:** Baydal | Header → *⚠️ Record not found.* → [Back] |
| `collection-create.png` | **Screen:** Log New Collection<br>**Stories:** Collection Create<br>**Designer:** Baydal | Header → Dropdown → Counts → Auto Balance → [Save] [Cancel] |
| `collection-create-empty.png` | **Screen:** Log Collection — Empty<br>**Stories:** Collection Create<br>**Designer:** Baydal | Form + alert: *⚠️ Add customer first.* |
| `collection-create-error.png` | **Screen:** Log Collection — Error<br>**Stories:** Collection Create<br>**Designer:** Baydal | Form + alert: *⚠️ Counts cannot be negative.* |
| `collection-edit.png` | **Screen:** Edit Collection<br>**Stories:** Collection Update<br>**Designer:** Baydal | Header → Pre‑filled form → [Update] [Cancel] |
| `collection-edit-error.png` | **Screen:** Edit Collection — Error<br>**Stories:** Collection Update<br>**Designer:** Baydal | Form + alert: *⚠️ Already finalized.* |
| `collection-delete-confirm.png` | **Screen:** Delete Confirm — Collection<br>**Stories:** Collection Delete<br>**Designer:** Baydal | Pop‑up: *Delete? Balance restores.* → [Cancel] [Yes] |
