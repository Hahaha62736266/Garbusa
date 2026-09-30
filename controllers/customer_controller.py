"""Customer Controller — MockRequest compatible"""
from datetime import date

customers_db = {}

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

def createCustomer(data):
    # ✅ Read from __dict__ — NO MORE None values!
    if hasattr(data, '__dict__'):
        payload = data.__dict__
    elif hasattr(data, 'json') and data.json is not None:
        payload = data.json
    else:
        payload = data if isinstance(data, dict) else {}

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

    return {
        "status": 201,
        "message": "Customer created",
        "data": {
            "id": len(customers_db),
            "customer_id": new_id,
            "full_name": customer["full_name"],
            "contact_number": customer["contact_number"],
            "address": customer["address"],
            "container_owned": customer["container_owned"],
            "owned_by_user_id": customer["owned_by_user_id"]
        }
    }
def updateCustomer(customer_id, data):
    if hasattr(data, 'json'):
        payload = data.json
    else:
        payload = data

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
