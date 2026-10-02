"""Customer Controller — MockRequest compatible"""
from datetime import date

customers_db = {}

def _extract_payload(data):
    if hasattr(data, 'validatedBody') and data.validatedBody is not None:
        return data.validatedBody
    if hasattr(data, 'body') and data.body is not None:
        return data.body
    if hasattr(data, 'get_json') and callable(data.get_json):
        j = data.get_json()
        if j is not None:
            return j
    if hasattr(data, 'json') and data.json is not None:
        return data.json
    if isinstance(data, dict):
        return data
    if hasattr(data, '__dict__'):
        d = data.__dict__
        if 'validatedBody' in d and d['validatedBody']:
            return d['validatedBody']
        if 'body' in d and d['body']:
            return d['body']
        return d
    return {}

def listCustomers(request=None):
    return {
        "status": 200,
        "message": "Customers retrieved successfully",
        "data": list(customers_db.values())
    }

list_customers = listCustomers

def showCustomer(customer_id):
    if not isinstance(customer_id, str):
        customer_id = getattr(customer_id, 'params', {}).get("customer_id", "")
    if customer_id not in customers_db:
        return {"status": 404, "error": "Not Found", "message": "Customer not found"}
    return {
        "status": 200,
        "message": "Customer retrieved",
        "data": customers_db[customer_id]
    }

show_customer = showCustomer

def createCustomer(data):
    payload = _extract_payload(data)

    new_id = payload.get("customer_id") or f"C{len(customers_db)+1:03d}"
    customer = {
        "customer_id": new_id,
        "full_name": payload.get("full_name"),
        "contact_number": payload.get("contact_number"),
        "address": payload.get("address"),
        "container_owned": payload.get("container_owned", 0),
        "registration_date": str(date.today()),
        "owned_by_user_id": payload.get("owned_by_user_id") or new_id
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

create_customer = createCustomer

def updateCustomer(customer_id, data=None):
    if data is None and hasattr(customer_id, 'params'):
        req = customer_id
        customer_id = req.params.get("customer_id", "")
        data = req

    if not isinstance(customer_id, str):
        customer_id = getattr(customer_id, 'params', {}).get("customer_id", "")

    payload = _extract_payload(data)

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

update_customer = updateCustomer

def deleteCustomer(customer_id):
    if not isinstance(customer_id, str):
        customer_id = getattr(customer_id, 'params', {}).get("customer_id", "")
    if customer_id not in customers_db:
        return {"status": 404, "error": "Not Found", "message": "Customer not found"}
    deleted = customers_db.pop(customer_id)
    return {
        "status": 200,
        "message": "Customer deleted",
        "data": deleted
    }

delete_customer = deleteCustomer
