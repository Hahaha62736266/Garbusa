# ✅ middleware/validation.py — GUARDS LIVE HERE
def validateCustomerCreate(request):
    data = request.body
    if not data.get("customer_id"):       # ✅ Validation HERE
        return {"status":422,...}
    request.validatedBody = cleanData      # ✅ Attach clean data
    return None  # No error = proceed

# ✅ controllers/customer_controller.py — THIN
def createCustomer(request):
    data = request.validatedBody           # ✅ Already clean!
    customer = Customer.save(data)         # ✅ Only work, no checks
    return {"status":201, "data":customer, "error":None}
