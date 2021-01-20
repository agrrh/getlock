from flask_restful import Resource

from lib.namespace import Namespace
from lib.lock import Lock


class LockController(Resource):
    def __init__(self, storage):
        self.storage = storage

    def put(self, namespace_id: str, lock_id: str):
        namespace = Namespace(storage=self.storage, id=namespace_id)

        if not namespace.read():
            return {"message": "Namespace not found", "lock": None}, 404

        lock = Lock(storage=self.storage, id=lock_id, namespace=namespace)

        # TODO Check auth
        # TODO Use data sent

        if not lock.read():
            lock.create()
            return {"message": "Lock created", "lock": lock._dump()}, 201

        lock.update()

        return {"message": "Lock updated", "lock": lock._dump()}, 201

    def get(self, namespace_id: str, lock_id: str):
        namespace = Namespace(storage=self.storage, id=namespace_id)

        if not namespace.read():
            return {"message": "Namespace not found", "lock": None}, 404

        # TODO Check auth

        lock = Lock(storage=self.storage, id=lock_id, namespace=namespace)

        if not lock.read():
            return {"message": "Lock not found", "lock": None}, 404

        lock._load_self()

        return {"message": "Lock found", "lock": lock._dump()}, 200

    def delete(self, namespace_id: str, lock_id: str):
        namespace = Namespace(storage=self.storage, id=namespace_id)

        if not namespace.read():
            return {"message": "Namespace not found", "lock": None}, 404

        # TODO Check auth

        lock = Lock(storage=self.storage, id=lock_id, namespace=namespace)

        if not lock.read():
            return {"message": "Lock not found", "lock": None}, 404

        lock.delete()

        return {"message": "Lock removed", "lock": lock._dump()}, 200
