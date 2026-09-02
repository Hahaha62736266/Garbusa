from models.customer_model import Customer
def listCustomers(r): return {"status":200,"data":Customer.all(),"error":None}
def showCustomer(r): return {"status":200,"data":Customer.find(r.params.get("customer_id")),"error":None}
def createCustomer(r): return {"status":201,"data":Customer.save(r.validatedBody),"error":None}
def updateCustomer(r): return {"status":200,"data":Customer.update(r.params.get("customer_id"),r.validatedBody),"error":None}
def deleteCustomer(r): Customer.remove(r.params.get("customer_id")); return {"status":200,"data":{},"error":None}
