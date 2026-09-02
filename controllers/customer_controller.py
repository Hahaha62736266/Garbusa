# ==========================================================
# THIN CONTROLLER: Customers
# NO validation here — already done in middleware
# NO direct DB code — call Model only
# ==========================================================
from models.customer_model import Customer

def listCustomers(request):
    """GET /customers — List all"""
    customers = Customer.all()
    return {"status": 200, "data": customers, "error": None}

def showCustomer(request):
    """GET /customers/:customer_id — Show one"""
    customer_id = request.params.get("customer_id")
    customer = Customer.find(customer_id)
    return {"status": 200, "data": customer, "error": None}

def createCustomer(request):
    """POST /customers — Create (validatedBody already clean)"""
    data = request.validatedBody
    customer = Customer.save(data)
    return {"status": 201, "data": customer, "error": None}

def updateCustomer(request):
    """PUT /customers/:customer_id — Update"""
    customer_id = request.params.get("customer_id")
    data = request.validatedBody
    customer = Customer.update(customer_id, data)
    return {"status": 200, "data": customer, "error": None}

def deleteCustomer(request):
    """DELETE /customers/:customer_id — Delete"""
    customer_id = request.params.get("customer_id")
    Customer.remove(customer_id)
    return {"status": 200, "data": {"deleted_id": customer_id}, "error": None}
