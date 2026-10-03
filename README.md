# Garbusa — Aquaflow Tracker
### Water Refilling Station Management System

A lightweight web application designed to digitalize daily sales, deliveries, and container balances for local water refilling stations.

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

**Aquaflow Tracker** provides a management portal that digitalizes daily order queues, logs customer purchase profiles, and keeps a real-time count of containers currently out on loan, ensuring smoother logistics and zero lost inventory.

---

## 🏗️ Architecture & Project Structure

The project is built on **Flask** with **Supabase (PostgreSQL)** for database storage (with automatic fallback to an in-memory database when Supabase is disconnected).

```text
Garbusa/
├── app.py                  # Main Flask application (Routes, Auth, DB access)
├── schema.sql              # Supabase database schema & RLS security policies
├── Procfile                # Production deployment configuration (Gunicorn)
├── requirements.txt        # Python dependencies
├── .env.example            # Template for required environment variables
├── test_pipeline.py        # Task 3 lab test pipeline script (Arrange / Act / Assert)
├── controllers/            # Controller layer functions
├── middleware/             # Validation and authorization middleware
├── templates/              # HTML Frontend Templates (Jinja2)
│   ├── index.html          # Operational Dashboard UI
│   ├── login.html          # User Login page
│   └── register.html       # Customer / Collector Registration page
├── tests/                  # Automated Pytest suite
│   ├── conftest.py         # Test configuration & fixtures
│   ├── test_api.py         # Full API integration & auth test suite
│   └── test_validation_pipeline.py  # Pytest pipeline cases
├── .github/workflows/
│   └── tests.yml           # GitHub Actions automated test workflow
└── archive/                # Archived legacy frontends & experimental routes
```

---

## 🗄️ Core Data Entities

1. **Users (`users`)**
   - Fields: `id`, `email`, `password_hash`, `full_name`, `role` (`admin` | `delivery` | `customer`), `customer_id` (FK).
2. **Customers (`customers`)**
   - Fields: `customer_id` (PK), `full_name`, `contact_number`, `address`, `container_owned`, `registration_date`.
3. **Products (`products`)**
   - Fields: `product_id` (PK), `product_name`, `price_per_unit`, `description`, `stock_available`.
4. **Orders (`orders`)**
   - Fields: `order_id` (PK), `customer_id` (FK), `product_id` (FK), `quantity`, `total_amount`, `order_date`, `status` (`Pending` | `Delivered`).
5. **Collections (`collections`)**
   - Fields: `collection_id` (PK), `customer_id` (FK), `order_id` (FK), `empty_jugs_returned`, `filled_jugs_released`, `container_balance`, `collection_date`, `collected_by`.

---

## 🔐 Authentication & Roles

* **Sessions**: Signed HTTP-only session cookies managed by Flask.
* **Passwords**: Password hashing using `werkzeug.security`.
* **Role Permissions**:
  - `Admin`: Full access to all endpoints and records. Creates products and customers.
  - `Collector / Delivery`: Manages orders, updates delivery status (`Pending` -> `Delivered`), records gallon collections.
  - `Customer`: Views own records and places orders for own account.
  - **Self-registration**: Users can register as `Customer` or `Collector`. Admin accounts cannot be self-registered (created on startup via environment variables or by system admin).

---

## 🛠️ Local Development & Setup

### Prerequisites
* Python 3.10+
* Git

### Installation & Execution
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd Garbusa
   ```

2. Copy the environment template and set your configuration:
   ```bash
   cp .env.example .env
   ```
   *Fill in `SUPABASE_URL`, `SUPABASE_SECRET_KEY`, and a random `SECRET_KEY`.*

3. Set up database tables in your Supabase project:
   - Run the contents of `schema.sql` in the **Supabase SQL Editor**.

4. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. Run the application:
   ```bash
   python app.py
   ```
   *The server starts at `http://127.0.0.1:5000`.*

---

## 🧪 Automated Testing

Run the full automated test suite using `pytest`:

```bash
python -m pytest tests/ -v
```

Run the Task 3 lab pipeline test runner:

```bash
python test_pipeline.py
```

All tests run completely offline against an in-memory isolated database instance.

---

## 🚀 Deployment

The app is configured for deployment on platforms like Render, Heroku, or Fly.io using Gunicorn.

- Start command (via `Procfile`):
  ```bash
  web: gunicorn app:app --bind 0.0.0.0:$PORT --workers 2 --preload
  ```
