import re

PHONE_PATTERN = re.compile(r'^09\d{2}-\d{3}-\d{4}$')

def validateCustomerCreate(req):
    b = req.body
    required = ["customer_id","full_name","contact_number","address","container_owned"]
    for f in required:
        if f not in b:
            return {"status":422,"error":f"Missing field: {f}","field":f}
    if not re.match(r'^C\d{3}$', b.get("customer_id","")):
        return {"status":422,"error":"customer_id must be C followed by 3 digits","field":"customer_id"}
    if not PHONE_PATTERN.match(b.get("contact_number","")):
        return {"status":422,"error":"contact_number format: 09XX-XXX-XXXX","field":"contact_number"}
    if not isinstance(b.get("container_owned"), int) or b["container_owned"] < 0:
        return {"status":422,"error":"container_owned must be non-negative integer","field":"container_owned"}
    req.validatedBody = b
    return None

def validateCustomerUpdate(req):
    return validateCustomerCreate(req)

def validateProductCreate(req):
    b = req.body
    required = ["product_id","product_name","price_per_unit","stock_available"]
    for f in required:
        if f not in b:
            return {"status":422,"error":f"Missing field: {f}","field":f}
    if not re.match(r'^P\d{3}$', b.get("product_id","")):
        return {"status":422,"error":"product_id must be P followed by 3 digits","field":"product_id"}
    if float(b.get("price_per_unit",0)) < 0:
        return {"status":422,"error":"price_per_unit cannot be negative","field":"price_per_unit"}
    if int(b.get("stock_available",0)) < 0:
        return {"status":422,"error":"stock_available cannot be negative","field":"stock_available"}
    req.validatedBody = b
    return None

def validateProductUpdate(req):
    return validateProductCreate(req)

ALLOWED_STATUSES = ["Pending","Delivered"]

def validateOrderCreate(req):
    b = req.body
    required = ["order_id","customer_id","product_id","quantity","status"]
    for f in required:
        if f not in b:
            return {"status":422,"error":f"Missing field: {f}","field":f}
    if not re.match(r'^O\d{3}$', b.get("order_id","")):
        return {"status":422,"error":"order_id must be O followed by 3 digits","field":"order_id"}
    if int(b.get("quantity",0)) <= 0:
        return {"status":422,"error":"quantity must be positive","field":"quantity"}
    if b.get("status") not in ALLOWED_STATUSES:
        return {"status":422,"error":"status must be Pending or Delivered","field":"status"}
    req.validatedBody = b
    return None

def validateOrderUpdate(req):
    return validateOrderCreate(req)

def validateCollectionCreate(req):
    b = req.body
    required = ["collection_id","customer_id","empty_jugs_returned","filled_jugs_released","container_balance","collected_by"]
    for f in required:
        if f not in b:
            return {"status":422,"error":f"Missing field: {f}","field":f}
    if not re.match(r'^CL\d{3}$', b.get("collection_id","")):
        return {"status":422,"error":"collection_id must be CL followed by 3 digits","field":"collection_id"}
    if int(b.get("container_balance",0)) < 0:
        return {"status":422,"error":"container_balance cannot be negative","field":"container_balance"}
    req.validatedBody = b
    return None

def validateCollectionUpdate(req):
    return validateCollectionCreate(req)

def checkOwnership(req, recordOwnerId):
    currentUserId = req.auth.get("user_id") if req.auth else None
    if not currentUserId:
        return {"status":403,"error":"Not authenticated","field":None}
    if str(currentUserId) != str(recordOwnerId):
        return {"status":403,"error":"Forbidden: you do not own this record","field":None}
    return None

def authorizeDeleteOrder(req):
    from models.order_model import Order
    oid = req.params.get("order_id")
    existing = Order.find(oid)
    if not existing:
        return {"status":404,"error":"Record not found","field":None}
    return checkOwnership(req, existing.get("customer_id"))
