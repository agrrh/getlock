from flask_restful import Resource

from lib.lock import Lock


# TODO Refactor this shit
class LockCatalog(Resource):
    def __init__(self, storage=None):
        self.storage = storage

    def get(self):
        locks_id_list = self.storage.list()

        locks_count = len(locks_id_list)

        def locks_generator():
            for lock_id in self.storage.list():
                lock_data = self.storage.read(lock_id)
                if lock_data:
                    yield Lock(**lock_data)

        return {
            "message": "okay",
            "locks": {lock.id: lock.__dict__ for lock in locks_generator()},
            "locks_count": locks_count,
        }, 200
