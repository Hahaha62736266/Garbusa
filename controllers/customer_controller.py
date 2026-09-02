# OWNER: Baydal
def listCustomers(request):
    return {"status":200,"data":{"message":"listCustomers stub"},"error":None}

def showCustomer(request):
    cid = request.params.get("customer_id")
    return {"status":200,"data":{"message":"showCustomer stub","customer_id":cid},"error":None}

def createCustomer(request):
    return {"status":201,"data":{"message":"createCustomer stub"},"error":None}

def updateCustomer(request):
    cid = request.params.get("customer_id")
    return {"status":200,"data":{"message":"updateCustomer stub","customer_id":cid},"error":None}

def deleteCustomer(request):
    cid = request.params.get("customer_id")
    return {"status":200,"data":{"message":"deleteCustomer stub","customer_id":cid},"error":None}


# OWNER: Baydal
import re

def createCustomer(request):
    data = request.body or {}

    # GUARD CLAUSES — Check BAD cases FIRST
    if not data.get("customer_id"):
        return {"status": 422, "data": None, "error": "customer_id is required"}
    if not re.match(r"^C\d{3}$", data["customer_id"]):
        return {"status": 422, "data": None, "error": "customer_id must be C followed by 3 digits (e.g. C001)"}

    if not data.get("full_name"):
        return {"status": 422, "data": None, "error": "full_name is required"}
    if not isinstance(data["full_name"], str) or not (2 <= len(data["full_name"]) <= 100):
        return {"status": 422, "data": None, "error": "full_name must be 2–100 characters"}

    if not data.get("contact_number"):
        return {"status": 422, "data": None, "error": "contact_number is required"}
    if not re.match(r"^09\d{2}-\d{3}-\d{4}$", data["contact_number"]):
        return {"status": 422, "data": None, "error": "contact_number must use format 09XX-XXX-XXXX"}

    if not data.get("address") or len(data["address"]) < 5:
        return {"status": 422, "data": None, "error": "address is required (min 5 characters)"}

    if "container_owned" not in data:
        return {"status": 422, "data": None, "error": "container_owned is required"}
    if not isinstance(data["container_owned"], int) or data["container_owned"] < 0:
        return {"status": 422, "data": None, "error": "container_owned must be a non-negative integer"}

    # ✅ ALL VALID — Proceed to create
    return {"status": 201, "data": {"message": "createCustomer stub"}, "error": None}

# OWNER: Baydal
def updateCustomer(request):
    customer_id = request.params.get("customer_id")
    data = request.body or {}

    # GUARD CLAUSES
    if not re.match(r"^C\d{3}$", customer_id or ""):
        return {"status": 422, "data": None, "error": "customer_id must be C followed by 3 digits"}

    if "full_name" in data:
        if not isinstance(data["full_name"], str) or not (2 <= len(data["full_name"]) <= 100):
            return {"status": 422, "data": None, "error": "full_name must be 2–100 characters"}

    if "contact_number" in data:
        if not re.match(r"^09\d{2}-\d{3}-\d{4}$", data["contact_number"]):
            return {"status": 422, "data": None, "error": "contact_number must use format 09XX-XXX-XXXX"}

    if "address" in data and len(data["address"]) < 5:
        return {"status": 422, "data": None, "error": "address must be at least 5 characters"}

    if "container_owned" in data:
        if not isinstance(data["container_owned"], int) or data["container_owned"] < 0:
            return {"status": 422, "data": None, "error": "container_owned must be a non-negative integer"}

    # ✅ ALL VALID — Proceed to update
    return {"status": 200, "data": {"message": "updateCustomer stub", "customer_id": customer_id}, "error": None}

# OWNER: Baydal
# THIN CONTROLLER — Validation runs BEFORE → use validatedBody

# Data Layer import (assumes models exist)
from models.customer_model import Customer

def listCustomers(request):
    """GET /customers — List all"""
    customers = Customer.all()
    return {"status": 200, "data": customers, "error": None}

def showCustomer(request):
    """GET /customers/:customer_id — Show one"""
    cid = request.params.get("customer_id")
    customer = Customer.find(cid)
    return {"status": 200, "data": customer, "error": None}

def createCustomer(request):
    """POST /customers — Create (validatedBody already clean)"""
    data = request.validatedBody           # ✅ Validation done upstream
    customer = Customer.save(data)          # ✅ Data Layer only
    return {"status": 201, "data": customer, "error": None}

def updateCustomer(request):
    """PUT /customers/:customer_id — Update"""
    cid = request.params.get("customer_id")
    data = request.validatedBody
    customer = Customer.update(cid, data)
    return {"status": 200, "data": customer, "error": None}

def deleteCustomer(request):
    """DELETE /customers/:customer_id — Delete"""
    cid = request.params.get("customer_id")
    Customer.remove(cid)
    return {"status": 200, "data": {"deleted_id": cid}, "error": None}
