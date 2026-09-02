# ==========================================================
# DATA LAYER: Customer Model
# Handles storage & retrieval of Customer records
# ==========================================================

# In-memory "database" — replace with real DB later
_customers = {}
_next_id = 1

def all():
    """Return all customers"""
    return list(_customers.values())

def find(customer_id):
    """Find one customer by ID"""
    return _customers.get(customer_id)

def save(data):
    """Create new customer"""
    global _next_id
    record = {
        "id": _next_id,
        "customer_id": data.get("customer_id"),
        "full_name": data.get("full_name"),
        "contact_number": data.get("contact_number"),
        "address": data.get("address"),
        "container_owned": data.get("container_owned", 0),
        "owned_by_user_id": data.get("owned_by_user_id", "admin")  # For authorization
    }
    _customers[data["customer_id"]] = record
    _next_id += 1
    return record

def update(customer_id, data):
    """Update existing customer"""
    record = _customers.get(customer_id)
    if not record:
        return None
    # Merge fields
    if "full_name" in data: record["full_name"] = data["full_name"]
    if "contact_number" in data: record["contact_number"] = data["contact_number"]
    if "address" in data: record["address"] = data["address"]
    if "container_owned" in data: record["container_owned"] = data["container_owned"]
    return record

def remove(customer_id):
    """Delete customer"""
    if customer_id in _customers:
        del _customers[customer_id]
        return True
    return False
