_products = {}

class Product:
    @staticmethod
    def all():
        return list(_products.values())
    @staticmethod
    def find(product_id):
        return _products.get(product_id)
    @staticmethod
    def save(data):
        _products[data["product_id"]] = data
        return data
    @staticmethod
    def update(product_id, data):
        if product_id in _products:
            _products[product_id].update(data)
            return _products[product_id]
        return None
    @staticmethod
    def remove(product_id):
        if product_id in _products:
            del _products[product_id]
            return True
        return False
