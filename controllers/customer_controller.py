
# ===================================
# Customer Stub Handlers
# ===================================

def listCustomers(request):
    """GET /customers — List all customers"""
    return {
        "status": 200,
        "data": { "message": "listCustomers stub" },
        "error": None
    }


def showCustomer(request):
    """GET /customers/:customer_id — View one customer"""
    customer_id = request.params.get("customer_id")
    return {
        "status": 200,
        "data": {
            "message": "showCustomer stub",
            "customer_id": customer_id
        },
        "error": None
    }


def createCustomer(request):
    """POST /customers — Create new customer"""
    return {
        "status": 201,
        "data": { "message": "createCustomer stub" },
        "error": None
    }


def updateCustomer(request):
    """PUT /customers/:customer_id — Update customer"""
    customer_id = request.params.get("customer_id")
    return {
        "status": 200,
        "data": {
            "message": "updateCustomer stub",
            "customer_id": customer_id
        },
        "error": None
    }


def deleteCustomer(request):
    """DELETE /customers/:customer_id — Delete customer"""
    customer_id = request.params.get("customer_id")
    return {
        "status": 200,
        "data": {
            "message": "deleteCustomer stub",
            "customer_id": customer_id
        },
        "error": None
    }
