# models/product_model.py
"""
Product Model — Aquaflow Tracker
Defines Product entity and helper methods
"""
"""Product Model."""

class Product:
    def __init__(self, product_id, product_name, price_per_unit,
                 description="", stock_available=0):
        self.product_id = product_id
        self.product_name = product_name
        self.price_per_unit = price_per_unit
        self.description = description
        self.stock_available = stock_available

    def to_dict(self):
        return {
            "product_id": self.product_id,
            "product_name": self.product_name,
            "price_per_unit": self.price_per_unit,
            "description": self.description,
            "stock_available": self.stock_available
        }


# Simple in-memory "database" — replace with real DB later
products_db = {}


def get_all_products():
    """Return list of all products as dictionaries"""
    return [p.to_dict() for p in products_db.values()]


def get_product_by_id(product_id):
    """Get single product by ID"""
    product = products_db.get(product_id)
    return product.to_dict() if product else None

# ─── ADD THIS at the BOTTOM of models/product_model.py ───
_products = {}
_next_product_id = 1

def save(data):
    """Create new product — matches pattern used by Customer/Order"""
    global _next_product_id
    record = {
        "id": _next_product_id,
        "product_id": data.get("product_id"),
        "product_name": data.get("product_name"),
        "price_per_unit": data.get("price_per_unit"),
        "stock_available": data.get("stock_available", 0)
    }
    _products[data["product_id"]] = record
    _next_product_id += 1
    return record
# ─── In-memory storage ───
_products = {}
_next_product_id = 1

def save(data):
    """Create new product — matches pattern used by Customer & Order"""
    global _next_product_id
    record = {
        "id": _next_product_id,
        "product_id": data.get("product_id"),
        "product_name": data.get("product_name"),
        "price_per_unit": data.get("price_per_unit"),
        "stock_available": data.get("stock_available", 0)
    }
    _products[data["product_id"]] = record
    _next_product_id += 1
    return record