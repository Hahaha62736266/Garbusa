# Component Library — Aquaflow Tracker
## Task 1: Break Wireframes into Reusable Components

**Project:** Aquaflow Tracker — Water Refilling Station Management System
**Branch:** `move-wireframes-to-folder`
**Date:** 2026-09-30

---

## 🎯 Purpose
Identify reusable UI elements across all screens so we build **once, reuse everywhere** — consistent design, faster development, easier updates.

---

## 📋 Master Component List

| # | Component Name | Type | Reuse Level | Found On |
|---|---|---|---|---|
| C01 | **Navbar** | Layout | ⭐⭐⭐⭐⭐ | All screens |
| C02 | **PageHeader** | Layout | ⭐⭐⭐⭐⭐ | All screens |
| C03 | **ListRow** | Data | ⭐⭐⭐⭐⭐ | Orders, Customers, Products, Collections |
| C04 | **StatusBadge** | Display | ⭐⭐⭐⭐ | Orders, Collections |
| C05 | **DataCard** | Container | ⭐⭐⭐ | Dashboard, Summary widgets |
| C06 | **FormField** | Form | ⭐⭐⭐⭐ | All create/edit forms |
| C07 | **ActionButton** | Control | ⭐⭐⭐⭐ | All screens |
| C08 | **DataTable** | Data | ⭐⭐⭐ | List views |
| C09 | **AlertMessage** | Feedback | ⭐⭐⭐ | Form results, system notices |
| C10 | **ContainerBalance** | Specialized | ⭐⭐ | Customer profile, Collection log |
| C11 | **Footer** | Layout | ⭐⭐⭐⭐⭐ | All screens |

> **🏆 Most Reused: `ListRow`** — appears on every list screen. Build it cleanly once, use everywhere.

---

## 📱 Screen-to-Component Mapping

### 1. Dashboard / Home
- Navbar (C01)
- PageHeader (C02)
- DataCard × 4 (C05) — Today's Orders, Active Customers, Stock Levels, Pending Deliveries
- ListRow (C03) — Recent activity preview
- Footer (C11)

### 2. Customers — List
- Navbar (C01)
- PageHeader + "Add Customer" button (C02 + C07)
- DataTable (C08) → contains ListRow (C03) for each customer
  - StatusBadge (C04) — Active/Inactive
- ActionButton — Edit, Delete per row (C07)
- Footer (C11)

### 3. Customers — Add/Edit Form
- Navbar (C01)
- PageHeader (C02)
- FormField — Name, Contact, Address, Initial Jugs (C06 × 4)
- ActionButton — Save / Cancel (C07 × 2)
- AlertMessage — Success/Error feedback (C09)
- Footer (C11)

### 4. Orders — Create
- Navbar (C01)
- PageHeader (C02)
- FormField — Customer select, Product select, Quantity (C06 × 3)
- DataCard — Price preview (C05)
- ActionButton — Submit Order (C07)
- AlertMessage — Order # confirmation (C09)
- Footer (C11)

### 5. Orders — Queue / List
- Navbar (C01)
- PageHeader + Filter buttons (C02 + C07)
- ListRow — One per order (C03)
  - StatusBadge — Pending / Delivered / Cancelled (C04)
- ActionButton — Mark Delivered / View Details (C07)
- Footer (C11)

### 6. Products — Inventory
- Navbar (C01)
- PageHeader (C02)
- ListRow — Product name, price, stock (C03)
- StatusBadge — In Stock / Low Stock / Out of Stock (C04)
- ActionButton — Restock / Edit (C07)
- Footer (C11)

### 7. Collections — Delivery Log
- Navbar (C01)
- PageHeader (C02)
- FormField — Customer, Jugs In, Jugs Out (C06 × 3)
- ContainerBalance — Running total display (C10)
- ListRow — Past collection history (C03)
- ActionButton — Record Collection (C07)
- Footer (C11)

---

## 🧱 Component Specifications

### C01 — Navbar
