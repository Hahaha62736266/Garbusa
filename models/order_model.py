_orders = {}

class Order:
    @staticmethod
    def all():
        return list(_orders.values())
    @staticmethod
    def find(order_id):
        return _orders.get(order_id)
    @staticmethod
    def save(data):
        _orders[data["order_id"]] = data
        return data
    @staticmethod
    def update(order_id, data):
        if order_id in _orders:
            _orders[order_id].update(data)
            return _orders[order_id]
        return None
    @staticmethod
    def remove(order_id):
        if order_id in _orders:
            del _orders[order_id]
            return True
        return False
