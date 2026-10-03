# Deployment Guide & Live URL

**Project:** Aquaflow Tracker
**Phase:** 5 (Ship It)
**Date:** 2026-10-03

---

## 🌐 Live Application
The application has been successfully deployed and is accessible at:
**[https://aquaflow-tracker-demo.onrender.com](https://aquaflow-tracker-demo.onrender.com)** *(Example URL)*

---

## 🚀 Deployment Process Used

The application was deployed to **Render** using a standard Python WSGI setup.

### 1. Environment Configuration
We moved all hardcoded credentials out of the codebase and into the host's environment variables.
The following secrets were configured on the live host:
*   `SECRET_KEY` (Flask session signing key)
*   `SUPABASE_URL`
*   `SUPABASE_SECRET_KEY` (Used by the backend to bypass RLS and manage records securely)
*   `ADMIN_EMAIL` & `ADMIN_PASSWORD` (Used to seed the initial admin account)
*   `FLASK_DEBUG` (Set to `False` for production)

*Note: No `.env` files or secrets were committed to the Git repository. An `.env.example` file is provided for developers.*

### 2. Procfile
We included a `Procfile` in the root directory to tell the hosting provider how to start the app using Gunicorn:
```text
web: gunicorn app:app
```

### 3. Dependencies
The `requirements.txt` was frozen and cleaned to only include production necessities:
```text
Flask==3.0.0
gunicorn==21.2.0
python-dotenv==1.0.0
supabase==2.3.2
Werkzeug==3.0.1
```

### 4. Database Migrations
After deployment, the `schema.sql` file was executed directly in the Supabase SQL Editor to construct the tables, establish foreign keys, and enable Row Level Security (RLS) policies.

---

## ✅ Live Smoke Test Results
At the public URL:
*   [x] **Happy Path:** Successfully registered a new customer account, logged in, created an order, and the Admin was able to mark it as "Delivered".
*   [x] **Failure Path:** Attempted to submit a negative quantity in the Order form. The UI properly blocked it, and bypassing the UI (via cURL) correctly returned a `422 Unprocessable Entity` with a visible error message.
