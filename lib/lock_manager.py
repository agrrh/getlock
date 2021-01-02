from flask_restful import Resource, reqparse

from lib.lock import Lock

# TODO Some persistent storage
#   https://github.com/hashicorp/nomad-guides/blob/master/application-deployment/redis/redis.nomad
locks = {}


class LockManager(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "ttl", type=float, default=60.0, help="Time for lock to live without refreshes"
    )

    def __init__(self, storage=None):
        self.storage = storage

    # FIXME Steal prevention, some kind of owner token?
    def put(self, lock_id):
        lock_id = str(lock_id)

        args = self.parser.parse_args(strict=True)

        lock_data = self.storage.read(lock_id)

        if not lock_data:
            lock = Lock(lock_id, **args)
            self.storage.create(lock.id, lock.__dict__)
            self.storage.ttl(lock.id, int(lock.ttl))
            return {
                "locked": True,
                "message": "lock acquired",
                "lock": lock.__dict__,
            }, 201

        lock = Lock(**lock_data)

        lock.refresh()
        self.storage.update(lock_id, lock.__dict__)
        self.storage.ttl(lock.id, int(lock.ttl))

        return {"locked": True, "message": "lock refreshed", "lock": lock.__dict__}, 200

    def get(self, lock_id):
        lock_id = str(lock_id)

        lock_data = self.storage.read(lock_id)

        if not lock_data:
            return {"locked": False, "message": "lock not found or expired"}, 404

        lock = Lock(**lock_data)

        if not lock.is_active():
            self.storage.delete(lock.id)
            return {
                "locked": False,
                "message": "lock has expired",
                "lock": lock.__dict__,
            }, 404

        return {"locked": True, "message": "lock is active", "lock": lock.__dict__}, 423

    # FIXME Add some security, like check for owner token?
    def delete(self, lock_id):
        lock_id = str(lock_id)

        lock_data = self.storage.read(lock_id)

        if not lock_data:
            return {"locked": False, "message": "lock not found or expired"}, 404

        lock = Lock(**lock_data)

        self.storage.delete(lock_id)

        return {
            "locked": False,
            "message": "lock has been removed",
            "lock": lock.__dict__,
        }, 200
