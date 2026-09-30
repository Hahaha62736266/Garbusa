"""Customer Controller — Aquaflow Tracker"""
from datetime import date
from models import customer_model

# In-memory database
customers_db = {}

# Model wrapper — matches test pattern
class CustomerModel:
    def __init__(self, data):
        self.data = data

    def create(self):
        try:
            # Extract data safely
            if hasattr(self.data, '__dict__'):
                payload = self.data.__dict__
            elif hasattr(self.data, 'json') and self.data.json is not None:
                payload = self.data.json
            else:
                payload = self.data if isinstance(self.data, dict) else {}

            # Create new customer
            new_id = f"C{len(customers_db)+1:03d}"
            customer = {
                "customer_id": new_id,
                "full_name": payload.get("full_name"),
                "contact_number": payload.get("contact_number"),
                "address": payload.get("address"),
                "container_owned": payload.get("container_owned", 0),
                "registration_date": str(date.today()),
                "owned_by_user_id": payload.get("owned_by_user_id", "admin")
            }
            customers_db[new_id] = customer

            # Save to model if available
            try:
                customer_model.save(customer)
            except Exception:
                pass

            return {"success": True, "data": customer}
        except Exception as e:
            return {"success": False, "error": str(e)}

# Controller functions
def list_customers():
    return {
        "status": 200,
        "message": "Customers retrieved successfully",
        "data": list(customers_db.values())
    }

def showCustomer(customer_id):
    if customer_id not in customers_db:
        return {"status": 404, "error": "Not Found", "message": "Customer not found"}
    return {
        "status": 200,
        "message": "Customer retrieved",
        "data": customers_db[customer_id]
    }

def createCustomer(req):
    data = getattr(req, 'validatedBody', None) or getattr(req, 'body', None) or {}
    model = CustomerModel(data)
    result = model.create()
    if result.get("success"):
        return {
            "status": 201,
            "message": "Customer created successfully",
            "data": result.get("data")
        }
    return {
        "status": 500,
        "message": "Failed to create customer",
        "error": result.get("error", "Unknown error")
    }

def updateCustomer(customer_id, data):
    payload = getattr(data, 'json', None) or data
    if customer_id not in customers_db:
        return {"status": 404, "error": "Not Found", "message": "Customer not found"}
    for k, v in payload.items():
        if k != "customer_id":
            customers_db[customer_id][k] = v
    return {
        "status": 200,
        "message": "Customer updated",
        "data": customers_db[customer_id]
    }

def deleteCustomer(customer_id):
    if customer_id not in customers_db:
        return {"status": 404, "error": "Not Found", "message": "Customer not found"}
    deleted = customers_db.pop(customer_id)
    return {
        "status": 200,
        "message": "Customer deleted",
        "data": deleted
    }
