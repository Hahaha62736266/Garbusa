_collections = {}

class Collection:
    @staticmethod
    def all():
        return list(_collections.values())
    @staticmethod
    def find(collection_id):
        return _collections.get(collection_id)
    @staticmethod
    def save(data):
        _collections[data["collection_id"]] = data
        return data
    @staticmethod
    def update(collection_id, data):
        if collection_id in _collections:
            _collections[collection_id].update(data)
            return _collections[collection_id]
        return None
    @staticmethod
    def remove(collection_id):
        if collection_id in _collections:
            del _collections[collection_id]
            return True
        return False
