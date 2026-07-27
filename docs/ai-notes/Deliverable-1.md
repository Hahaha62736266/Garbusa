# Aquaflow Tracker — Screens & States
## Deliverable 1 | Task 3 Output

---

### 👤 Customers Module
| Screen Name | Purpose | All States |
|---|---|---|
| Customer List | View all registered customers | ✅ Normal: Table showing ID, name, contact, gallon balance<br>⚠️ Empty: *"No customers added yet. Register your first customer to begin."*<br>❌ Error: *"Could not load customer list. Check connection and try again."* |
| Customer Profile | View full details & history | ✅ Normal: All fields + linked orders/collections<br>⚠️ Empty: *"No transaction history for this customer."*<br>❌ Error: *"Customer record not found."* |
| Add New Customer | Register new client | ✅ Normal: Active form with required fields<br>❌ Error: *"Fill all required fields / Duplicate contact number."* |
| Edit Customer | Update existing info | ✅ Normal: Pre-filled editable form<br>❌ Error: *"Record no longer available for editing."* |
| Delete Confirmation | Confirm removal | ✅ Prompt: *"Delete this customer? History will be retained. This cannot be undone."* |

---

### 🛒 Products Module
| Screen Name | Purpose | All States |
|---|---|---|
| Product Catalog | View all items & stock | ✅ Normal: List with ID, name, price, stock<br>⚠️ Empty: *"No products added yet."*<br>❌ Error: *"Failed to load product catalog."* |
| Product Details | View full specs | ✅ Normal: All fields + usage stats<br>❌ Error: *"Product not found."* |
| Add New Product | Add new refill/jug | ✅ Normal: Active form<br>❌ Error: *"Price/stock cannot be negative."* |
| Edit Product | Update pricing/stock | ✅ Normal: Pre-filled editable form<br>❌ Error: *"Product no longer available."* |
| Delete Confirmation | Confirm removal | ✅ Prompt: *"Remove this product? Existing orders remain unaffected."* |

---

### 📝 Orders Module
| Screen Name | Purpose | All States |
|---|---|---|
| Orders Queue | Track pending/delivered orders | ✅ Normal: Table with status, date, total<br>⚠️ Empty: *"No orders logged yet."*<br>❌ Error: *"Could not load order records."* |
| Order Details | View full transaction | ✅ Normal: All fields + linked customer/product<br>❌ Error: *"Order not found or already removed."* |
| Create New Order | Log new request | ✅ Normal: Dropdowns + auto-calculated total<br>⚠️ Empty: *"Add at least one customer and product first."*<br>❌ Error: *"Select valid entries / Quantity must be ≥ 1."* |
| Update Order | Edit details/status | ✅ Normal: Pre-filled editable form<br>❌ Error: *"Cannot edit — already marked Delivered."* |
| Delete Confirmation | Cancel order | ✅ Prompt: *"Cancel and delete this order? This cannot be reversed."* |

---

### 🧴 Collections Module
| Screen Name | Purpose | All States |
|---|---|---|
| Collection Log | Track gallon exchanges | ✅ Normal: List with returns, releases, balance<br>⚠️ Empty: *"No collection transactions recorded."*<br>❌ Error: *"Failed to load collection history."* |
| Collection Record | View single transaction | ✅ Normal: Full details + before/after balance<br>❌ Error: *"Collection record not found."* |
| Log New Collection | Record exchange | ✅ Normal: Form + auto-balance calculation<br>⚠️ Empty: *"Add a customer first."*<br>❌ Error: *"Counts cannot be negative."* |
| Edit Collection | Correct entry | ✅ Normal: Pre-filled editable form<br>❌ Error: *"Cannot edit — already finalized."* |
| Delete Confirmation | Remove entry | ✅ Prompt: *"Delete this record? Customer balance will be restored."* |

---

✅ **Checklist Complete**:
- [x] List/index per record type
- [x] Detail / Create / Edit screens for all
- [x] Empty states defined
- [x] Error states defined
- [x] Delete confirmation for all delete actions
