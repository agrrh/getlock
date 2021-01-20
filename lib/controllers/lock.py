from flask_restful import Resource, reqparse, request

from lib.objects.namespace import Namespace
from lib.objects.lock import Lock


class LockController(Resource):
    # TODO Validate ID here and for other methods
    # TODO Check access as separate method or decorator
    #   https://flask-restful.readthedocs.io/en/latest/extending.html#resource-method-decorators

    parser = reqparse.RequestParser()
    parser.add_argument(
        "ttl", type=int, default=60, help="Time for lock to live without refreshes"
    )

    def __init__(self, storage):
        self.storage = storage

    def put(self, namespace_id: str, lock_id: str):
        namespace = Namespace(storage=self.storage, id=namespace_id)

        if not namespace.read():
            return {"message": "Namespace not found", "lock": None}, 404

        token = request.headers.get("X-Getlock-Auth")

        if token != namespace.token:
            return {"message": "Provided wrong auth token"}, 403

        args = self.parser.parse_args(strict=True)

        lock = Lock(storage=self.storage, id=lock_id, namespace=namespace, **args)

        if not lock.read():
            lock.create()
            return {"message": "Lock created", "lock": lock._dump()}, 201

        lock.update()

        return {"message": "Lock updated", "lock": lock._dump()}, 201

    def get(self, namespace_id: str, lock_id: str):
        namespace = Namespace(storage=self.storage, id=namespace_id)

        if not namespace.read():
            return {"message": "Namespace not found", "lock": None}, 404

        lock = Lock(storage=self.storage, id=lock_id, namespace=namespace)

        if not lock.read():
            return {"message": "Lock not found", "lock": None}, 404

        lock._load_self()

        return {"message": "Lock found", "lock": lock._dump()}, 200

    def delete(self, namespace_id: str, lock_id: str):
        namespace = Namespace(storage=self.storage, id=namespace_id)

        if not namespace.read():
            return {"message": "Namespace not found", "lock": None}, 404

        token = request.headers.get("X-Getlock-Auth")

        if token != namespace.token:
            return {"message": "Provided wrong auth token"}, 403

        lock = Lock(storage=self.storage, id=lock_id, namespace=namespace)

        if not lock.read():
            return {"message": "Lock not found", "lock": None}, 404

        lock.delete()

        return {"message": "Lock removed", "lock": lock._dump()}, 200
