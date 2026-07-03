# Garbusa
# Aquaflow Tracker - Water Refilling Station Management System

A lightweight, CRUD-shaped web application designed to digitalize daily sales, deliveries, and container balances for local water refilling stations.

---

## 👥 Team Roster & Roles (Sprint 1)

*   **Repo Lead:** Pepito — *Branch protection, merge hygiene, and repository health.*
*   **Board Lead:** Taylaran — *Task board upkeep, ticket assignment, and progress tracking.*
*   **Scribe:** Apostol — *Decision log documentation and sprint retrospective notes.*
*   **Builder 1:** Baydal — *Core application feature development.*
*   **Builder 2:** Obiasad — *Core application feature development.*

---

## 📝 Problem Statement

Local water refilling stations heavily rely on manual paper logbooks or loose whiteboards to track custom deliveries, walk-in orders, and customer-borrowed slim/round gallons. This manual approach leads to missing delivery windows, unaccounted-for container inventory, and inaccurate calculations of outstanding customer balances. 

**Aquaflow Tracker** provides a lightweight management portal that digitalizes daily order queues, logs customer purchase profiles, and keeps a real-time count of containers currently out on loan, ensuring smoother logistics and zero lost inventory over a 12-week development scope.

---

## 🗄️ Core CRUD Entities & Record Types

The application manages data workflows across three tightly related record types:

1.  **Customer Records (CRUD)**
    *   *Fields:* Customer ID, Name, Delivery Address, Contact Number, Outstanding Gallon Balance.
2.  **Order Logs (CRUD)**
    *   *Fields:* Order ID, Customer ID (Foreign Key), Order Date, Delivery Status (`Pending` / `Delivered`), Total Price, Payment Status.
3.  **Gallon Inventory Tracker (CRUD)**
    *   *Fields:* Container ID, Type (`Slim 5-Gallon` / `Round 5-Gallon`), Physical Stock Available, Total Containers Loaned Out.

---

## 🛠️ Tech Stack & Setup (To Be Updated in Week 3)

> 💡 *Note: This project scaffolding is configured for a Python/Streamlit ecosystem (or your team's chosen alternative).*

### Prerequisites
*   Python 3.10+
*   Git

### Local Installation
1. Clone the repository:
   ```bash
   git clone <your-repository-url>
   cd <repository-folder-name>

   # Customer Records

## Fields:
- `customer_id` (Unique identifier, e.g., integer or UUID)
- `first_name` (String)
- `last_name` (String)
- `email` (String, unique)
- `phone_number` (String)
- `registration_date` (Date/Timestamp)

## Example Records:
- **Customer 1:**
    - `customer_id`: 1001
    - `first_name`: Alice
    - `last_name`: Wonderland
    - `email`: alice.w@example.com
    - `phone_number`: 555-1234
    - `registration_date`: 2023-01-15T10:00:00Z
- **Customer 2:**
    - `customer_id`: 1002
    - `first_name`: Bob
    - `last_name`: The Builder
    - `email`: bob.b@example.com
    - `phone_number`: 555-5678
    - `registration_date`: 2023-02-20T11:30:00Z
