# ==========================================================
# THIN CONTROLLER: Customers — ADAPTED TO FUNCTION-BASED MODEL
# ==========================================================
from models import customer_model

# ✅ WRAPPER CLASS — matches what your test/middleware expects
class CustomerModel:
    def __init__(self, data):
        self.data = data

    def create(self):
        """Match the .create() pattern your tests are calling"""
        try:
            record = customer_model.save(self.data)
            return {"success": True, "data": record}
        except Exception as e:
            return {"success": False, "error": str(e)}


def createCustomer(req):
    """ARRANGE → model = Class(data); result = model.create()"""
    data = req.validatedBody or req.body
    model = CustomerModel(data)       # ✅ What your test expects
    result = model.create()           # ✅ What your test expects

    if result.get("success"):
        return {
            "status": 201,
            "message": "Customer created successfully",
            "data": result.get("data")
        }
    return {
        "status": 500,
        "message": "Failed to create customer",
        "error": result.get("error")
    }
