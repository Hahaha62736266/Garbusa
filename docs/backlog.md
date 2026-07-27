# Aquaflow Tracker — Project Backlog
## Team: Garbusa | Deliverable 1: Scoping & Wireframes

---

### 👥 Ownership Assignment
| Team Member | Assigned Record Type |
|---|---|
| Pepito | Product Records |
| Taylaran | Order Records |
| Apostol | Customer Records |
| Baydal | Collection Records |
| Obiasad | Wireframes + AI Scope Check |

---

## 🟢 1. Customer Records
| Operation | User Story | Acceptance Criteria |
|---|---|---|
| **Create** | As a station staff, I want to add a new customer record so that I can track their details, deliveries, and gallon balance. | - All required fields (name, contact, address) must be filled before saving<br>- System auto-generates a unique customer ID<br>- New entry appears in the customer list immediately |
| **Read – List** | As a station staff, I want to view a list of all customers so that I can quickly find contact info and outstanding balances. | - Displays all registered customers with ID, name, contact, and current balance<br>- Can search or filter by name or ID<br>- Shows total count of customers |
| **Read – Detail** | As a station staff, I want to open a single customer’s full profile so that I can see their address, contact, and gallon history. | - Shows all stored fields for the selected customer<br>- Lists all past orders and collection records linked to them<br>- Displays accurate up-to-date container balance |
| **Update** | As a station staff, I want to edit an existing customer record so that I can correct addresses, update contacts, or adjust gallon balances. | - Can only edit existing valid customer entries<br>- Changes save and reflect instantly in list and detail views<br>- Prevents duplicate contact numbers if marked unique |
| **Delete** | As a station staff, I want to remove a customer record after confirming so that I can clean up entries for inactive clients. | - Shows a confirmation prompt before deletion<br>- Deleted records no longer appear in active lists<br>- Related order/collection history is retained or clearly marked |

---

## 🟢 2. Product Records
| Operation | User Story | Acceptance Criteria |
|---|---|---|
| **Create** | As a station manager, I want to add a new product/service so that I can offer new refill types or new gallon units for sale. | - Requires product name, price, and initial stock<br>- System auto-generates unique product ID<br>- New product appears in order dropdown lists immediately |
| **Read – List** | As a station manager, I want to view a list of all products so that I can check prices, stock levels, and available options. | - Shows ID, name, price, description, and current stock<br>- Sorts by name or stock level<br>- Highlights items with low stock |
| **Read – Detail** | As a station manager, I want to view a product’s full details so that I can verify pricing, description, and current stock. | - Displays all stored product fields<br>- Shows usage count in active orders<br>- Reflects real-time stock changes |
| **Update** | As a station manager, I want to edit an existing product so that I can adjust prices, update stock, or correct descriptions. | - Can modify any editable field<br>- Price changes apply only to future orders<br>- Stock updates are reflected everywhere |
| **Delete** | As a station manager, I want to delete a product after confirming so that I can remove items no longer offered. | - Requires confirmation prompt<br>- Product is hidden from new order forms<br>- Existing linked orders remain unaffected |

---

## 🟢 3. Order Records
| Operation | User Story | Acceptance Criteria |
|---|---|---|
| **Create** | As a station staff, I want to log a new order so that I can record customer requests, calculate totals, and track delivery status. | - Must select valid existing customer and product<br>- Auto-calculates total amount based on quantity and price<br>- Default status set to "Pending" |
| **Read – List** | As a station staff, I want to view an orders list so that I can see pending deliveries and daily transaction summaries. | - Shows order ID, customer, product, total, date, and status<br>- Can filter by status or date range<br>- Counts pending vs delivered orders |
| **Read – Detail** | As a station staff, I want to open an order’s full details so that I can verify items, amounts, and payment status. | - Displays all order fields plus customer and product names<br>- Shows linked collection records if any<br>- Allows quick status update from this view |
| **Update** | As a station staff, I want to edit an existing order so that I can adjust quantities, update delivery status, or fix entry errors. | - Can only edit orders that are not yet marked completed<br>- Changing quantity recalculates total automatically<br>- Status updates are clearly visible |
| **Delete** | As a station staff, I want to cancel and delete an order after confirming so that I can remove mistakes or cancelled requests. | - Prompts for confirmation<br>- Removes entry from active order queue<br>- Does not affect customer or product records |

---

## 🟢 4. Collection Records
| Operation | User Story | Acceptance Criteria |
|---|---|---|
| **Create** | As a delivery/station staff, I want to log a collection transaction so that I can track returned empties and released filled gallons. | - Must select an existing customer<br>- Enter returned empties and released filled gallons<br>- Auto-computes and updates customer’s container balance |
| **Read – List** | As a station staff, I want to view all collection logs so that I can monitor daily container flow and balances. | - Shows collection ID, customer, returned/released counts, and date<br>- Can filter by date or staff<br>- Shows daily total containers in/out |
| **Read – Detail** | As a station staff, I want to view a single collection record so that I can confirm returns, releases, and updated balance. | - Shows all transaction details<br>- Displays customer balance before and after transaction<br>- Shows who processed the entry |
| **Update** | As a station staff, I want to edit a collection entry so that I can correct counts or update who handled the transaction. | - Only un-finalized entries can be edited<br>- Changes recalculate customer balance automatically<br>- Logs remain consistent |
| **Delete** | As a station staff, I want to remove a collection record after confirming so that I can fix logged errors. | - Requires confirmation<br>- Reverts customer balance to previous state<br>- Record is removed from all lists |

---

## ✅ Compliance Check
- ✔ All **4 record types** have full CRUD coverage
- ✔ **5 stories per type**: Create + List Read + Detail Read + Update + Delete
- ✔ Every story has **1–3 verifiable acceptance criteria**
- ✔ All team members have assigned ownership
- ✔ Matches Aquaflow Tracker’s actual fields and workflow
