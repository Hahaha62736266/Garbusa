_customers = {}

class Customer:
    @staticmethod
    def all():
        return list(_customers.values())
    @staticmethod
    def find(customer_id):
        return _customers.get(customer_id)
    @staticmethod
    def save(data):
        _customers[data["customer_id"]] = data
        return data
    @staticmethod
    def update(customer_id, data):
        if customer_id in _customers:
            _customers[customer_id].update(data)
            return _customers[customer_id]
        return None
    @staticmethod
    def remove(customer_id):
        if customer_id in _customers:
            del _customers[customer_id]
            return True
        return False
